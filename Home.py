# streamlit_app.py
import streamlit as st
import os
import re
from io import BytesIO
import tempfile
import time

# Install required packages
os.system("pip install -q yt-dlp pytube moviepy")

st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎵",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #ff4b4b;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    .subheader {
        text-align: center;
        color: #1e88e5;
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3rem;
        font-weight: bold;
    }
    .stSelectbox>div>div {
        border-radius: 10px;
    }
    .success-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #e8f5e9;
        border: 1px solid #4caf50;
        margin: 1rem 0;
    }
    .error-box {
        padding: 1rem;
        border-radius: 10px;
        background-color: #ffebee;
        border: 1px solid #f44336;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def clean_filename(filename):
    """Clean filename from illegal characters"""
    return re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)[:100]

def download_mp3_ytdlp(url):
    """Download MP3 using yt-dlp"""
    try:
        import yt_dlp
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = clean_filename(info.get('title', 'unknown'))
            mp3_file = os.path.join(temp_dir, f"{title}.mp3")
            
            # Read file content
            with open(mp3_file, 'rb') as f:
                mp3_bytes = f.read()
            
            return mp3_bytes, f"{title}.mp3"
            
    except Exception as e:
        st.error(f"Error downloading MP3: {str(e)}")
        return None, None

def download_mp4_ytdlp(url, quality='best'):
    """Download MP4 using yt-dlp"""
    try:
        import yt_dlp
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Quality mapping
        quality_formats = {
            '360p': 'best[height<=360][ext=mp4]',
            '480p': 'best[height<=480][ext=mp4]',
            '720p': 'best[height<=720][ext=mp4]',
            '1080p': 'best[height<=1080][ext=mp4]',
            'best': 'best[ext=mp4]'
        }
        
        ydl_opts = {
            'format': quality_formats.get(quality, 'best[ext=mp4]'),
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = clean_filename(info.get('title', 'unknown'))
            ext = info.get('ext', 'mp4')
            mp4_file = os.path.join(temp_dir, f"{title}.{ext}")
            
            # Read file content
            with open(mp4_file, 'rb') as f:
                mp4_bytes = f.read()
            
            return mp4_bytes, f"{title}.{ext}"
            
    except Exception as e:
        st.error(f"Error downloading MP4: {str(e)}")
        return None, None

def get_video_info(url):
    """Get video information"""
    try:
        import yt_dlp
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader', 'Unknown'),
                'view_count': info.get('view_count', 0)
            }
    except:
        return None

def format_duration(seconds):
    """Format duration"""
    if seconds:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    return "Unknown"

def main():
    st.markdown('<h1 class="main-header">🎵 YouTube Downloader</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subheader">Download MP3 & MP4 Gratis Tanpa Iklan</h3>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "⬇️ Download", "❓ Help"])
    
    with tab1:
        st.subheader("Selamat Datang!")
        st.write("""
        Aplikasi ini memungkinkan Anda untuk:
        - 🔊 Download audio YouTube sebagai MP3
        - 📹 Download video YouTube sebagai MP4
        - 🚫 Tanpa iklan dan gratis sepenuhnya
        - ⚡ Proses cepat dan mudah
        
        **Cara menggunakan:**
        1. Masuk ke tab "Download"
        2. Paste URL YouTube
        3. Pilih format (MP3/MP4) dan kualitas
        4. Klik tombol download
        5. File akan otomatis terdownload ke komputer Anda
        """)
        
        st.info("💡 Tips: Gunakan URL YouTube yang valid dan pastikan video tersedia untuk publik.")
    
    with tab2:
        st.subheader("Download YouTube Video/Audio")
        
        # URL input
        url = st.text_input("🔗 Masukkan URL YouTube:", placeholder="https://www.youtube.com/watch?v=...")
        
        if url:
            # Show video info
            with st.spinner("Mengambil informasi video..."):
                info = get_video_info(url)
                
            if info:
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    if info['thumbnail']:
                        st.image(info['thumbnail'], width=200)
                
                with col2:
                    st.write(f"**📹 Judul:** {info['title']}")
                    st.write(f"**⏱️ Durasi:** {format_duration(info['duration'])}")
                    st.write(f"**👤 Channel:** {info['uploader']}")
                    st.write(f"**👁️ Views:** {info['view_count']:,}" if info['view_count'] else "**👁️ Views:** Unknown")
            
            # Format selection
            st.divider()
            format_choice = st.radio("🎯 Pilih Format Download:", ["🎵 MP3 (Audio)", "📹 MP4 (Video)"])
            
            if format_choice == "🎵 MP3 (Audio)":
                if st.button("📥 Download MP3", type="primary", use_container_width=True):
                    with st.spinner("🔄 Sedang memproses download MP3..."):
                        mp3_bytes, filename = download_mp3_ytdlp(url)
                        
                        if mp3_bytes and filename:
                            st.success("✅ Download berhasil!")
                            st.balloons()
                            
                            # Download button
                            st.download_button(
                                label="💾 Simpan File MP3",
                                data=mp3_bytes,
                                file_name=filename,
                                mime="audio/mpeg",
                                use_container_width=True
                            )
                        else:
                            st.error("❌ Download gagal! Pastikan URL valid dan coba lagi.")
            
            else:  # MP4
                quality = st.selectbox("🎯 Pilih Kualitas Video:", 
                                     [".best", "1080p", "720p", "480p", "360p"])
                
                if st.button("📥 Download MP4", type="primary", use_container_width=True):
                    with st.spinner("🔄 Sedang memproses download MP4..."):
                        mp4_bytes, filename = download_mp4_ytdlp(url, quality.replace(".best", "best"))
                        
                        if mp4_bytes and filename:
                            st.success("✅ Download berhasil!")
                            st.balloons()
                            
                            # Download button
                            st.download_button(
                                label="💾 Simpan File MP4",
                                data=mp4_bytes,
                                file_name=filename,
                                mime="video/mp4",
                                use_container_width=True
                            )
                        else:
                            st.error("❌ Download gagal! Pastikan URL valid dan coba lagi.")
        
        else:
            st.info("👆 Masukkan URL YouTube di atas untuk mulai download")
    
    with tab3:
        st.subheader("❓ Bantuan & FAQ")
        
        st.write("**Q: Apakah aplikasi ini gratis?**")
        st.write("A: Ya, 100% gratis tanpa biaya tersembunyi.")
        
        st.write("**Q: Apakah aman digunakan?**")
        st.write("A: Ya, semua proses dilakukan di server aman dan file dihapus setelah download.")
        
        st.write("**Q: Format apa yang didukung?**")
        st.write("A: MP3 (audio) dan MP4 (video) dengan berbagai kualitas.")
        
        st.write("**Q: Batas ukuran file?**")
        st.write("A: Tergantung platform Streamlit, umumnya hingga 200MB.")
        
        st.write("**Q: Video apa saja yang bisa didownload?**")
        st.write("A: Video yang tersedia untuk publik dan tidak melanggar hak cipta.")
        
        st.divider()
        st.write("📝 **Disclaimer:**")
        st.warning("""
        - Gunakan aplikasi ini sesuai hak cipta dan ketentuan YouTube
        - Kami tidak bertanggung jawab atas penyalahgunaan
        - Semua file dihapus setelah proses download selesai
        """)

if __name__ == "__main__":
    main()
