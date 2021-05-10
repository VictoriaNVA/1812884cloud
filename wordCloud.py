import matplotlib.pyplot as plt
from wordcloud import WordCloud
import pandas as pd

# Read csv into dataframe
df = pd.read_csv('trending.csv')
words = df.word

# Generate word cloud of the trending words
word_cloud = WordCloud(background_color="white").generate(str(words))
plt.figure()
plt.imshow(word_cloud, interpolation="bilinear")
plt.axis("off")
plt.show()
