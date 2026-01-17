import streamlit as st

st.set_page_config(page_title="YouTube Video Downloader", page_icon="🎵", layout="wide")

# Home page content
st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: #FF6B6B; font-size: 3rem; margin-bottom: 1rem;">🎵 YouTube Video Downloader</h1>
        <h2 style="color: #4ECDC4; font-size: 1.5rem; margin-bottom: 2rem;">Welcome!</h2>
        <p style="font-size: 1.2rem; color: #666; max-width: 600px; margin: 0 auto;">
            With this application, you can easily download YouTube videos and playlists. 
            Use the left menu to navigate to the desired page.
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Feature cards
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
        <div style="border: 2px solid #FF6B6B; border-radius: 10px; padding: 2rem; text-align: center; height: 300px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">▶️</div>
            <h3 style="color: #FF6B6B; margin-bottom: 1rem;">Single Video Downloader</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">
                Download a single YouTube video. Includes video preview, quality selection, and advanced download features.
            </p>
            <div style="background: #FF6B6B; color: white; padding: 0.5rem 1rem; border-radius: 5px; display: inline-block;">
                Go to the "▶️ Youtube Downloader" page from the left menu
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div style="border: 2px solid #4ECDC4; border-radius: 10px; padding: 2rem; text-align: center; height: 300px; display: flex; flex-direction: column; justify-content: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎶</div>
            <h3 style="color: #4ECDC4; margin-bottom: 1rem;">Batch Video Downloader</h3>
            <p style="color: #666; margin-bottom: 1.5rem;">
                Process multiple video URLs at once. Includes batch downloading and progress tracking.
            </p>
            <div style="background: #4ECDC4; color: white; padding: 0.5rem 1rem; border-radius: 5px; display: inline-block;">
                Go to the "🎶 Playlist Downloader" page from the left menu
            </div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Feature list
st.markdown("### ✨ Application Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **📹 Video Downloading:**
    - Download videos in MP4 format
    - Quality options (720p, 480p, 360p)
    - Video preview and details
    - Download progress indicator
    
    **🎵 Audio Downloading:**
    - Extract audio in MP3 format
    - High-quality audio (192 kbps)
    - FFmpeg integration
    """)

with col2:
    st.markdown("""
    **🔧 Advanced Features:**
    - Reliable downloading powered by yt-dlp
    - Error handling and reporting
    - Safe filename generation
    - Batch download support
    
    **📁 File Management:**
    - Automatic Downloads folder
    - File size display
    - List of downloaded files
    """)

st.divider()

# Usage instructions
with st.expander("📖 How to Use?"):
    st.markdown("""
    ### Step-by-Step Guide:
    
    1. **Select a page from the left menu:**
       - **▶️ Youtube Downloader:** To download a single video
       - **🎶 Playlist Downloader:** To download multiple videos
    
    2. **Choose format and quality:**
       - Select MP4 for video or MP3 for audio
       - Choose your desired video quality
    
    3. **Enter URLs:**
       - Paste YouTube video links
       - For batch downloading, enter one URL per line
    
    4. **Start the download process:**
       - Click the "Download" button
       - Wait for the process to complete
    
    ### 💡 Tips:
    - FFmpeg is required for MP3 downloading
    - Large files may take longer
    - Ensure your internet connection is stable
    """)

# Footer
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: #666; border-top: 1px solid #eee; margin-top: 2rem;">
        <p>🚀 Powered by <strong>yt-dlp</strong> | 
        📁 Files are saved in the <code>Downloads</code> folder</p>
    </div>
""", unsafe_allow_html=True)
