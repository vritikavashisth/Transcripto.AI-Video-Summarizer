import os
<<<<<<< HEAD
import subprocess
from faster_whisper import WhisperModel
from transformers import pipeline


# ---------------------------------------------------------
# 🔥 LOAD MODELS
=======
from faster_whisper import WhisperModel
from transformers import pipeline

# ---------------------------------------------------------
# 🔥 LOAD MODELS (Only runs once — fastest performance)
>>>>>>> e20f9f3705378aceec5a685a3cbb71ba02556f41
# ---------------------------------------------------------

whisper_model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

summarizer = pipeline(
    "summarization",
    model="sshleifer/distilbart-cnn-12-6",
    device=-1
)

<<<<<<< HEAD

# ---------------------------------------------------------
# 🔥 EXTRACT AUDIO FROM VIDEO (Fixes Memory Error)
# ---------------------------------------------------------
def extract_audio(video_path, audio_path="temp_audio.wav"):
    if os.path.exists(audio_path):
        os.remove(audio_path)

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",          # <--- LOW SAMPLE RATE (SAFE)
        audio_path
    ]

    subprocess.call(cmd)
    return audio_path


# ---------------------------------------------------------
# 🔥 TRANSCRIBE AUDIO SAFELY
# ---------------------------------------------------------
def transcribe_audio(video_path, chunk_size=30):
    audio_path = extract_audio(video_path)

    segments_text = []

    segments, _ = whisper_model.transcribe(
        audio_path,
        beam_size=1,
        best_of=1,
        vad_filter=True,
        chunk_length=chunk_size    # <--- MEMORY FIX
=======
# ---------------------------------------------------------
# 🔥 TRANSCRIBE VIDEO
# ---------------------------------------------------------
def transcribe_audio(video_path, chunk_size=30):
    segments_text = []

    segments, _ = whisper_model.transcribe(
        video_path,
        beam_size=1,
        best_of=1,
        vad_filter=True,
>>>>>>> e20f9f3705378aceec5a685a3cbb71ba02556f41
    )

    for seg in segments:
        segments_text.append(seg.text)

    return " ".join(segments_text)


# ---------------------------------------------------------
<<<<<<< HEAD
# 🔥 SUMMARIZE TEXT
=======
# 🔥 SUMMARIZE TEXT  (FIXED: Chunk size reduced)
>>>>>>> e20f9f3705378aceec5a685a3cbb71ba02556f41
# ---------------------------------------------------------
def summarize_text(text, max_chunk=400):
    chunks = []
    words = text.split()

    current = []
    count = 0

    for w in words:
        current.append(w)
        count += 1

<<<<<<< HEAD
=======
        # 400 words → safe for BART (fits in 1024 token limit)
>>>>>>> e20f9f3705378aceec5a685a3cbb71ba02556f41
        if count >= max_chunk:
            chunks.append(" ".join(current))
            current = []
            count = 0

    if current:
        chunks.append(" ".join(current))

    final_summary = ""

    for chunk in chunks:
        summary = summarizer(
            chunk,
            max_length=150,
            min_length=40,
            do_sample=False
        )[0]["summary_text"]

        final_summary += summary + " "

    return final_summary.strip()


# ---------------------------------------------------------
<<<<<<< HEAD
# 🔥 MAIN FUNCTION
=======
# 🔥 MAIN FUNCTION (returns BOTH transcript & summary)
>>>>>>> e20f9f3705378aceec5a685a3cbb71ba02556f41
# ---------------------------------------------------------
def video_to_summary(video_path):
    print("Processing video...")

    transcript = transcribe_audio(video_path)
    print("\nTRANSCRIPT COMPLETED\n")

    summary = summarize_text(transcript)
    print("\nSUMMARY COMPLETED\n")

    return transcript, summary
