![image](https://github.com/user-attachments/assets/7c156468-8150-496d-802f-b2cdd572a515)

HOME PAGE 
![image](https://github.com/user-attachments/assets/15ba53bf-5cc7-43ff-8fb1-1763a3d7dd35)

🎙️ **Jarvis AI Assistant**

A voice-controlled AI Assistant built with Python that can perform tasks like answering questions, opening apps, searching the web, playing music, automating tasks, and more — inspired by J.A.R.V.I.S. from Iron Man.

---

## 🚀 Features

- 🔊 Voice recognition and speech response
- 🌐 Google/Wikipedia/YouTube search
- 🎵 Play music via YouTube
- 🧠 Answer general knowledge questions using Wikipedia
- 💬 Tell jokes
- 📁 Open files and applications
- 🖱️ GUI automation using PyAutoGUI
- 🧾 Notes and reminders
- 📲 Message and call functionality
- 📄 Reads PDFs aloud
- 📋 Saves voice commands history

---

## 🛠️ Technologies Used

- `Python`
- `speechrecognition` for voice input
- `pyttsx3` for text-to-speech
- `wikipedia` for fetching summaries
- `pywhatkit` for YouTube and WhatsApp
- `pyautogui` for GUI automation
- `pyjokes` for fun interaction
- `sqlite3` for storing notes and history

---

## 📦 Installation

### 1. Clone the repository:

```bash
git clone https://github.com/saurabhmaurya6746/Jarvis 
cd jarvis

2. Install the dependencies:

pip install -r requirements.txt
If you face issues with pyaudio installation on Windows:

pip install pipwin
pipwin install pyaudio
▶️ How to Run

python run.py
Make sure your microphone is enabled and connected.

📁 Project Structure

📁 Jarvis/
├── main.py               # Core assistant logic
├── run.py                # Entry point
├── contacts.csv          # Contact list for call/message
├── jarvis.db             # Local database for storage
├── requirements.txt      # Python dependencies
├── window_dump.xml       # ADB UI automation structure
├── Pdf/                  # PDF documents Jarvis can read
│   ├── debugging.pdf
│   ├── knowledge.pdf
│   └── nodal.pdf
├── www/                  # Frontend assets (HTML, JS, CSS)
│   ├── index.html
│   ├── controller.js
│   └── style.css
└── README.md             # Project guide
📷 Screenshots

**Face Recognition Pipeline Overview**

The face recognition system in this project utilizes OpenCV's LBPH (Local Binary Patterns Histograms) method for face detection and recognition. The system captures images, trains a face recognition model, and then uses that model for face recognition. Below is a breakdown of the files in the engine/auth/ folder:
1. Capturing Face Samples: Use sample.py to capture images of faces. These images are stored in the samples/ folder with unique labels.

2. Training the Model: Use trainer.py to train the face recognition model using the captured samples. The model is stored in the trainer/ folder.

3. Face Recognition: Use recoganize.py to perform face recognition. This script will load the trained model and attempt to identify faces in real-time or from stored images.

🙋‍♂️ Author
Saurabh Maurya
Final-year CSE student at Prasad Institute of Technology

📄 License
This project is licensed under the MIT License.

## 📄 requirements.txt

Create a `requirements.txt` file and include:

pyttsx3
speechrecognition
wikipedia
pywhatkit
webbrowser
pyautogui
pyaudio
playsound
eel
pvporcupine
pymupdf
hugchat
