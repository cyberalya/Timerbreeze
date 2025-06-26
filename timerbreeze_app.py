import streamlit as st
import time
import random
from streamlit_option_menu import option_menu

st.set_page_config(page_title="TimerBreeze 🍃", layout="wide")

# Inisialisasi state
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "music_files" not in st.session_state:
    st.session_state.music_files = []
if "current_song" not in st.session_state:
    st.session_state.current_song = None

# Quotes motivasi
quotes = [
    "🌟 Kamu hebat sudah sampai sejauh ini!",
    "💫 Satu sesi kecil adalah langkah besar untuk impianmu",
    "😌 Fokus sekarang, santai nanti~",
    "💪 Ayo selesaikan satu hal hari ini!",
    "🧠 Mimpi besar dimulai dari fokus kecil"
]

# Background Custom
bg_choice = st.sidebar.selectbox("🎨 Pilih Background", [
    "Default (Putih)", "Langit Senja", "Pantai", "Coding Vibes", "Upload Gambar Sendiri"
])

if bg_choice == "Langit Senja":
    bg_url = "https://i.ibb.co/z6f3m5g/sunset-sky.jpg"
elif bg_choice == "Pantai":
    bg_url = "https://i.ibb.co/W2zjMDR/beach.jpg"
elif bg_choice == "Coding Vibes":
    bg_url = "https://i.ibb.co/fCqHmhg/code.jpg"
elif bg_choice == "Upload Gambar Sendiri":
    bg_file = st.sidebar.file_uploader("Upload Background", type=["jpg", "jpeg", "png"])
    if bg_file:
        bg_url = f"data:image/png;base64,{base64.b64encode(bg_file.read()).decode()}"
    else:
        bg_url = ""
else:
    bg_url = ""

if bg_url:
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url('{bg_url}');
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

# Navigasi
selected = option_menu(None, ["🕒 Timer", "📝 To-Do", "🎵 Musik"],
    icons=["hourglass-split", "list-check", "music-note"], orientation="horizontal")

# Fungsi Timer
def countdown(minutes):
    total = int(minutes * 60)
    bar = st.progress(0)
    for i in range(total):
        mins, secs = divmod(total - i, 60)
        st.metric("⏳ Waktu Tersisa", f"{mins:02d}:{secs:02d}")
        bar.progress((i + 1) / total)
        time.sleep(1)
    st.success("🎉 Waktu habis, good job!")
    st.balloons()
    st.info(random.choice(quotes))

# Halaman Timer
if selected == "🕒 Timer":
    st.title("🍃 Fokus & Istirahat")
    fokus = st.slider("Durasi Fokus (menit)", 5, 60, 25)
    istirahat = st.slider("Durasi Istirahat (menit)", 1, 30, 5)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Mulai Fokus"):
            countdown(fokus)
    with col2:
        if st.button("☕ Istirahat"):
            countdown(istirahat)

# Halaman To-Do
elif selected == "📝 To-Do":
    st.title("📝 Rencana Hari Ini")
    task = st.text_input("Tambah kegiatan:")
    if st.button("➕ Tambahkan"):
        if task:
            st.session_state.tasks.append(task)
    for i, item in enumerate(st.session_state.tasks):
        st.write(f"✅ {item}")

# Halaman Musik
elif selected == "🎵 Musik":
    st.title("🎶 Playlist Kamu")

    uploaded_files = st.file_uploader("Upload Lagu (MP3)", type=["mp3"], accept_multiple_files=True)
    if uploaded_files:
        for f in uploaded_files:
            if f not in st.session_state.music_files:
                st.session_state.music_files.append(f)

    if st.session_state.music_files:
        for i, music in enumerate(st.session_state.music_files):
            col1, col2 = st.columns([6, 1])
            with col1:
                st.write(f"🎵 {music.name}")
            with col2:
                if st.button(f"▶️ Putar", key=f"play-{i}"):
                    st.session_state.current_song = music

    if st.session_state.current_song:
        st.audio(st.session_state.current_song, format='audio/mp3')
        st.write(f"Sedang memutar: **{st.session_state.current_song.name}**")

    st.markdown("---")
    st.subheader("💡 Catatan:")
    st.info("Kontrol Spotify & YouTube masih dalam pengembangan. Untuk sekarang, upload dan putar musik langsung dari file.")
