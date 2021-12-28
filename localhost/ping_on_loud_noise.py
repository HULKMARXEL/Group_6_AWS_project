import time, math, audioop
import pyaudio

from camera import take_picture, delete_picture

from rekognition import analyze_photo

from send_info import send_info

# PyAudio Settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1

# Init PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

# Store previous data for running average
history = []

while True:
    total = 0

    #Now we read data from device for around one second
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)

        #oreo_sound.append(data)
        if True:
            reading = audioop.max(data, 2)
            total += reading
        
        time.sleep(.0001)

    # Converts sound data into "decibel" scale
    total = math.log(total)

    # Clear old history
    if len(history) >= 60:
        history.pop(0)

    # Update history
    history.append(total)

    # Running average
    avg = sum(history) / len(history)
    print(avg)

    if avg > 11:
        pic_path = take_picture()

        info = analyze_photo(pic_path)

        info['decibel'] = avg

        send_info(info)

        delete_picture(pic_path)