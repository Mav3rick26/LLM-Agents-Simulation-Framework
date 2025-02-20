import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()


def perform_sentiment_analysis(text):
    scores = analyzer.polarity_scores(text)
    sentiment_value = scores['compound']
    return sentiment_value
