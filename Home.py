# streamlit_app.py
import streamlit as st
import os
import re
import tempfile
import time

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
        color: #FF4B91;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .subheader {
        text-align: center;
        color: #1E90FF;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stButton>button {
        background-color: #FF4B91;
        color: white;
        border-radius: 15px;
        height: 3.5rem;
        font-weight: bold;
        font-size: 1.1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #FF1493;
        transform: scale(1.02);
    }
    .success-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    .error-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin: 1rem 0;
        text-align: center;
    }
    .info-card {
        background-color: #f8f9fa;
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #1E90FF;
    }
</style>
""", unsafe_allow_html=True)

def clean_filename(filename):
    """Clean filename from illegal characters"""
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '_', filename)
    return cleaned[:100]  # Limit length

def download_media_ytdlp(url, media_type="mp3", quality="best"):
    """Download media using yt-dlp with proper configuration"""
    try:
        import yt_dlp
        import io
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        if media_type == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': False,
                'extract_audio': True,
            }
        else:  # mp4
            # Quality format mapping
            quality_map = {
                '360p': 'bv*[height<=360][ext=mp4]+ba[ext=m4a]/b[height<=360][ext=mp4] / bv*[height<=360]+ba/b[height<=360]',
                '480p': 'bv*[height<=480][ext=mp4]+ba[ext=m4a]/b[height<=480][ext=mp4] / bv*[height<=480]+ba/b[height<=480]',
                '720p': 'bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4] / bv*[height<=720]+ba/b[height<=720]',
                '1080p': 'bv*[height<=1080][ext=mp4]+ba[ext=m4a]/b[height<=1080][ext=mp4] / bv*[height<=1080]+ba/b[height<=1080]',
                'best': 'bv*+ba/b'
            }
            
            ydl_opts = {
                'format': quality_map.get(quality, 'bv*+ba/b'),
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': False,
            }
        
        # Download with yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info first
            info = ydl.extract_info(url, download=False)
            title = clean_filename(info.get('title', 'download'))
            
            # Now download the actual file
            ydl.download([url])
            
            # Find the downloaded file
            downloaded_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    downloaded_files.append(os.path.join(root, file))
            
            if downloaded_files:
                # Get the most recent file
                latest_file = max(downloaded_files, key=os.path.getctime)
                
                # Read file content
                with open(latest_file, 'rb') as f:
                    file_content = f.read()
                
                # Determine extension
                if media_type == "mp3":
                    filename = f"{title}.mp3"
                else:
                    filename = f"{title}.{latest_file.split('.')[-1]}"
                
                return file_content, filename
        
        return None, None
        
    except Exception as e:
        st.error(f"Detailed error: {str(e)}")
        return None, None

def get_video_info(url):
    """Get video information safely"""
    try:
        import yt_dlp
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'title': info.get('title', 'Unknown Title'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', 'https://i.ytimg.com/vi/default.jpg'),
                'uploader': info.get('uploader', 'Unknown Uploader'),
                'view_count': info.get('view_count', 0),
                'upload_date': info.get('upload_date', 'Unknown Date')
            }
    except Exception as e:
        st.warning(f"Tidak dapat mengambil info video: {str(e)}")
        return None

def format_duration(seconds):
    """Format duration in HH:MM:SS or MM:SS"""
    if not seconds:
        return "Unknown"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def main():
    # Header
    st.markdown('<h1 class="main-header">🎵 YouTube Downloader Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Download MP3 & MP4 Secara Gratis & Tanpa Iklan</p>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🏠 Home", "⬇️ Download", "❓ FAQ"])
    
    with tab1:
        st.subheader("✨ Selamat Datang!")
        st.markdown("""
        <div class="info-card">
        💡 <b>Aplikasi ini memungkinkan Anda untuk:</b><br>
        • 🔊 Download audio YouTube sebagai MP3<br>
        • 📹 Download video YouTube sebagai MP4<br>
        • ⚡ Proses cepat dan mudah<br>
        • 🚫 Tanpa iklan dan 100% gratis<br>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🚀 Cara Menggunakan:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**1️⃣ Copy URL**")
            st.info("Salin URL video YouTube")
        
        with col2:
            st.markdown("**2️⃣ Pilih Format**")
            st.info("Pilih MP3 atau MP4")
        
        with col3:
            st.markdown("**3️⃣ Download**")
            st.info("Klik tombol download")
    
    with tab2:
        st.subheader("⬇️ Download Media")
        
        # URL input
        url = st.text_input("🔗 Masukkan URL YouTube:", 
                           placeholder="https://www.youtube.com/watch?v=...",
                           help="Paste URL lengkap dari video YouTube")
        
        if url and ("youtube.com" in url or "youtu.be" in url):
            # Show loading spinner while getting info
            with st.spinner("🔍 Mengambil informasi video..."):
                info = get_video_info(url)
            
            if info:
                # Display video info
                st.divider()
                st.subheader("📋 Informasi Video")
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.image(info['thumbnail'], width=200, caption="Thumbnail Video")
                
                with col2:
                    st.write(f"**📹 Judul:** {info['title']}")
                    st.write(f"**⏱️ Durasi:** {format_duration(info['duration'])}")
                    st.write(f"**👤 Channel:** {info['uploader']}")
                    if info['view_count']:
                        st.write(f"**👁️ Views:** {info['view_count']:,}")
                    st.write(f"**📅 Upload:** {info['upload_date']}")
                
                # Format selection
                st.divider()
                st.subheader("⚙️ Pilihan Download")
                
                format_choice = st.radio("🎯 Pilih Format:", 
                                       ["🎵 MP3 (Audio Only)", "📹 MP4 (Video)"],
                                       horizontal=True)
                
                if format_choice == "🎵 MP3 (Audio Only)":
                    # MP3 download
                    if st.button("📥 Download MP3", type="primary", use_container_width=True):
                        with st.spinner("🔄 Memproses download MP3... Mohon tunggu beberapa saat..."):
                            file_content, filename = download_media_ytdlp(url, "mp3")
                            
                            if file_content and filename:
                                st.markdown('<div class="success-box"><h3>✅ Download Berhasil!</h3></div>', unsafe_allow_html=True)
                                st.balloons()
                                
                                # Download button
                                st.download_button(
                                    label="💾 Simpan File MP3 Sekarang",
                                    data=file_content,
                                    file_name=filename,
                                    mime="audio/mpeg",
                                    use_container_width=True
                                )
                            else:
                                st.markdown('<div class="error-box"><h3>❌ Download Gagal!</h3><p>Pastikan URL valid dan video tersedia untuk publik.</p></div>', unsafe_allow_html=True)
                
                else:
                    # MP4 download with quality selection
                    quality = st.select_slider("🎯 Pilih Kualitas Video:", 
                                             options=["360p", "480p", "720p", "1080p", "best"],
                                             value="720p")
                    
                    if st.button("📥 Download MP4", type="primary", use_container_width=True):
                        with st.spinner("🔄 Memproses download MP4... Mohon tunggu beberapa saat..."):
                            file_content, filename = download_media_ytdlp(url, "mp4", quality)
                            
                            if file_content and filename:
                                st.markdown('<div class="success-box"><h3>✅ Download Berhasil!</h3></div>', unsafe_allow_html=True)
                                st.balloons()
                                
                                # Download button
                                st.download_button(
                                    label=f"💾 Simpan File MP4 ({quality})",
                                    data=file_content,
                                    file_name=filename,
                                    mime="video/mp4",
                                    use_container_width=True
                                )
                            else:
                                st.markdown('<div class="error-box"><h3>❌ Download Gagal!</h3><p>Pastikan URL valid dan video tersedia untuk publik.</p></div>', unsafe_allow_html=True)
            
            else:
                st.warning("⚠️ Tidak dapat mengambil informasi video. Pastikan URL valid!")
        
        elif url:
            st.error("❌ URL tidak valid! Pastikan URL dari YouTube.")
        
        else:
            st.info("👆 Masukkan URL YouTube di atas untuk mulai download")
            
            # Quick tips
            with st.expander("💡 Tips Cepat"):
                st.markdown("""
                • Gunakan URL dari browser address bar\n
                • Video harus tersedia untuk publik\n
                • Beberapa video mungkin memiliki batasan download\n
                • File besar mungkin memerlukan waktu lebih lama
                """)
    
    with tab3:
        st.subheader("❓ Pertanyaan Umum")
        
        with st.expander("💰 Apakah aplikasi ini benar-benar gratis?"):
            st.write("Ya! Aplikasi ini 100% gratis tanpa biaya tersembunyi.")
        
        with st.expander("🛡️ Apakah aman digunakan?"):
            st.write("Ya, semua proses dilakukan secara aman dan file dihapus setelah download.")
        
        with st.expander("📏 Batas ukuran file?"):
            st.write("Streamlit memiliki batas sekitar 200MB per file.")
        
        with st.expander("🎥 Video apa saja yang bisa didownload?"):
            st.write("Video yang tersedia untuk publik dan tidak memiliki batasan DRM.")
        
        with st.expander("⚡ Kenapa sometimes download gagal?"):
            st.write("Beberapa video memiliki proteksi khusus dari YouTube atau server sedang sibuk.")
        
        st.divider()
        st.subheader("⚠️ Disclaimer")
        st.warning("""
        Pengguna bertanggung jawab penuh atas penggunaan aplikasi ini.
        Pastikan menghormati hak cipta dan ketentuan penggunaan YouTube.
        Kami tidak menyimpan atau mendistribusikan konten yang didownload.
        """)

if __name__ == "__main__":
    main()
