from playsound import playsound
import eel , os
import time
from engine.commands import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
import re
import webbrowser
import sqlite3
# playing assistant sound
from engine.helper import *
import pvporcupine
import struct
import subprocess 
import time
import pyaudio
import fitz  
import pymupdf
import tkinter as tk
import pyautogui
from urllib.parse import quote
import tempfile
from hugchat import hugchat
# for pdf extration 
import glob

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\Audio\\music.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query.lower()

    app_name = query.strip()

    if app_name != "":

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
            results = cursor.fetchall()

            if len(results) != 0:
                speak("Opening "+query)
                os.startfile(results[0][0])

            elif len(results) == 0: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
        except:
            speak("some thing went wrong")

# opening pdf 
def open_pdf(file_name):
    search_name = file_name
    pdf_folder = "Pdf"
    if not search_name.endswith(".pdf"):
        # file_name += ".pdf"
        search_name += ".pdf"
    cursor.execute("SELECT file_name FROM pdf_files WHERE file_name = ?", (search_name,))
    result = cursor.fetchone()
    print(result,'file')

    if result:
        pdf_file = result[0]  # Get the file name from the database 
        pdf_path = os.path.join(pdf_folder, pdf_file)  # Construct full path

        if os.path.exists(pdf_path):
            print(f"Found '{pdf_path}'. Opening...")
            speak(f"Found '{pdf_path}'. Opening...")
            os.startfile(pdf_path)  # Open the PDF file
        else:
            print(f"Error: File '{pdf_path}' not found. Check if it exists.")
            speak(f"Error: File '{pdf_path}' not found. Check if it exists.")
    else:
        print("PDF not found in the database.")
        speak("PDF not found in the database.")

def search_pdf_name(query):
    # Convert query to lowercase for easy matching
        # Find the starting position of the file name (after "open")
        file_start = query.find("open") + 5  # "open " is 5 characters
        file_end = query.find("pdf")  # Find the position of "pdf"

        # Extract file name
        file_name = query[file_start:file_end].strip()

        return file_name
    
        return None



# finding file name and searching words 
def search_file_and_words(query):
    query = query.lower()
    if "open" in query and "search" in query:
        file_start = query.find("open") + 5
        file_end = query.find("pdf")
        file_name = query[file_start:file_end].strip()

        search_start = query.find("search") + 7
        search_word = query[search_start:].strip()

        return file_name, search_word
    else:
        return None, None


# # PyMuPDF for opening and searching PDF

def open_pdf_and_search(file_name, search_word):
    if not file_name.endswith(".pdf"):
        file_name += ".pdf"

    cursor.execute("SELECT file_name FROM pdf_files WHERE file_name = ?", (file_name,))
    result = cursor.fetchone()

    if not result:
        print("PDF not found in the database.")
        speak("PDF not found in the database.")
        eel.DisplayMessage("PDF not found in the database.")
        return
    
    pdf_path = os.path.join("Pdf", result[0])  # Ensure correct path
    print(f"Found '{pdf_path}'. Opening and searching...")
    speak(f"Found '{pdf_path}'. Opening and searching...")
    eel.DisplayMessage(f"Found '{pdf_path}'. Opening and searching...")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF: {e}")
        return
    count=0
    found = False
    for page in doc:
        text_instances = page.search_for(search_word)
        if text_instances:
            for inst in text_instances:
                page.add_highlight_annot(inst)
                count=count+1
            found = True
    print(f'There is total {count},{search_word} words in {file_name}')
    speak(f'There is total {count},{search_word} words in {file_name}')
    eel.DisplayMessage(f'There is total {count},{search_word} words in {file_name}')

    if found:
        try:
            # Ensure `temporary pdf` folder exists
            temp_folder = "temporary"
            os.makedirs(temp_folder, exist_ok=True)

            # Save the highlighted file in `temporary pdf/`
            temp_pdf_path = os.path.join(temp_folder, file_name)
            doc.save(temp_pdf_path)  
            doc.close()

            print(f"Highlighted PDF saved temporarily at: {temp_pdf_path}")
            speak(f"Highlighted PDF saved temporarily at: {temp_pdf_path}")
            eel.DisplayMessage(f"Highlighted PDF saved temporarily at: {temp_pdf_path}")

            # Open the PDF
            # if os.name == 'nt':  # Windows
            subprocess.run(["start", temp_pdf_path], shell=True)
            

        except Exception as e:
            print(f"Error handling temporary PDF: {e}")
    else:
        print(f"'{search_word}' not found in '{file_name}'.")
        speak(f"'{search_word}' not found in '{file_name}'.")
        eel.dis(f"'{search_word}' not found in '{file_name}'.")

    doc.close()


def extract_filenames_from_query(query):
    # Extract words that seem like filenames but may not have .pdf
    words = re.findall(r'\b\w+\b', query)  # Extract only words

    # Convert them to PDF filenames
    filenames = {word + ".pdf" for word in words if word.lower() not in {"delete", "all", "the", "file", "from", "temporary pdf", "except", "and","jarvis","temporary","pdf","folder"}}
    
    return filenames  # Return a set of filenames

def clear_temp_pdfs(query):
    temp_folder = "temporary"
    
    if not os.path.exists(temp_folder):
        print("Temp folder does not exist. Nothing to delete.")
        speak("Temp folder does not exist. Nothing to delete.")
        eel.DisplayMessage("Temp folder does not exist. Nothing to delete.")
        return
    
    # Extract filenames to keep from the user query
    keep_files = extract_filenames_from_query(query)
    print(f"Files to keep: {keep_files}")

    # Get all PDF files in the temp folder
    for file_path in glob.glob(os.path.join(temp_folder, "*.pdf")):
        file_name = os.path.basename(file_path)  # Extract filename only
        
        if file_name not in keep_files:
            try:
                os.remove(file_path)
                print(f"Deleted: {file_name}")
                speak(f"Deleted: {file_name}")
                eel.DisplayMessage(f"Deleted: {file_name}")
            except Exception as e:
                print(f"Error deleting {file_name}: {e}")
                speak(f"Error deleting {file_name}: {e}")
                eel.DisplayMessage(f"Error deleting {file_name}: {e}")


def findContact(query):
    print('find')
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp','whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

# Create Whatsapp Function  
def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        print('tab')
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        jarvis_message = "staring video call with "+name
    
    # Encode the message for URL
    encoded_message = quote(message)
     
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
    full_command = f'start "" "{whatsapp_url}"'

    # whatsapp_url = f"https://web.whatsapp.com/send?phone={mobile_no}&text={encoded_message}"

    # # Open the URL in the default web browser
    # full_command=webbrowser.open(whatsapp_url)

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    # subprocess.run(full_command, shell=True)

    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        # print(i,'press')
        pyautogui.hotkey('tab')
    
    pyautogui.hotkey('enter')

    speak(jarvis_message)
    eel.DisplayMessage(jarvis_message)

# youtube search    
def PlayYoutube(query):
    print('playyoutube')
    search_term = extract_yt_term(query)
    speak("Playing " + search_term)
    kit.playonyt(search_term)


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa","atlas"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()


# chat bot 
def chatBot(query):
    
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine/cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print("User Query:", query)
    # response = chatbot.chat(user_input)
    # speak(response)
    print("Chatbot Response:", response)
    
    return response

# android automation

def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)

# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(270, 1480)
    #start chat
    tapEvents(590, 575)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(300, 345)
    # tap on input
    tapEvents(370, 1511)
    #message
    adbInput(message)
    #send
    tapEvents(665, 1510)
    speak("message send successfully to "+name)


