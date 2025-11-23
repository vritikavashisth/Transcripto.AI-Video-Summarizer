import os
from faster_whisper import WhisperModel
from transformers import pipeline

# ---------------------------------------------------------
# 🔥 LOAD MODELS (Only runs once — fastest performance)
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
    )

    for seg in segments:
        segments_text.append(seg.text)

    return " ".join(segments_text)


# ---------------------------------------------------------
# 🔥 SUMMARIZE TEXT  (FIXED: Chunk size reduced)
# ---------------------------------------------------------
def summarize_text(text, max_chunk=400):
    chunks = []
    words = text.split()

    current = []
    count = 0

    for w in words:
        current.append(w)
        count += 1

        # 400 words → safe for BART (fits in 1024 token limit)
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
# 🔥 MAIN FUNCTION (returns BOTH transcript & summary)
# ---------------------------------------------------------
def video_to_summary(video_path):
    print("Processing video...")

    transcript = transcribe_audio(video_path)
    print("\nTRANSCRIPT COMPLETED\n")

    summary = summarize_text(transcript)
    print("\nSUMMARY COMPLETED\n")

    return transcript, summary
