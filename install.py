import subprocess
import sys
import platform
import re

def get_gpu_info():
    """
    Mengecek GPU NVIDIA dan versi CUDA driver yang terinstall.
    Mengembalikan tuple: (is_available, cuda_version_float)
    """
    print("🔍 Sedang memeriksa ketersediaan GPU NVIDIA & Versi Driver...")
    try:
        # Menjalankan nvidia-smi
        output = subprocess.check_output('nvidia-smi', stderr=subprocess.STDOUT).decode('utf-8')
        
        # Mencari string "CUDA Version: XX.X" menggunakan Regex
        match = re.search(r"CUDA Version:\s+(\d+\.\d+)", output)
        cuda_version = float(match.group(1)) if match else 0.0
        
        print(f"✅ GPU NVIDIA Terdeteksi! (Max Supported CUDA: {cuda_version})")
        return True, cuda_version
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️ GPU NVIDIA tidak terdeteksi atau driver bermasalah (nvidia-smi not found).")
        return False, 0.0

def install(packages, index_url=None):
    """Menjalankan perintah pip install."""
    cmd = [sys.executable, "-m", "pip", "install"]
    
    if index_url:
        cmd.extend(["--index-url", index_url])
        # Tambahkan extra-index-url ke pypi standar agar dependency lain (numpy/jinja2) tetap ketemu
        cmd.extend(["--extra-index-url", "https://pypi.org/simple"])
    
    # Menambahkan paket ke command
    if isinstance(packages, list):
        cmd.extend(packages)
    else:
        cmd.extend(packages.split())
        
    print(f"\n🔄 Menjalankan: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
        print("✅ Berhasil.")
    except subprocess.CalledProcessError:
        print("❌ Gagal menginstall paket. Pastikan koneksi internet stabil.")
        sys.exit(1)

def main():
    print("========================================")
    print("   AUTO INSTALLER - AI WORKOUT ASSISTANT")
    print("========================================")
    
    # 1. Cek GPU dan Versi Driver
    has_gpu, max_cuda_version = get_gpu_info()
    
    print("\n📦 Tahap 1: Instalasi Core AI (PyTorch)...")
    
    if has_gpu:
        print("🚀 Mode: GPU ACCELERATED")
        
        # --- LOGIKA PEMILIHAN VERSI ---
        # GTX 1050 sebenernya support CUDA 12 kalo driver update.
        # Tapi kita cari aman berdasarkan versi driver yang terdeteksi sekarang.
        
        if max_cuda_version >= 12.1:
            print(f"Driver kamu modern (Support CUDA {max_cuda_version}). Menginstall PyTorch CUDA 12.1...")
            pt_index = "https://download.pytorch.org/whl/cu121"
        elif max_cuda_version >= 11.0:
            print(f"Driver kamu versi lama (Max CUDA {max_cuda_version}). Menginstall PyTorch CUDA 11.8 (Compatible Mode)...")
            pt_index = "https://download.pytorch.org/whl/cu118"
        else:
            print(f"⚠️ Driver kamu sangat lama (Max CUDA {max_cuda_version}).")
            print("Mencoba install versi CUDA 11.8 (Saran: Update driver NVIDIA kamu jika gagal)...")
            pt_index = "https://download.pytorch.org/whl/cu118"
            
        try:
            install("torch torchvision torchaudio", index_url=pt_index)
        except Exception:
            print("⚠️ Gagal install versi GPU. Mencoba fallback ke CPU...")
            install("torch torchvision torchaudio")
            
    else:
        print("🐢 Mode: CPU ONLY")
        print("Sedang menginstall PyTorch versi standar...")
        install("torch torchvision torchaudio")

    # 2. Install Library Pendukung Lainnya
    print("\n📦 Tahap 2: Instalasi Library Pendukung...")
    requirements = [
        "streamlit",
        "opencv-python",
        "numpy",
        "pandas",
        "Pillow",
        "ultralytics"
    ]
    
    install(requirements)

    print("\n========================================")
    print("🎉 INSTALASI SELESAI!")
    print("========================================")
    print("Cara menjalankan aplikasi:")
    print("👉 streamlit run app.py")

if __name__ == "__main__":
    main()
