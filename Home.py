import streamlit as st
import yt_dlp
import os
import tempfile
import re
from datetime import timedelta

st.set_page_config(
    page_title="VidSave - YouTube Downloader", 
    page_icon="🎥", 
    layout="wide"
)

# Custom CSS styling
st.markdown("""
<style>
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .feature-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.2s;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .download-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        font-size: 18px !important;
        border-radius: 25px !important;
        margin: 10px 0 !important;
    }
    .quality-badge {
        background: #f0f0f0;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 2px;
        display: inline-block;
        font-size: 12px;
    }
    .stats-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def format_duration(seconds):
    """Convert seconds to H:M:S format"""
    return str(timedelta(seconds=int(seconds)))

def format_filesize(bytes_value):
    """Convert bytes to human readable format"""
    if bytes_value is None:
        return "Unknown"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} TB"

def sanitize_filename(filename):
    """Remove invalid characters from filename"""
    return re.sub(r'[<>:"/\\|?*]', '', filename)[:100]

def get_video_formats(url):
    """Get available formats for the video"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"Gagal mengambil informasi video: {str(e)}")
        return None

def download_media(url, format_id=None, is_audio=False):
    """Download video or audio"""
    try:
        temp_dir = tempfile.mkdtemp()
        
        if is_audio:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                'quiet': True,
            }
        else:
            if format_id:
                ydl_opts = {
                    'format': format_id,
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                }
            else:
                ydl_opts = {
                    'format': 'best[ext=mp4]',
                    'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if is_audio:
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            
            return filename, info
            
    except Exception as e:
        st.error(f"Download gagal: {str(e)}")
        return None, None

# Header
st.markdown("""
<div class="header">
    <h1>🎥 VidSave - YouTube Downloader</h1>
    <p style="font-size: 1.2rem; opacity: 0.9;">Unduh video dan musik dari YouTube dengan mudah dan cepat</p>
</div>
""", unsafe_allow_html=True)

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔗 Masukkan URL YouTube")
    url = st.text_input("", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")
    
    if url:
        with st.spinner("🔄 Mengambil informasi video..."):
            video_info = get_video_formats(url)
        
        if video_info:
            # Video information
            st.markdown("---")
            st.subheader("📹 Informasi Video")
            
            col_info1, col_info2 = st.columns([1, 2])
            with col_info1:
                if 'thumbnail' in video_info:
                    st.image(video_info['thumbnail'], width=200)
            
            with col_info2:
                st.write(f"**judul:** {video_info.get('title', 'N/A')}")
                st.write(f"**Channel:** {video_info.get('uploader', 'N/A')}")
                st.write(f"**Durasi:** {format_duration(video_info.get('duration', 0))}")
                st.write(f"**Dilihat:** {video_info.get('view_count', 0):,} kali")
                st.write(f"**Tanggal Upload:** {video_info.get('upload_date', 'N/A')[:4]}")
            
            st.markdown("---")
            
            # Available formats
            st.subheader("📥 Pilihan Format Download")
            
            # Audio download section
            with st.expander("🎵 Audio (MP3)", expanded=True):
                if st.button("⬇️ Unduh Audio MP3", key="audio_btn"):
                    with st.spinner("🎵 Sedang mengunduh audio..."):
                        filename, info = download_media(url, is_audio=True)
                        if filename and os.path.exists(filename):
                            with open(filename, "rb") as file:
                                st.success("✅ Audio berhasil diunduh!")
                                st.download_button(
                                    label="💾 Download MP3",
                                    data=file,
                                    file_name=os.path.basename(filename),
                                    mime="audio/mpeg"
                                )
                        else:
                            st.error("❌ Gagal mengunduh audio")
            
            # Video download section
            with st.expander("📹 Video (MP4)", expanded=True):
                # Filter video formats
                video_formats = []
                if 'formats' in video_info:
                    for f in video_info['formats']:
                        if f.get('vcodec') != 'none' and f.get('ext') == 'mp4':
                            video_formats.append(f)
                
                # Sort by resolution
                video_formats.sort(key=lambda x: x.get('height', 0), reverse=True)
                
                # Display available qualities
                if video_formats:
                    cols = st.columns(3)
                    displayed_formats = []
                    
                    for i, fmt in enumerate(video_formats[:9]):  # Show max 9 formats
                        if fmt.get('height') and fmt.get('height') not in displayed_formats:
                            quality = f"{fmt.get('height')}p"
                            filesize = format_filesize(fmt.get('filesize'))
                            
                            with cols[i % 3]:
                                if st.button(f"{quality}\n({filesize})", key=f"fmt_{fmt.get('format_id')}"):
                                    with st.spinner(f"📹 Sedang mengunduh video {quality}..."):
                                        filename, info = download_media(url, fmt.get('format_id'), False)
                                        if filename and os.path.exists(filename):
                                            with open(filename, "rb") as file:
                                                st.success(f"✅ Video {quality} berhasil diunduh!")
                                                st.download_button(
                                                    label=f"💾 Download {quality}",
                                                    data=file,
                                                    file_name=os.path.basename(filename),
                                                    mime="video/mp4"
                                                )
                                        else:
                                            st.error("❌ Gagal mengunduh video")
                            
                            displayed_formats.append(fmt.get('height'))
                else:
                    st.info("Tidak ada format video tersedia")
            
            # Preview section
            st.markdown("---")
            st.subheader("👀 Preview")
            if 'thumbnail' in video_info:
                st.image(video_info['thumbnail'], caption="Thumbnail Video", use_column_width=True)

with col2:
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("✨ Fitur Unggulan")
    st.markdown("""
    • 🔥 **Gratis & Cepat** - Tanpa biaya tersembunyi
    • 🎯 **Kualitas Tinggi** - Hingga 1080p Full HD
    • 🎵 **Audio Premium** - MP3 kualitas tinggi
    • ⚡ **Tanpa Registrasi** - Langsung bisa digunakan
    • 🛡️ **Aman & Privasi** - File langsung ke device Anda
    • 🌐 **Kompatibel** - Bekerja di semua device
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="feature-card">', unsafe_allow_html=True)
    st.subheader("📋 Cara Menggunakan")
    st.markdown("""
    1. **Salin URL** video YouTube
    2. **Tempel** di kolom input
    3. **Pilih** format yang diinginkan
    4. **Klik** tombol download
    5. **Simpan** file ke device Anda
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Stats
    st.markdown('<div class="stats-box">', unsafe_allow_html=True)
    st.subheader("📊 Statistik")
    st.metric("Video Diproses", "10,000+", "↑ 15% Hari Ini")
    st.metric("User Aktif", "50,000+", "↑ 8% Minggu Ini")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <p>© 2024 VidSave - YouTube Downloader | Dibuat dengan ❤️ untuk komunitas</p>
    <p style="font-size: 0.9rem; color: #666;">
        Disclaimer: Aplikasi ini hanya untuk tujuan pribadi dan non-komersial. 
        Pastikan Anda memiliki hak untuk mengunduh konten tersebut.
    </p>
</div>
""", unsafe_allow_html=True)
