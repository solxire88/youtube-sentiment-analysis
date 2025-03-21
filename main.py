import streamlit as st
from dotenv import load_dotenv
import os
import re
from transformers import pipeline
import pandas as pd
import plotly.express as px 
from googleapiclient.discovery import build


st.set_page_config(
    page_title="YouTube Sentiment Analysis Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    /* Overall page style */
    .reportview-container {
        background: #f0f2f6;
    }
    /* Sidebar style */
    .sidebar .sidebar-content {
        background: #ffffff;
    }
    /* Title style */
    h1 {
        font-family: 'Segoe UI', sans-serif;
        color: #333333;
    }
    /* Metric style */
    .stMetric {
        font-size: 1.2rem;
        color: #444444;
    }
    /* Button style */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5em 1em;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True
)


load_dotenv()
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
if not YOUTUBE_API_KEY:
    st.error("Please set YOUTUBE_API_KEY in your .env file.")
    st.stop()


@st.cache_resource
def get_youtube_service():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def fetch_video_stats(video_id):
    youtube = get_youtube_service()
    request = youtube.videos().list(
        part="statistics,snippet",
        id=video_id
    )
    response = request.execute()
    if response.get("items"):
        item = response["items"][0]
        stats = item.get("statistics", {})
        return {
            "viewCount": int(stats.get("viewCount", 0)),
            "likeCount": int(stats.get("likeCount", 0)),
            "commentCount": int(stats.get("commentCount", 0))
        }
    return {}


def extract_video_id(url):
    regex = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
    match = re.search(regex, url)
    if match:
        return match.group(1)
    else:
        return None

def fetch_youtube_comments(video_id):
    youtube = get_youtube_service()
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    while request:
        response = request.execute()
        for item in response.get("items", []):
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment_data = {
                "text": snippet.get("textDisplay", ""),
                "publishedAt": snippet.get("publishedAt", ""),
                "likeCount": snippet.get("likeCount", 0)
            }
            comments.append(comment_data)
        request = youtube.commentThreads().list_next(request, response)
    return comments


@st.cache_data
def sentiment_analysis():
    return pipeline("sentiment-analysis",model="distilbert-base-uncased-finetuned-sst-2-english")


def analyze_comments(comments, sentiment_pipe):
    texts = [c["text"] for c in comments]
    sentiments = sentiment_pipe(texts, truncation=True)
    df = pd.DataFrame({
        "Comment": texts,
        "Sentiment": [s['label'] for s in sentiments],
        "Score": [s["score"] for s in sentiments],
        "PublishedAt": [c["publishedAt"] for c in comments],
        "LikeCount": [c["likeCount"] for c in comments]
    })

    df["PublishedAt"] = pd.to_datetime(df["PublishedAt"])

    df["SentimentScore"] = df.apply(lambda row: row["Score"] if row["Sentiment"]=="POSITIVE" else -row["Score"], axis=1)
    return df


def display_advanced_stats(df):
    # Bar Chart: Sentiment Distribution
    sentiment_counts = df["Sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["Sentiment", "Count"]
    fig_bar = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        color="Sentiment",
        title="Sentiment Distribution",
        labels={"Count": "Number of Comments"},
        template="plotly_white"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Histogram: Sentiment Score Distribution
    fig_hist = px.histogram(
        df,
        x="Score",
        color="Sentiment",
        marginal="box",
        nbins=20,
        title="Histogram of Sentiment Scores",
        labels={"Score": "Sentiment Score"},
        template="plotly_white"
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # Time Series: Average Sentiment Score Over Time
    if not df.empty:
        df["Date"] = df["PublishedAt"].dt.date
        daily_sentiment = df.groupby("Date")["SentimentScore"].mean().reset_index()
        fig_time = px.line(
            daily_sentiment,
            x="Date",
            y="SentimentScore",
            title="Average Sentiment Score Over Time",
            labels={"SentimentScore": "Average Sentiment Score", "Date": "Date"},
            template="plotly_white"
        )
        st.plotly_chart(fig_time, use_container_width=True)
    
    # Summary Statistics Table
    st.subheader("Summary Statistics by Sentiment")
    stats_df = df.groupby("Sentiment")["Score"].describe().reset_index()
    st.dataframe(stats_df)

# -----------------------------
# Streamlit Interface
# -----------------------------
st.sidebar.header("Video Input")
video_url = st.sidebar.text_input("Enter YouTube Video URL:")

st.title("YouTube Video Sentiment Analysis Dashboard")
st.markdown("Analyze the sentiment and engagement of YouTube video comments with advanced metrics and interactive visualizations.")

if video_url:
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("Invalid URL format")
    else:
        st.info("Fetching video statistics...")
        video_stats = fetch_video_stats(video_id)
        st.info("Fetching comments...")
        comments = fetch_youtube_comments(video_id)
        total_comments = len(comments)
        st.success("Fetched Comments Successfully.")
        
        # Display Video Stats in Metrics
        col_v1, col_v2, col_v3 = st.columns(3)
        with col_v1:
            st.metric("Video Views", video_stats.get("viewCount", "N/A"))
        with col_v2:
            st.metric("Video Likes", video_stats.get("likeCount", "N/A"))
        with col_v3:
            st.metric("Video Comment Count", video_stats.get("commentCount", "N/A"))
        
        if total_comments == 0:
            st.warning("No comments found.")
        else:
            sentiment_pipe = sentiment_analysis()
            df = analyze_comments(comments, sentiment_pipe)
            
            # Display Comment Metrics
            st.subheader("Comment Metrics:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Comments", total_comments)
            with col2:
                st.metric("Total Comment Likes", df["LikeCount"].sum())
            with col3:
                st.metric("Avg Comment Likes", f"{df['LikeCount'].mean():.2f}")
            
            st.subheader("Sentiment Analysis of Comments:")
            st.dataframe(df.head(10), use_container_width=True)
            display_advanced_stats(df)
