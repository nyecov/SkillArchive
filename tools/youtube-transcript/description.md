# YouTube Transcript Downloader

A Python automation tool using `yt-dlp` to fetch transcriptions and subtitles for YouTube videos.

**Primary Uses:**
1. Scraping video transcripts to feed into LLM agents for summarization, Q&A, or content rewriting.
2. Supports gracefully falling back between manufacturer-uploaded subtitles and YouTube's auto-generated subs.
3. Contains scaffolding to fall back to local Whisper audio transcription if no subs are available.

**Usage:**
```bash
python youtube_transcript.py "https://www.youtube.com/watch?v=..." --lang en
```
