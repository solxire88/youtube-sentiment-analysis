# YouTube Sentiment Analysis Dashboard

![YouTube Sentiment Analysis Dashboard](/assets/ss1.png)
![](/assets/ss2.png)
![](/assets/ss3.png)


## Overview

**YouTube Sentiment Analysis Dashboard** is an interactive web application built with Streamlit that allows you to analyze the sentiment of YouTube video comments. By leveraging the YouTube Data API and Hugging Face's sentiment analysis pipeline, this project retrieves video statistics and comment data, then visualizes the sentiment analysis through interactive graphs and metrics.

## Features

- **Video Metrics:** Displays overall video statistics such as views, likes, and comment count.
- **Comment Analysis:** Fetches comments along with metadata like published date and like count.
- **Sentiment Analysis:** Uses a pre-trained Hugging Face sentiment analysis pipeline to classify each comment.
- **Advanced Visualizations:**
  - Sentiment distribution bar chart.
  - Histogram and box plot of sentiment scores.
  - Time series analysis showing the progression of average sentiment over time.
- **Responsive Layout:** Clean and modern UI with a sidebar for input and an interactive dashboard view.

## Prerequisites

- Python 3.7 or higher
- A valid **YouTube Data API v3 key**

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/solxire88/youtube-sentiment-analysis.git
   cd youtube-sentiment-analysis
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install the Required Packages**

   ```bash
   pip install -r requirements.txt
   ```

   *Alternatively, install dependencies manually:*

   ```bash
   pip install streamlit python-dotenv transformers pandas plotly google-api-python-client
   ```

4. **Configure Environment Variables**

   Create a `.env` file in the root directory with your YouTube API key:

   ```dotenv
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```

## Usage

1. **Run the Streamlit App**

   ```bash
   streamlit run app.py
   ```

2. **Interact with the Dashboard**

   - Enter a YouTube video URL in the sidebar.
   - The app will fetch video statistics and comments.
   - Sentiment analysis is performed on the comments and displayed with interactive visualizations.
   - Explore the various metrics and charts provided.

## Project Structure

```
├── main.py                # Main Streamlit application script
├── .env                  # Environment variable file (not committed)
├── requirements.txt      # List of Python dependencies
└── README.md             # Project description and usage instructions
```

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request if you have ideas for improvements, bug fixes, or additional features.


## Acknowledgements

- [Streamlit](https://streamlit.io/) for making it easy to build interactive dashboards.
- [Hugging Face](https://huggingface.co/) for their excellent NLP models.
- [Google APIs](https://developers.google.com/youtube/v3) for providing access to YouTube data.

---

Happy analyzing! If you have any questions or feedback, please feel free to reach out.
