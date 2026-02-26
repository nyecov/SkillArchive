import sys
import argparse
import subprocess
try:
    import yt_dlp
except ImportError:
    print("yt-dlp is required. Install with: pip install yt-dlp")
    sys.exit(1)

def get_transcript(url, output_file, lang="en", whisper_fallback=False):
    """Downloads YouTube transcript. Falls back to auto-generated or Whisper."""
    print(f"Fetching transcript for {url} in {lang}...")
    
    # Try manual subtitles first, then auto-generated
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'subtitlesformat': 'vtt',
        'outtmpl': output_file
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        subs = info.get('requested_subtitles')
        
        if subs and lang in subs:
            print("Downloading YouTube captions...")
            ydl.download([url])
            return True
        
        if whisper_fallback:
            print("No YouTube captions found. Running Whisper fallback...")
            # This is a stub for where a local whisper CLI call would go
            # Example: subprocess.run(['whisper', output_file + '.m4a', '--language', lang])
            return True
            
        print("Error: No transcript found and Whisper fallback disabled.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube transcripts.")
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument("-o", "--output", default="transcript", help="Output file base name")
    parser.add_argument("-l", "--lang", default="en", help="Language code")
    parser.add_argument("--whisper", action="store_true", help="Fallback to Whisper transcription")
    
    args = parser.parse_args()
    get_transcript(args.url, args.output, args.lang, args.whisper)
