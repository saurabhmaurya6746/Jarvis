import re
import os 
import time
import xml.etree.ElementTree as ET
from engine.commands import speak
import eel 

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    # Fallback: if the expected pattern isn't found, use the entire command
    return match.group(1) if match else command

#### 6. Make Helper Function to remove unwanted words from query

def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]
    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string

# # explanation 
# # filtered_words = []

# # # Iterate over each word in the 'words' list
# # for word in words:
# #     # Convert the word to lowercase and check if it's not in 'words_to_remove'
# #     if word.lower() not in words_to_remove:
# #         # If the condition is True, append the original 'word' to 'filtered_words'
# #         filtered_words.append(word)

# #### 7. Example of Helper Function
 
# input_string = "make a phone call to pappa"
# words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', '']

# result = remove_words(input_string, words_to_remove)
# print(result)



# key events like receive call, stop call, go back
def keyEvent(key_code):
    command =  f'adb shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

# Tap event used to tap anywhere on screen
def tapEvents(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

#tab on center for opening recent app
def open_recent_apps_tab(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

def adbInput(message):
    command =  f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

def go_back():
    os.system('adb shell input keyevent 4')  # KEYCODE_BACK is 4
    time.sleep(1)
    # print("Went Back")

# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

# To replace space in string with %s for complete message send
def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')

# for swaping 
def swipe(x1, y1, x2, y2, duration=300):
    command = f'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'
    os.system(command)

# Move left (Swipe Right to Left)
def move_left():
    os.system('adb shell input swipe 600 850 200 850 300')  # Adjust coordinates as per screen resolution
    print("Moved Left")

# Move right (Swipe Left to Right)
def move_right():
    os.system('adb shell input swipe 100 850 600 850 300')  # Adjust coordinates
    print("Moved Right")

# Scroll down (Swipe Up to Down)
def scroll_down():
    os.system('adb shell input swipe 500 300 500 1000 300')  # Adjust coordinates
    print("Scrolled Down")

# Scroll up (Swipe Down to Up)
def scroll_up():
    os.system('adb shell input swipe 500 1000 500 300 300')  # Adjust coordinates
    print("Scrolled Up")

def go_home():
    os.system('adb shell input keyevent 3')
    print("Went Home")

def volume_up():
    os.system('adb shell input keyevent 24')
    print("Volume Up")

def volume_down():
    os.system('adb shell input keyevent 25')
    print("Volume Down")

def lock_screen():
    os.system('adb shell input keyevent 26')
    print("Locked Screen")

def open_notifications():
    os.system('adb shell cmd statusbar expand-notifications')
    print("Opened Notifications")

def swipe_up():
    os.system('adb shell input swipe 500 1500 500 500 300')
    print("Swiped Up")

def swipe_down():
    os.system('adb shell input swipe 500 500 500 1500 300')
    print("Swiped Down")


# # opening recent app 
# def open_recent_apps():
#     os.system('adb shell input keyevent 187')
#     print("Opened Recent Apps")

def open_recent_apps():
    """Open the recent apps screen."""
    print('openrecent')
    os.system('adb shell input keyevent KEYCODE_APP_SWITCH')
    time.sleep(1)  # Allow time for recent apps to open

def dump_ui():
    """Dump current UI layout and pull XML file."""
    os.system('adb shell uiautomator dump')
    os.system('adb pull /sdcard/window_dump.xml')

def parse_ui(app_name):
    """Parse dumped XML to check if app exists and return coordinates."""
    tree = ET.parse('window_dump.xml')
    root = tree.getroot()

    for node in root.iter('node'):
        if app_name.lower() in node.attrib.get('content-desc', '').lower() or app_name.lower() in node.attrib.get('text', '').lower():
            bounds = node.attrib['bounds']
            coords = re.findall(r'\d+', bounds)
            x = (int(coords[0]) + int(coords[2])) // 2
            y = (int(coords[1]) + int(coords[3])) // 2
            print(f"Found {app_name} at: {x}, {y}")
            return x, y
    return None

def swipe_left():
    """Swipe left gesture."""
    os.system('adb shell input swipe 150 880 630 880 300')
    time.sleep(1)

def tap_recent_app(app_name):
    """Open recent apps and tap on the specific app."""
    open_recent_apps()  # Open recent apps first
    max_swipes = 5
    print('Opening Recent' , app_name)
    speak('Opening Recent' , app_name)
    # eel.DisplayMessage('Opening Recent' , app_name)
    for i in range(max_swipes):
        dump_ui()
        coords = parse_ui(app_name)
        if coords:
            x, y = coords
            os.system(f'adb shell input tap {x} {y}')
            print(f"Tapped on {app_name}.")
            speak(f"Tapped on {app_name}.")
            eel.DisplayMessage(f"Tapped on {app_name}.")
            return
        else:
            print(f"{app_name} not found, swiping left...")
            swipe_left()

    print(f"Failed to find {app_name} after {max_swipes} swipes.")
    speak(f"Failed to find {app_name} after {max_swipes} swipes.")
    eel.DisplayMessage(f"Failed to find {app_name} after {max_swipes} swipes.")

# closing all the recent app 

def find_close_all():
    tree = ET.parse('window_dump.xml')
    root = tree.getroot()

    for node in root.iter('node'):
        if 'clear all' in node.attrib.get('content-desc', '').lower() or \
           'clear all' in node.attrib.get('text', '').lower() or \
           'close all' in node.attrib.get('content-desc', '').lower() or \
           'close all' in node.attrib.get('text', '').lower():
            bounds = node.attrib['bounds']
            coords = re.findall(r'\d+', bounds)
            x = (int(coords[0]) + int(coords[2])) // 2
            y = (int(coords[1]) + int(coords[3])) // 2
            return x, y
    return None

def close_all_apps():
    print("Opening recent apps...")
    # eel.DisplayMessage("Opening recent apps...")
    speak("Opening recent apps...")
    open_recent_apps()
    dump_ui()
    
    coords = find_close_all()

    if coords:
        x, y = coords
        os.system(f'adb shell input tap {x} {y}')
        print("Closed all apps!")
        speak("Closed all apps!")
        # print("Closed all apps!")
    else:
        print("Close All button not found!")
        eel.DisplayMessage("Close All button not found!")
        speak("Close All button not found!")


# closed any specific app from recent apps 

# ------------------- ADB Utility Functions -------------------

def open_recent_apps():
    """Open recent apps screen."""
    os.system('adb shell input keyevent KEYCODE_APP_SWITCH')
    time.sleep(1)

def dump_ui():
    """Dump current UI hierarchy and pull it."""
    os.system('adb shell uiautomator dump /sdcard/window_dump.xml')
    os.system('adb pull /sdcard/window_dump.xml')
    time.sleep(0.5)

# ------------------- Swipe Function -------------------

def swipe_right():
    """Swipe right to move to the next recent app."""
    print("Swiping to the next app...")
    os.system('adb shell input swipe 200 1240 900 1240 300')  # Adjust these based on device resolution
    time.sleep(1)

# ------------------- App Coordinate Finder -------------------

def find_app_coordinates(app_name):
    """Parse UI and find app coordinates by app_name."""
    try:
        tree = ET.parse('window_dump.xml')
        root = tree.getroot()

        for node in root.iter('node'):
            content_desc = node.attrib.get('content-desc', '').lower()
            text_attr = node.attrib.get('text', '').lower()

            if app_name.lower() in content_desc or app_name.lower() in text_attr:
                bounds = node.attrib['bounds']
                coords = re.findall(r'\d+', bounds)
                x = (int(coords[0]) + int(coords[2])) // 2
                y = (int(coords[1]) + int(coords[3])) // 2
                return (x, y)
    except Exception as e:
        print(f"Error parsing XML: {e}")
    
    return None

# ------------------- Main Function -------------------

def close_specific_recent_app(app_name):
    go_home()
    """Close specific app in recent apps by checking and swiping one by one."""
    open_recent_apps()
    attempts = 0
    max_attempts = 10  # Avoid infinite loop if app not found

    while attempts < max_attempts:
        dump_ui()
        coords = find_app_coordinates(app_name)
        print(f"Searching... {app_name}")
        speak(f"Searching... {app_name}")
        # eel.DisplayMessage(f"Searching... {app_name}")
        if coords:
            x, y = coords
            y=y+900
            print(f"Closing {app_name} by swiping up at ({x}, {y})...")
            speak(f"Closing {app_name}...")
            # eel.DisplayMessage(f"Closing {app_name}...")
            os.system(f'adb shell input swipe {x} {y} {x} 0 300')
            go_home()  # Swipe up to close app
            return  # App closed, exit function
        else:
            print(f"{app_name} not found yet, moving to next app...")
            speak(f"{app_name} not found yet, moving to next app...")
            # eel.DisplayMessage(f"{app_name} not found yet, moving to next app...")
            swipe_right()  # Move to next recent app
            attempts += 1

    # If max attempts reached, app not found
    print(f"{app_name} not found in recent apps.")
    speak(f"{app_name} not found in recent apps.")
    # eel.DisplayMessage(f"{app_name} not found in recent apps.")

# ------------------- App Name Extractor -------------------

# Known apps list (expand as needed)
known_apps = ['YouTube', 'WhatsApp', 'Instagram', 'Facebook', 'Chrome', 'Gmail', 'Gallery', 'Messages']

def extract_app_name(query):
    """Extract known app name from query."""
    for app in known_apps:
        if app.lower() in query.lower():
            return app
    return None

# ------------------- Example Usage -------------------

# query = "Close YouTube"
# app_name = extract_app_name(query)
# if app_name:
#     close_specific_recent_app(app_name)
# else:
#     print("No known app name found in query.")
