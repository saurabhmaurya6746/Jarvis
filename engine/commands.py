import pyttsx3
import speech_recognition as sr
import eel
import time
import datetime


#how can you open my notification settings
def speak(text):
    text=str(text)
    print(text)
    eel.DisplayMessage(text)
    # eel.DisplayMessage('hhh')
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    # engine.setProperty('rate',174)
    engine.setProperty('rate',140)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source :
        print("listening...")  
        eel.DisplayMessage("listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source , 10,7)
    try:
        print("recongnizing......")
        eel.DisplayMessage("recognizing...")
        query=r.recognize_google(audio , language='en-in')
        print("user said :",query)
        eel.DisplayMessage(query)
        # speak(query)
        time.sleep(2)
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def wishme():
    hour=int(datetime.datetime.now().hour)
    if(hour>=0 and hour<=12):
        speak('Good morning Sir')
    elif(hour>=12 and hour<=16):
        speak('Good afternoon Sir')
    else:
        speak('Good evening Sir')
    
    speak(" I am jarvis, please say how may I help you")


@eel.expose
def allCommands(message=1):
    if message == 1: 
        query=takecommand()
        print(query)
        eel.senderText(query)
    else:
        query=message
        print(query)
        eel.senderText(query)
        
    try:
        query = query.replace('Jarvis',"")
        query = query.strip()

        if "open" in query and "pdf" in query and "search" in query:
            # print('hello')
            from engine.features import search_file_and_words
            file_name, search_word = search_file_and_words(query)
            print(file_name,search_word)
            if file_name and search_word:
                from engine.features import open_pdf_and_search
                open_pdf_and_search(file_name, search_word)

        elif 'open' in query and 'recent app' in query or 'recent tab' in query or 'recent apps' in query:
            from engine.helper import open_recent_apps
            speak("opening recent apps ")
            open_recent_apps()
        elif ('close' in query or 'closed' in query) or ('remove' in query or 'removed' in query) and ('from' in query or 'in' in query) and ('recent app' in query or 'recent apps' in query):
            # Extract app name by removing unnecessary words
            words = query.replace('close', '').replace('closed', '').replace('app', '').replace('application', '').strip()
            from engine.helper import extract_app_name
            app_name = extract_app_name(query)  # You can clean more if needed
            print(f"Closing {app_name}")
            speak(f"Closing {app_name}")
            from engine.helper import close_specific_recent_app
            close_specific_recent_app(app_name)    
        elif ('close' in query or 'closed' in query) or ('all app' in query or 'all apps' in query) or ('all my app' in query or 'all my apps' in query) or ('all recent app' in query or 'all recent apps' in query):
            from engine.helper import close_all_apps,go_home
            go_home()
            close_all_apps()  
        elif 'take screnshot' in query or 'take screenshot' in query:
            from engine.mobile import take_screenshot 
            speak('taking screenshot')
            take_screenshot()

        elif 'my battery percentage' in query or 'battery percentage' in query:
            from engine.mobile import battery_status
            battery_status()

        elif 'set my brightness' in query or 'set brightness' in query:
            from engine.mobile import set_brightness
            speak('how much brightness you want')
            level = takecommand()
            # level = 'set at level 40'
            set_brightness(level)

        elif "turn on wifi" in query or "enable wifi" in query:
            from engine.mobile import toggle_wifi_true
            toggle_wifi_true(on=True)

        elif "turn off wifi" in query or "disable wifi" in query:
            from engine.mobile import toggle_wifi_false
            toggle_wifi_false(on=False)

        elif "turn on mobile data" in query or "enable mobile data" in query:
            from engine.mobile import toggle_mobile_data_on
            toggle_mobile_data_on(on=True)

        elif "turn off mobile data" in query or "disable mobile data" in query:
            from engine.mobile import toggle_mobile_data_off
            toggle_mobile_data_off(on=False)
        elif 'scroll down' in query:
            from engine.helper import scroll_down
            scroll_down()

        elif 'scroll up' in query:
            from engine.helper import scroll_up
            scroll_up()

        elif 'back home' in query or 'back to home' in query or 'go home' in query:
            from engine.helper import go_home
            go_home()
        
        elif 'choose' in query and 'this app' in query:
            from engine.helper import open_recent_apps_tab
            open_recent_apps_tab(500,500)

        elif 'valume up' in query or 'volume up' in query:
            from engine.helper import volume_up
            speak('volume up')
            volume_up()
        elif 'valume down' in query or 'volume down' in query:
            from engine.helper import volume_down
            speak('volume down')
            volume_down()
        elif 'lock screen' in query or 'lock my screen' in query:
            from engine.helper import lock_screen
            lock_screen()

        elif 'open notifications panel' in query or 'open notification bar' in query or 'open notification' in query:
            from engine.helper import open_notifications
            open_notifications()
        
        elif 'move left' in query:
            from engine.helper import move_left
            move_left()
        
        elif 'move right' in query:
            from engine.helper import move_right
            move_right()     

        elif 'go back' in query:
            from engine.helper import go_back  
            go_back()            
        elif "open" in query and "pdf" in query:
            # print("open pdf perform")
            from engine.features import open_pdf ,search_pdf_name
            file_name=search_pdf_name(query)
            print(file_name)
            open_pdf(file_name)

        elif "the time" in query:
            time=datetime.datetime.now().strftime("%H:%M:%S")
            print('Sir ,the time is ',time)
            speak('Sir , the time is')
            speak(time)

        elif "send message" in query or "phone call" in query or "video call" in query or "send a message" in query or 'send messge' in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                # preferance = 'mobile'
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query or "send a message" in query or 'send messge' in query: 
                        speak("what message to send")
                        message = takecommand()
                        # message = 'this is testing message'
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query or "send a message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)
                else:
                    speak('No response found')

        elif "on youtube" in query:
            print('in youtube')
            from engine.features import PlayYoutube
            PlayYoutube(query)

        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
                     
        elif 'delete' in query and 'pdf' in query and any(word in query for word in ['temporary pdf', 'temporary folder']):
            from engine.features import clear_temp_pdfs
            # filename=extract_filenames_from_query(query)
            clear_temp_pdfs(query)
        else:
            from engine.features import chatBot
            query = query+' in 40 words'
            response = chatBot(query) 
            speak(response)
    except:
        print("error")
        
    eel.ShowHood()









