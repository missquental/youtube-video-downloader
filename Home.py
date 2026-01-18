import streamlit as st
import json
from metaai_api import MetaAI

# Judul Aplikasi
st.set_page_config(page_title="MetaAI Video Generator", layout="centered")
st.title("🎥 MetaAI Video Generator with Streamlit")
st.markdown("---")

# Sidebar untuk input cookies
st.sidebar.header("🔐 Masukkan Cookies Anda")
datr = st.sidebar.text_input("datr", "")
wd = st.sidebar.text_input("wd", "1536x443")
abra_sess = st.sidebar.text_input("abra_sess", "")
dpr = st.sidebar.text_input("dpr", "1.25")

# Validasi cookies
if datr and abra_sess:
    cookies = {
        "datr": datr,
        "wd": wd,
        "abra_sess": abra_sess,
        "dpr": dpr
    }
else:
    st.warning("⚠️ Silakan masukkan nilai `datr` dan `abra_sess` terlebih dahulu.")
    st.stop()

# Inisialisasi MetaAI satu kali
@st.cache_resource
def init_meta_ai(cookies):
    return MetaAI(cookies=cookies)

ai = init_meta_ai(cookies)

# Prompt utama
st.subheader("✍️ Masukkan Prompt Video Anda")
prompt = st.text_area("Prompt", placeholder="Contoh: Generate a realistic video of a beautiful sunset over the ocean")

if st.button("🎬 Buat Video"):
    if not prompt.strip():
        st.error("❗ Harap masukkan prompt.")
    else:
        with st.spinner("Sedang membuat video... mohon tunggu beberapa saat."):
            try:
                result = ai.generate_video(prompt)
                
                if result["success"]:
                    st.success("✅ Video berhasil dibuat!")
                    st.write(f"- **Conversation ID**: `{result['conversation_id']}`")
                    
                    st.write("### 🎞️ Hasil Video")
                    for i, url in enumerate(result['video_urls'], 1):
                        st.video(url)

                    # Simpan ke file JSON
                    filename = f"video_{result['conversation_id']}.json"
                    with open(filename, 'w') as f:
                        json.dump(result, f, indent=2)
                    st.download_button(
                        label="💾 Unduh Hasil (JSON)",
                        data=open(filename, "rb"),
                        file_name=filename,
                        mime="application/json"
                    )
                else:
                    st.error("❌ Gagal membuat video.")
                    if "error" in result:
                        st.write(f"Error: {result['error']}")
            except Exception as e:
                st.exception(f"Terjadi kesalahan: {str(e)}")

# Contoh Penggunaan Lanjutan
with st.expander("🔍 Lihat Contoh Prompt"):
    st.code("""
Beberapa ide prompt:
1. Generate a realistic video of a beautiful sunset over the ocean
2. Generate a video of a cat playing piano
3. Generate a video of dolphins swimming in the ocean
4. Generate a video of fireworks at night
""")

# Footer info
st.markdown("---")
st.caption("💡 Dibuat dengan ❤️ menggunakan Streamlit & MetaAI API")
