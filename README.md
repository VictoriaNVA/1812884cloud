# Project A: Stream Data Processing 

## Summary 
This project uses python with Twitter API and Apache Spark Streaming to receive a live data stream of tweets, and select the most frequently occurring words and hashtags. The data is presented as a dataframe table in the console, in 60 seconds intervals. The user chooses whether to display the top 10 trending hashtags or top 10 trending words before the stream runs. The running dataframe is exported as a CSV in order to be visualised as a simple Word Cloud.
Download the python files and create a new project in a python IDE such as PyCharm, adding the three files, twitterStream.py, sparkStreaming,py and wordCloud.py.

### References
This project was completed following these articles / tutorials:
- [Article](https://www.toptal.com/apache/apache-spark-streaming-twitter)
- [YouTube tutorial](https://www.youtube.com/watch?v=gf9VtGkQcwM)
- [Jupyter Notebook](https://pgirish.github.io/spark-project/index.html)
- [Word Cloud](https://www.datacamp.com/community/tutorials/wordcloud-python)

## Requirements
- Python
- Python IDE
- Apache Spark
- Hadoop winutils.exe (if running on Windows machines)
- Twitter Developer Account


## Install packages
Make sure to install the following packages, which are imported in some of the files. These can be installed using the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install requests
```
```bash
pip install requests_oauthlib
```
```bash
pip install pyspark
```
```bash
pip install matplotlib
```
```bash
pip install pandas
```
```bash
pip install wordcloud
```

## Running instructions
To function properly, the files must be ran in order. 
*Note:* in twitterStream.py, the twitter API tokens from the beginning of the file must be replaced. Instructions for how to get these credentials [here](https://rapidapi.com/blog/how-to-use-the-twitter-api/).
* Run the twitterStream.py file first. This file is in charge of receiving a near real-time filtered stream of Tweets from Twitter, and sending these tweets to a Socket TCP port. Once ran, the console will display the "Waiting for TCP connection..." message. This will change in the next steps
* Now, run sparkStreaming.py and wait. A warning will be displayed in the console, which can be ignored. sparkStreaming.py reads the data from the TCP port using a Spark Streaming context. The data stream RDD is filtered and transformed into a SQL dataframe table, which is saved locally as a csv, using Pandas. 
* Next, the console will give you instructions for input. Once an option is typed in, if you look in twitterStream's console output, you will see the live stream of tweets.
* Going back to sparkStreaming, the console will start to display the chosen option (trending words or trending hashtags) as a table of 10 words/hashtags and their frequency count. This will display every 60 seconds, and might not show exactly 10 entries if there aren't that many in the twitter stream.
* Wait for a few minutes for the data displayed in the console to reach a higher frequency count. Once the count is satisfactory, you can try to visualise it as a Word Cloud. You can stop the two files, but it is not necessary for the next step.
* To visualise the words/hashtags as a Word Cloud, run the wordCloud.py file.
