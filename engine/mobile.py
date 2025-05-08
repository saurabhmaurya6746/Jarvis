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
   
