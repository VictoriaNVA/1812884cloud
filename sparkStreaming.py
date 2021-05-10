from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SQLContext
import pandas as pd

# create spark configuration
conf = SparkConf()
conf.setAppName("TwitterStreamApp")

# create spark context with the above configuration
spark_ctx = SparkContext(conf=conf)
spark_ctx.setLogLevel("ERROR")

# create the Streaming Context from the above spark context with interval size of 1 minute
str_ctx = StreamingContext(spark_ctx, 60)

# Checkpoint for RDD recovery
str_ctx.checkpoint("checkpoint_TwitterApp")
# Read data from port (changed regularly)
dataStream = str_ctx.socketTextStream("localhost", 5555)


# This method adds up the previous hashtag count with the new count and returns the sum
def aggregate_count(new_values, total_sum):
    return sum(new_values) + (total_sum or 0)


# Get SQL context from spark context
def get_sql(spark_context):
    if 'sqlContextSingletonInstance' not in globals():
        globals()['sqlContextSingletonInstance'] = SQLContext(spark_context)
    return globals()['sqlContextSingletonInstance']


# This method processes the hashtags RDD
# Note that at the moment data is displayed AFTER the first interval
# The more intervals pass the more accurate hashtag count is
def process_data(time, rdd):
    print("----------- %s -----------" % str(time))
    print("-----------Please wait...------------------\n")
    try:
        # Get spark sql singleton context
        sql_ctx = get_sql(rdd.context)
        # Convert to row rdd and create dataframe
        row_rdd = rdd.map(lambda w: Row(word=w[0], count=w[1]))
        hashtags_df = sql_ctx.createDataFrame(row_rdd)
        # Create hashtags table from dataframe
        hashtags_df.registerTempTable("words")
        # Query top 10 trending hashtags
        hashtags_top = sql_ctx.sql(
            "select word, count from words where word like '#%'order by count desc"
            " limit 10")
        # Query top 10 trending words
        trending_top = sql_ctx.sql(
            "select word, count from words where CHAR_LENGTH(word) > 5"
            " order by count desc limit 10")

        if option == "H":
            # Print top 10 hashtags
            print("-----------Stream of trending hashtags-----------")
            hashtags_top.show()
            # Save the dataframe to csv for word cloud
            hashtags_top.toPandas().to_csv('trending.csv', index=False, index_label=None)
        elif option == "T":
            # Print top 10 hashtags
            print("-----------Stream of trending words-----------")
            trending_top.show()
            # Save the dataframe to csv for word cloud
            trending_top.toPandas().to_csv('trending.csv', index=False, index_label=None)
        else:
            print("Input not valid. Showing default: hashtags")
            hashtags_top.show()
        # Save to csv file for word cloud
    except:
        pass


# Data stored for a 10 min window
lines = dataStream.window(60*10)
# Split each tweet into words
words = lines.flatMap(lambda line: line.split(" "))
# Filter the words to get hashtags, then map to pairs of (hashtag,count) and update count
hashtags = words.map(lambda x: (x.lower(), 1)) \
    .updateStateByKey(aggregate_count)
# Process the RDD
hashtags.foreachRDD(process_data)

# User input for trending words (may also include hashtags) or trending hashtags only
option = input('You can view top trending words or top hashtags.\nPlease type in one of the options as T or H: ')
option = option.upper()
# Start streaming and await finish
str_ctx.start()
str_ctx.awaitTermination()
