# YouTube Video Summarizer

This project provides two implementations of a YouTube video summarizer:
1. **Web App** using Flask + HTML (user-friendly interface).
2. **Terminal-based Transcript Fetcher** for quick summaries.

---

## Features

- Fetch transcripts from YouTube videos.
- Summarize video content using the Cohere API.
- Web app version with Flask + HTML.
- Terminal version for lightweight usage.

---

## Project Structure

```
yt_video_summarizer/
│
├── app.py                # Flask web app entry point
├── templates/
│   └── index.html        # Frontend HTML for video input and display
│
├── transcript_fetcher.py # Terminal-based summarizer implementation
├── .env                  # Store your Cohere API key
├── requirements.txt      # Dependencies
└── README.md             # Documentation (this file)
```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/yt_video_summarizer.git
   cd yt_video_summarizer
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate    # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root folder with your Cohere API key:
   ```env
   API_KEY=your_actual_cohere_api_key_here
   ```

---

## Usage

### Flask Web App

1. Run the app:
   ```bash
   python app.py
   ```
2. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```
3. Enter a YouTube video URL to get a summarized transcript.

---

### Terminal Transcript Fetcher

1. Run the terminal app:
   ```bash
   python transcript_fetcher.py
   ```

2. Enter a YouTube video URL in the terminal when prompted.

3. Get the transcript and summary printed in the console.

---

## Requirements

- Python 3.8+
- Flask
- python-dotenv
- Cohere
- youtube-transcript-api

---

## Notes

- Free Cohere API keys may expire or become invalid after a while. Generate a new one if needed.
- If transcripts are unavailable for a given video, the summarizer will not work.
