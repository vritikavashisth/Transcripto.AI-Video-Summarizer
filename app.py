import streamlit as st
import os
import importlib
import sys
import traceback


# -------------------- CUSTOM PURPLE THEME CSS --------------------
def load_css():
    st.markdown("""
        <style>

        /* Background */
        .stApp {
            background: linear-gradient(135deg, #0f0f1f, #1a1a2e);
            color: #e2e2e2;
        }

        /* Center container */
        .main-container {
            text-align: center;
            margin-top: 60px;
        }

        /* Title gradient */
        .title-text {
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(270deg, #7aa2ff, #c084fc, #8ef0ff, #b38bff);
            background-size: 800% 800%;
            animation: gradientFlow 7s ease infinite;
            -webkit-background-clip: text;
            color: transparent;
            white-space: nowrap;
        }

        @keyframes gradientFlow {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .sub-text {
            font-size: 21px;
            opacity: 0.85;
            margin-top: -8px;
            margin-bottom: 40px;
        }

        /* Hide empty uploader label */
        .stFileUploader label {
            display: none !important;
        }

        /* Custom uploader box */
        .stFileUploader > div:nth-child(1) {
            border: 2px dashed rgba(255, 255, 255, 0.15) !important;
            padding: 25px !important;
            border-radius: 16px !important;
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(8px) !important;
            -webkit-backdrop-filter: blur(8px) !important;
        }

        /* Upload button */
        .stFileUploader button {
            background: linear-gradient(90deg, #7f5fff, #a66bff) !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 10px 22px !important;
            border: none !important;
            font-weight: 600 !important;
        }

        /* Download button */
        .download-custom button {
            background: linear-gradient(90deg, #7f5fff, #a66bff) !important;
            color: white !important;
            border-radius: 12px !important;
            padding: 10px 22px !important;
            border: none !important;
            font-weight: 600 !important;
        }

        .download-custom button:hover {
            background: linear-gradient(135deg, #7a6cff, #c18cff) !important;
        }

        </style>
    """, unsafe_allow_html=True)



# -------------------- MAIN APP --------------------
def main():

    st.set_page_config(page_title="Transcripto.AI", page_icon="✨", layout="centered")
    load_css()

    # Title + Subtitle
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="title-text">Transcripto.AI - Video Summarizer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Upload any video to get AI-powered Transcript & Summary instantly.✨</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # --- Import main.py functions safely ---
    try:
        project_root = os.getcwd()
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        import main as main_module
        importlib.reload(main_module)

        video_to_summary = main_module.video_to_summary

    except Exception:
        st.error("Failed to load main.py — check console for details.")
        st.text(traceback.format_exc())
        return

    # ---- File Upload ----
    uploaded_file = st.file_uploader(
        "Upload Video",
        type=["mp4", "avi", "mov", "mkv", "mpeg4"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        temp_video = "temp_video.mp4"

        with open(temp_video, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("⏳ Processing video… Please wait..."):
            try:
                transcript, summary = video_to_summary(temp_video)

            except Exception:
                st.error("An error occurred during processing:")
                st.text(traceback.format_exc())
                return
            finally:
                try:
                    if os.path.exists(temp_video):
                        os.remove(temp_video)
                except:
                    pass

        # ------------------ OUTPUT SECTION ------------------

        st.subheader("📄 Transcript")
        st.write(transcript)

        # ---- DOWNLOAD TRANSCRIPT ----
        st.markdown('<div class="download-custom">', unsafe_allow_html=True)
        st.download_button(
            "Download Transcript",
            transcript,
            file_name="transcript.txt",
            mime="text/plain",
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("📝 Summary")
        st.write(summary)

        # ---- DOWNLOAD SUMMARY ----
        st.markdown('<div class="download-custom">', unsafe_allow_html=True)
        st.download_button(
            "Download Summary",
            summary,
            file_name="summary.txt",
            mime="text/plain",
        )
        st.markdown('</div>', unsafe_allow_html=True)



if __name__ == "__main__":
    main()
