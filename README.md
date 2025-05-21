# 🗣️ Speech Recognition with Whisper.cpp + Gradio

A simple tool to transcribe audio files using [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) with a Gradio web
interface.

---

## ✅ Features

- Transcribe audio files to text using Whisper.cpp
- Optional timestamp inclusion
- Web UI powered by Gradio
- Support for Core ML on macOS (Apple Silicon)

---

## 🧰 Setup Instructions (macOS Apple Silicon)

### 1. Install Xcode Command Line Tools

Ensure Core ML support works correctly:

```bash
xcode-select --install
```

### 2. Create a Conda Environment

```bash
conda create -n py311-whisper python=3.11 -y
conda activate py311-whisper
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Clone Whisper.cpp Repository

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
```

### 5. Download a Pretrained Model

```bash
cd whisper.cpp
./models/download-ggml-model.sh base.en
```

### 6. Generate Core ML Model

```bash
./models/generate-coreml-model.sh base.en
```

### 7. Build Whisper.cpp with Core ML Support

```bash
cmake -B build -DWHISPER_COREML=1
cmake --build build -j --config Release
```

### 8. Test Whisper CLI

```bash
./build/bin/whisper-cli -f samples/jfk.wav
```

## 🚀 Run the Web Interface

Once setup is complete, launch the Gradio app:

```bash
python main.py
```


## 📁 Directory Structure
```
.
├── app/
│   ├── asr.py           # Core transcription logic
│   └── main.py          # Gradio interface
├── data/tmp/            # Temporary audio and text files (optional)
├── whisper.cpp/         # External repository
├── requirements.txt     # Python dependencies
└── README.md
```


## 📌 Notes
Tested on macOS M1 with Python 3.11

Ensure Whisper.cpp is built before launching the app

For best results, use .wav files or let the app handle conversion using ffmpeg
