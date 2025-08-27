from flask import Flask, render_template, request
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
import cohere
import time
import os

app = Flask(__name__)

load_dotenv()
COHERE_API_KEY = os.getenv("CO_API_KEY")

# print("Loaded Key:", os.getenv("CO_API_KEY"))

# Cohere API key
cohere_client = cohere.Client(COHERE_API_KEY)

# --- Helper functions ---
def extract_video_id(url):
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    return None

def fetch_transcript(video_url):
    try:
        video_id = extract_video_id(video_url)
        print("Extracted video ID:", video_id)

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
        except NoTranscriptFound:
            print("English transcript not found, trying fallback options...")
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en', 'ta', 'hi', 'auto'])
            transcript = transcript.fetch()
        except TranscriptsDisabled:
            print("Transcripts are disabled for this video.")
            return None

        full_text = " ".join([item["text"] for item in transcript])
        return full_text

    except Exception as e:
        print("Transcript fetch failed:", e)
        return None

# --- Text chunking utility ---
def chunk_text(text, max_chars=4000):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        current_length += len(word) + 1
        if current_length < max_chars:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
            current_length = len(word) + 1

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks

# --- Summarization handler ---
def summarize_text(text):
    try:
        if len(text) < 4000:
            print("Using single request for short transcript")
            response = cohere_client.summarize(
                text=text,
                length="medium",
                format="paragraph",
                model="command",
            )
            return response.summary
        else:
            print("Transcript too long. Chunking and summarizing in parts...")
            chunks = chunk_text(text)
            partial_summaries = []

            for i, chunk in enumerate(chunks):
                print(f"🔹 Summarizing chunk {i + 1}/{len(chunks)}")
                response = cohere_client.summarize(
                    text=chunk,
                    length="medium",
                    format="paragraph",
                    model="command",
                )
                partial_summaries.append(response.summary)
                time.sleep(12)  # Handle rate limit for Trial key

            final_summary = "\n\n".join(partial_summaries)
            return final_summary

    except Exception as e:
        print("Summarization failed:", e)
        return "Summary failed. Check your API key or input."

# --- Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    transcript_preview = None
    error = None

    if request.method == "POST":
        video_url = request.form.get("videoUrl")
        print("Received video URL:", video_url)

        transcript = fetch_transcript(video_url)
        print("Transcript (first 200 chars):", transcript[:200] if transcript else "None")

        if transcript:
            transcript_preview = transcript[:1000]
            summary = summarize_text(transcript)
        else:
            error = "Could not fetch transcript. Make sure the video has captions and is publicly accessible."

    return render_template("index.html", summary=summary, transcript=transcript_preview, error=error)

# --- Main ---
if __name__ == "__main__":
    app.run(debug=True)
