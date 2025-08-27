from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import cohere
import os

load_dotenv()

COHERE_API_KEY = os.getenv("API_KEY")


# import re
import urllib.parse
def get_id(url):
    try:
        parsed_url = urllib.parse.urlparse(url)
        if "youtu.be" in parsed_url.netloc:
            return parsed_url.path.strip("/")
        elif "youtube.com" in parsed_url.netloc:
            query_params = urllib.parse.parse_qs(parsed_url.query)
            return query_params.get("v", [None])[0]
        return None
    except Exception as e:
        print("URL parsing error:", e)
        return None


def get_transcript(url):
    video_id = get_id(url)
    if not video_id:
        raise ValueError("INVALID YOUTUBE URL")

    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    full_text = " ".join([entry['text'] for entry in transcript_list])
    return full_text


def summarize_with_cohere(text):
    co = cohere.Client(COHERE_API_KEY)
    response = co.summarize(
        text=text,
        model="command-r-plus",
        length="medium",
        format="paragraph"
    )
    return response.summary.strip()


if __name__ == "__main__":
    try:
        url = input("ENTER YOUTUBE URL: ").strip()
        transcript = get_transcript(url)
        print("\nTRANSCRIPT PREVIEW:\n")
        print(transcript[:1000])

        choice = input("\n DO YOU WANT TO SUMMARIZE IT? (y/n): ").lower()
        if choice == 'y':
            print("\nSummarizing with Cohere...")
            summary = summarize_with_cohere(transcript)
            print("\nSUMMARY:\n")
            print(summary)

            save = input("\n Save summary to file? (y/n): ").lower()
            if save == 'y':
                with open("yt_summary.txt", "w", encoding="utf-8") as f:
                    f.write(summary)
                print(" Saved to yt_summary.txt")
    except Exception as error:
        print("ERROR:", error)

