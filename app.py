import cv2
import streamlit as st
import numpy as np
import tempfile
from ultralytics import YOLO
import math
from PIL import Image
import torch
import pandas as pd
import os
from datetime import datetime

# Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="AI Gym Trainer - Max Res",
    layout="wide"
)

# --- KONFIGURASI HISTORY ---
HISTORY_FILE = "workout_history.csv"

def load_history():
    """Memuat data riwayat dari CSV."""
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame(columns=["Tanggal", "Waktu", "Jenis Latihan", "Repetisi", "Status"])

def save_history(exercise, count):
    """Menyimpan sesi latihan ke CSV."""
    df = load_history()
    now = datetime.now()
    new_data = pd.DataFrame({
        "Tanggal": [now.strftime("%Y-%m-%d")],
        "Waktu": [now.strftime("%H:%M:%S")],
        "Jenis Latihan": [exercise],
        "Repetisi": [count],
        "Status": ["Selesai"]
    })
    # Menggabungkan data lama dan baru
    df = pd.concat([new_data, df], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)

# --- JUDUL & SIDEBAR ---
st.title("AI Workout Assistant (High Res)")
st.markdown("""
Dashboard ini menggunakan **YOLOv8 / YOLO11 Pose Estimation** dengan **Resolusi Asli**.
Data latihan akan otomatis disimpan saat tombol **Stop & Simpan** ditekan.
""")

# Sidebar untuk Pengaturan
# --- MODIFIKASI: Menggunakan Form agar tidak auto-reload ---
with st.sidebar.form(key='config_form'):
    st.header("Pengaturan")
    # Menambahkan opsi YOLOv8 dan YOLO11 lengkap (n, s, m, l, x)
    model_type = st.selectbox(
        "Pilih Model", 
        [
            "yolov8n-pose.pt", "yolov8s-pose.pt", "yolov8m-pose.pt", "yolov8l-pose.pt", "yolov8x-pose.pt",
            "yolo11n-pose.pt", "yolo11s-pose.pt", "yolo11m-pose.pt", "yolo11l-pose.pt", "yolo11x-pose.pt"
        ]
    )

    # Cek ketersediaan GPU untuk opsi default
    default_device_index = 1 if torch.cuda.is_available() else 0
    device_option = st.selectbox(
        "Device", 
        ["cpu", "cuda:0"], 
        index=default_device_index, 
        help="Jika GPU tidak terdeteksi, sistem akan otomatis menggunakan CPU."
    )

    input_source = st.radio("Sumber Input", ["Video Upload", "Webcam"])
    exercise_type = st.selectbox("Jenis Latihan", ["PushUp", "PullUp"])

    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.5, 0.05)
    
    # Tombol konfirmasi
    submit_btn = st.form_submit_button("OK / Terapkan")

# --- SIDEBAR HISTORY (Di luar form agar bisa interaksi langsung) ---
st.sidebar.markdown("---")
st.sidebar.header("Riwayat Latihan")
if st.sidebar.checkbox("Tampilkan Tabel Riwayat", value=True):
    df_history = load_history()
    if not df_history.empty:
        st.sidebar.dataframe(
            df_history, 
            hide_index=True,
            use_container_width=True
        )
        if st.sidebar.button("Hapus Riwayat"):
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
                st.rerun()
    else:
        st.sidebar.info("Belum ada data latihan.")

# --- FUNGSI UTILITAS MATEMATIKA ---
def calculate_angle(a, b, c):
    """Menghitung sudut antara tiga titik (a, b, c). b adalah titik sudut."""
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return angle

def get_dynamic_font_scale(frame_width):
    """Menyesuaikan ukuran teks berdasarkan lebar video agar tidak kekecilan di resolusi tinggi."""
    # Base scale 1.0 untuk lebar 1000px
    return frame_width / 1000.0

# --- KELAS ANALISIS POSE ---
class PoseAnalyzer:
    def __init__(self, exercise_type):
        self.exercise_type = exercise_type
        self.counter = 0
        self.stage = None
        self.feedback = ""
        self.form_status = "OK"
        
        self.pushup_up_angle = 145 
        self.pushup_down_angle = 90
        self.body_straight_threshold = 150
        
        self.pullup_up_angle = 90   # Diubah ke 90 sesuai permintaan
        self.pullup_down_angle = 145 # Diubah ke 145 sesuai permintaan
        
    def analyze(self, keypoints):
        if keypoints.shape[0] == 0:
            return None, "Tidak ada orang terdeteksi"

        l_shoulder, r_shoulder = keypoints[5], keypoints[6]
        l_elbow, r_elbow = keypoints[7], keypoints[8]
        l_wrist, r_wrist = keypoints[9], keypoints[10]
        l_hip, r_hip = keypoints[11], keypoints[12]
        l_knee, r_knee = keypoints[13], keypoints[14]
        l_ankle, r_ankle = keypoints[15], keypoints[16]
        l_ear, r_ear = keypoints[3], keypoints[4]
        nose = keypoints[0]

        a_shoulder, a_elbow, a_wrist, a_hip, a_knee, a_ankle, a_ear = \
            r_shoulder, r_elbow, r_wrist, r_hip, r_knee, r_ankle, r_ear
        
        side = "Kanan"
        orientation = "Depan/Belakang"
        
        # Inisialisasi variabel sudut agar tidak error
        neck_angle = 0
        body_angle = 0
        elbow_angle = 0

        if self.exercise_type == "PushUp":
            if nose[0] > l_shoulder[0] and nose[0] > r_shoulder[0]:
                orientation = "Menghadap Kanan"
            elif nose[0] < l_shoulder[0] and nose[0] < r_shoulder[0]:
                orientation = "Menghadap Kiri"
            else:
                orientation = "Depan/Belakang"

            if l_hip[0] > 0 and r_hip[0] == 0:
                side = "Kiri"
                a_shoulder, a_elbow, a_wrist, a_hip, a_knee, a_ankle, a_ear = \
                    l_shoulder, l_elbow, l_wrist, l_hip, l_knee, l_ankle, l_ear
            elif r_hip[0] > 0 and l_hip[0] == 0:
                side = "Kanan"
            
            elif l_hip[0] > 0 and r_hip[0] > 0:
                if orientation == "Menghadap Kiri":
                    side = "Kiri" 
                    a_shoulder, a_elbow, a_wrist, a_hip, a_knee, a_ankle, a_ear = \
                        l_shoulder, l_elbow, l_wrist, l_hip, l_knee, l_ankle, l_ear
                else:
                    side = "Kanan"

        elif self.exercise_type == "PullUp":
            orientation = "Depan/Belakang"

        # --- LOGIKA PUSHUP ---
        if self.exercise_type == "PushUp":
            elbow_angle = calculate_angle(a_shoulder, a_elbow, a_wrist)
            body_angle = calculate_angle(a_shoulder, a_hip, a_ankle)
            neck_angle = calculate_angle(a_ear, a_shoulder, a_hip)

            self.feedback = []
            self.form_status = "OK"

            if body_angle < self.body_straight_threshold:
                self.feedback.append("LURUSKAN PUNGGUNG!")
                self.form_status = "BAD"
            
            if neck_angle < 140:
                self.feedback.append("KEPALA LURUS KE DEPAN!")
                self.form_status = "BAD"

            if elbow_angle > self.pushup_up_angle:
                self.stage = "UP"
            if elbow_angle < self.pushup_down_angle and self.stage == 'UP':
                if self.form_status == "OK":
                    self.stage = "DOWN"
                    self.counter += 1
                else:
                    self.feedback.append("Repetisi tidak dihitung (Form Buruk)")

            return {
                "count": self.counter,
                "stage": self.stage,
                "feedback": self.feedback,
                "angle": elbow_angle,
                "body_angle": body_angle,
                "neck_angle": neck_angle, # Ditambahkan ke return value
                "orientation": orientation,
                "side": side
            }

        # --- LOGIKA PULLUP ---
        elif self.exercise_type == "PullUp":
            l_elbow_angle = calculate_angle(l_shoulder, l_elbow, l_wrist)
            r_elbow_angle = calculate_angle(r_shoulder, r_elbow, r_wrist)
            avg_elbow_angle = (l_elbow_angle + r_elbow_angle) / 2
            
            self.feedback = []
            if avg_elbow_angle > self.pullup_down_angle:
                self.stage = "DOWN"
            if avg_elbow_angle < self.pullup_up_angle and self.stage == "DOWN":
                self.stage = "UP"
                self.counter += 1
                
            return {
                "count": self.counter,
                "stage": self.stage,
                "feedback": self.feedback,
                "angle": avg_elbow_angle,
                "orientation": orientation
            }

# --- MAIN APP LOGIC ---

@st.cache_resource
def load_model(model_name, device):
    final_device = device
    if device == 'cuda:0' and not torch.cuda.is_available():
        final_device = 'cpu'
        st.warning(f"GPU tidak terdeteksi oleh PyTorch. Otomatis beralih ke {final_device}.")
    
    try:
        model = YOLO(model_name)
        model.to(final_device)
        return model, final_device
    except Exception as e:
        if final_device != 'cpu':
            st.warning(f"Gagal memuat di {final_device}, mencoba CPU...")
            model = YOLO(model_name)
            model.to('cpu')
            return model, 'cpu'
        else:
            raise e

try:
    model, active_device = load_model(model_type, device_option)
    st.sidebar.success(f"Model berjalan di: {active_device.upper()}")
except Exception as e:
    st.error(f"Gagal memuat model: {e}.")
    st.stop()

if 'analyzer' not in st.session_state or st.session_state.current_exercise != exercise_type:
    st.session_state.analyzer = PoseAnalyzer(exercise_type)
    st.session_state.current_exercise = exercise_type

analyzer = st.session_state.analyzer

col1, col2 = st.columns([3, 1])
with col2:
    st.markdown("### Statistik Real-Time")
    st_count = st.empty()
    st_stage = st.empty()
    st_feedback = st.empty()
    
    st.markdown("---")
    # Placeholder baru untuk data detail di sidebar
    st_angle = st.empty()
    st_body_angle = st.empty()
    st_neck_angle = st.empty() # Placeholder untuk Sudut Leher
    st_orientation = st.empty()
    
    # Tombol Reset Manual
    if st.button("Reset Counter", key="reset_btn"):
        analyzer.counter = 0
        analyzer.stage = None
        st.rerun()

with col1:
    st_frame = st.empty()

cap = None

if input_source == "Video Upload":
    uploaded_file = st.file_uploader("Upload Video Latihan (Resolusi Asli)", type=['mp4', 'mov', 'avi'])
    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        cap = cv2.VideoCapture(tfile.name)
elif input_source == "Webcam":
    if st.button("Mulai Webcam (Resolusi Max)"):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
             cap = cv2.VideoCapture(1)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
        st.toast(f"Webcam Aktif")

if cap is not None and cap.isOpened():
    # --- TOMBOL STOP & SAVE ---
    # Tombol ini akan menghentikan loop while di bawahnya
    stop_button = st.button("Stop & Simpan", type="primary", use_container_width=True)
    
    if stop_button:
        # Logika Penyimpanan
        if analyzer.counter > 0:
            save_history(exercise_type, analyzer.counter)
            st.success(f"Latihan Disimpan: {exercise_type} ({analyzer.counter} Reps)")
            # Reset counter setelah simpan agar siap untuk sesi berikutnya
            analyzer.counter = 0
            analyzer.stage = None
        else:
            st.info("Latihan dihentikan. Tidak ada repetisi untuk disimpan.")

    while cap.isOpened() and not stop_button:
        ret, frame = cap.read()
        if not ret:
            # --- LOGIKA AUTO-SAVE SAAT VIDEO SELESAI ---
            if analyzer.counter > 0:
                save_history(exercise_type, analyzer.counter)
                st.success(f"Video Selesai. Latihan Disimpan: {exercise_type} ({analyzer.counter} Reps)")
                # Reset counter
                analyzer.counter = 0
                analyzer.stage = None
            else:
                st.warning("Video selesai. Tidak ada repetisi untuk disimpan.")
            break
        
        h, w, _ = frame.shape
        
        # --- UPDATE DISINI: TRY-EXCEPT UNTUK INFERENCE ---
        try:
            # MENAMBAHKAN max_det=1 AGAR HANYA MENDETEKSI 1 ORANG
            results = model(frame, verbose=False, conf=confidence_threshold, device=active_device, max_det=1)
        except Exception as e:
            # Jika error GPU saat runtime, pindah ke CPU dan coba lagi
            if active_device == 'cuda:0':
                st.toast("Error GPU Runtime. Switch ke CPU...", icon="⚠️")
                active_device = 'cpu'
                model.to('cpu')
                results = model(frame, verbose=False, conf=confidence_threshold, device='cpu', max_det=1)
            else:
                raise e

        # Plot keypoints saja (boxes=False akan menghilangkan kotak, menyisakan dot)
        annotated_frame = results[0].plot(boxes=False)

        try:
            keypoints = results[0].keypoints.xy.cpu().numpy()
            
            if len(keypoints) > 0:
                person_keypoints = keypoints[0]
                data = analyzer.analyze(person_keypoints)
                
                # Update UI Side Bar (Col2) - Semua teks dipindah ke sini
                st_count.metric("Repetisi", data['count'])
                st_stage.info(f"Posisi: {data['stage'] if data['stage'] else 'Mulai'}")
                
                # Menampilkan data detail di panel samping
                st_angle.write(f"**Sudut Siku:** {int(data.get('angle', 0))}°")
                st_body_angle.write(f"**Sudut Badan:** {int(data.get('body_angle', 0))}°")
                
                # Menampilkan Sudut Leher jika ada datanya
                if data.get('neck_angle', 0) > 0:
                     st_neck_angle.write(f"**Sudut Leher:** {int(data.get('neck_angle', 0))}°")
                else:
                     st_neck_angle.empty()

                st_orientation.write(f"**Arah:** {data.get('orientation', '-')}")
                
                feedback_text = data.get('feedback', [])
                if feedback_text:
                    st_feedback.error("\n".join(feedback_text))
                    # cv2.putText DIHAPUS agar frame bersih
                else:
                    st_feedback.success("Form Bagus!")

                # cv2.putText untuk Badan dan Arah DIHAPUS agar frame bersih

        except Exception as e:
            pass

        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        
        # --- PERBAIKAN DISPLAY: RESIZE VISUAL ---
        # Kita kecilkan ukuran frame HANYA untuk ditampilkan di layar (biar gak kegedean).
        # Tapi AI (model) di atas tetap memproses frame resolusi ASLI.
        display_width = 640
        aspect_ratio = h / w
        display_height = int(display_width * aspect_ratio)
        frame_resized = cv2.resize(frame_rgb, (display_width, display_height))
        
        try:
            # Hapus width="stretch" agar ukuran mengikuti hasil resize (640px)
            st_frame.image(frame_resized, channels="RGB")
        except Exception:
            # Mengabaikan error jika frame gagal dirender saat cleanup (video selesai)
            pass

    cap.release()
else:
    with col1:
        st.info("Menunggu input...")
