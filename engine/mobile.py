import os
import datetime
import eel
from engine.commands import speak
import re
import datetime
import xml.etree.ElementTree as ET
import re
import time
import subprocess

import os
import datetime

def take_screenshot():
    print('hhhhh')
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"screen_{timestamp}.png"
    result = os.system(f'adb shell screencap -p /sdcard/Pictures/{filename}')
    
    if result == 0:
        print(f"Screenshot saved as {filename}")
        os.system(f'adb pull /sdcard/Pictures/{filename} ./')  # Uncomment to pull to PC
    else:
        print("Failed to take screenshot. Is device connected?")

# Battery Level & Status Checker
def battery_status():
    # Run adb command and get output
    battery_info = os.popen('adb shell dumpsys battery').read()

    # Go line by line to find 'level'
    for line in battery_info.splitlines():
        if 'level' in line:
            battery_level = line.strip().split(":")[1].strip()
            print(f"Battery Percentage: {battery_level}%")
            speak(f" Battery Percentage: {battery_level}%")
            eel.DisplayMessage(f"Battery Percentage: {battery_level}%")
            return battery_level

# Auto Brightness Controller
def set_brightness(input_string):
    level = extract_brightness_level_number(input_string)
    print(level)
    os.system(f'adb shell settings put system screen_brightness {level}')
    print(f"Brightness set to {level}")
    speak(f"Brightness set to {level}")
    eel.DisplayMessage(f"Brightness set to {level}")

def extract_brightness_level_number(input_string):
    match = re.search(r'\d+', input_string)
    if match:
        return int(match.group())
    else:
        raise ValueError("No number found in the input string.")

# set valume at any fixed level
def set_volume(level):
    level = extract_brightness_level_number(level)
    print(level)
    os.system(f'adb shell media volume --stream 3 --set {level}')
    print(f"Volume set to {level}")
    speak(f"Volume set to {level}")
    eel.DisplayMessage(f"Volume set to {level}")

# wifi handling 
def toggle_wifi_true(on=True):
    state = 'enable' if on else 'disable'
    os.system(f'adb shell svc wifi {state}')
    print(f"WiFi {'enabled' if on else 'disabled'}")

def toggle_wifi_false(on=False):
    state = 'enable' if on else 'disable'
    os.system(f'adb shell svc wifi {state}')
    print(f"WiFi {'enabled' if on else 'disabled'}")


# calling funcationlity
def reject_call():
    os.system('adb shell input keyevent KEYCODE_ENDCALL')
    print("Incoming call rejected.")

def accept_call():
    os.system('adb shell input keyevent KEYCODE_CALL')
    print("Incoming call accepted.")

# turn on mobile data 
def toggle_mobile_data_on(on=True):
    os.system(f'adb shell svc data enable')

#turn off mobile data 
def toggle_mobile_data_off(on=True):
    os.system(f'adb shell svc data disable')
    


# Smart Night Mode Scheduler
def set_night_mode():
    current_hour = datetime.now().hour
    if current_hour >= 22:  # After 10 PM
        # Lower screen brightness
        os.system('adb shell settings put system screen_brightness 10')
        # Mute phone
        os.system('adb shell settings put system volume_ring 0')
        os.system('adb shell settings put system volume_music 0')
        os.system('adb shell settings put system volume_alarm 0')
        # Enable Do Not Disturb (DND)
        os.system('adb shell settings put global zen_mode 1')
    else:
        print("It's not time for night mode yet.")


# bluetooth asnimation
def turn_on_bluetooth():
    """
    Turns on Bluetooth on the connected Android device.-
    """
    os.system('adb shell service call bluetooth_manager 6')
    print("Bluetooth enabled.")
    speak("Bluetooth enabled.")
    eel.DisplayMessage("Bluetooth enabled.")

def turn_off_bluetooth():
    """
    Turns off Bluetooth on the connected Android device.
    """
    os.system('adb shell service call bluetooth_manager 8')
    print("Bluetooth disabled.")
    speak("Bluetooth disabled.")
    eel.DisplayMessage("Bluetooth disabled.")


# open any app on screen

def get_recent_app_coordinates(app_name):
    print('ggg')
    # Dump UI hierarchy
    os.system('adb shell uiautomator dump /sdcard/window_dump.xml')
    os.system('adb pull /sdcard/window_dump.xml')

    # Parse XML
    tree = ET.parse('window_dump.xml')
    root = tree.getroot()
    print('hhhhh')
    for node in root.iter('node'):
        if app_name.lower() in node.attrib.get('content-desc', '').lower() or app_name.lower() in node.attrib.get('text', '').lower():
            bounds = node.attrib['bounds']
            coords = re.findall(r'\d+', bounds)
            x = (int(coords[0]) + int(coords[2])) // 2
            y = (int(coords[1]) + int(coords[3])) // 2
            print(f"Found {app_name} at: {x}, {y}")
            return x, y
    print(f"{app_name} not found in Recent Apps.")
    return None

def tap_recent_app(app_name):
    # print('gggggggggggggggggggggg')
    coords = get_recent_app_coordinates(app_name)
    print(coords)
    if coords:
        x, y = coords
        os.system(f'adb shell input tap {x} {y}')
        print(f"Tapped on {app_name}.")
    else:
        print(f"{app_name} not found.")
    


# reading the latest sms 
def get_latest_sms():
    print('gggg')
    try:
        # Run ADB command to get latest SMS (Inbox)
        result = subprocess.run(["adb", "shell", "content query --uri content://sms/inbox --projection address,body,date --sort 'date DESC' --limit 1"],
                                capture_output=True, text=True)
        
        output = result.stdout.strip()
        print(output)
        
        if not output:
            print("No messages found.")
            return None, None

        # Extract sender and message using regex
        sender_match = re.search(r"address=(.*?),", output)
        message_match = re.search(r"body=(.*?),", output)

        sender = sender_match.group(1) if sender_match else "Unknown"
        message = message_match.group(1) if message_match else "No message content"

        print(f"Sender: {sender}")
        print(f"Message: {message}")

        return sender, message

    except Exception as e:
        print(f"Error: {e}")
        return None, None