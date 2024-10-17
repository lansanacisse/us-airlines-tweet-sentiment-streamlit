# import streamlit
import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


# Title of pages

st.title("Sentiment Analysis of Tweets about US Airlines")
st.sidebar.title("US Airlines")


st.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")
st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of Tweets 🐦")

# add decorator to cache data
@st.cache_data(persist=False) # persist=False means that the data will not be stored in the cache

# Function to load data
def load_data():
    data = pd.read_csv("Tweets.csv")
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

# Load data
data = load_data()


# write data
#st.write(data)

# Show random tweet
st.sidebar.subheader("Show random tweet")
random_tweet = st.sidebar.radio('Sentiment', ('positive', 'neutral', 'negative'))

st.sidebar.markdown(data.query("airline_sentiment == @random_tweet")[["text"]].sample(n=1).iat[0, 0])


# Number of tweets by sentiment
st.sidebar.subheader("Number of tweets by sentiment")
select = st.sidebar.selectbox('Visualization type', ['Bar plot', 'Pie chart'], key='1') # key is used to avoid error
sentiment_count = data['airline_sentiment'].value_counts() # count the number of sentiment
sentiment_count = pd.DataFrame({'Sentiment':sentiment_count.index, 'Tweets':sentiment_count.values})

# Write sentiment count data frame if not hide
if not st.sidebar.checkbox("Hide", True):
    st.subheader("Number of tweets by sentiment")
    if select == 'Bar plot':
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig)
    elif select == 'Pie chart':
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment')
        st.plotly_chart(fig)
    else :
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=500)
        st.plotly_chart(fig) 


# Create map for location of tweets
st.sidebar.subheader("When and where are users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23) # slider for hour of day to filter data by hour
modified_data = data[data['tweet_created'].dt.hour == hour] # filter data by hour
if not st.sidebar.checkbox("Close", True, key='close_checkbox'):
    st.markdown("### Tweet locations based on time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour + 1) % 24))
    st.map(modified_data)
    if st.sidebar.checkbox("Show raw data", False):
        st.write(modified_data)

# Breakdown of airline tweets
st.sidebar.subheader("Breakdown of airline tweets")
airline = st.sidebar.multiselect('Airline', ['US Airways', 'United', 'American', 'Southwest', 'Delta', 'Virgin America'], key='airline')

if len(airline) > 0:
    airline_data = data[data.airline.isin(airline)]
    fig_airline = px.histogram(airline_data, x='airline', y='airline_sentiment', histfunc='count', color='airline_sentiment',
    facet_col='airline_sentiment', labels={'airline_sentiment':'tweets'}, height=600, width=800)
    st.plotly_chart(fig_airline)

# Create word cloud
st.sidebar.subheader("Word Cloud")
word_sentiment = st.sidebar.radio('Display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("Close", True, key='close_checkbox_wordcloud'):
    st.subheader('Word cloud for %s sentiment' % word_sentiment)
    df = data[data['airline_sentiment'] == word_sentiment]
    words = ' '.join(df['text'])
    processed_words = ' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud = WordCloud(stopwords=STOPWORDS, background_color='white', width=800, height=640).generate(processed_words)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud)
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)
