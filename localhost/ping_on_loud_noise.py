import time, math, audioop
import pyaudio

from camera import take_picture, delete_picture

from rekognition import analyze_photo

from send_info import send_info

#Initialisation for PyAudio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5

#Object
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
 
while True:
    total=0

    #Now we read data from device for around one second
    for i in range(0,2):
        #l,data = inp.read()
        data = stream.read(CHUNK)

        #oreo_sound.append(data)
        if True:
            reading = audioop.max(data, 2)
            total += reading
        
        time.sleep(.0001)

    #any scaling factor
    total = math.log(total)

    if total > 11:
        pic_path = take_picture()

        info = analyze_photo(pic_path)

        info['decibel'] = total

        send_info(info)

        delete_picture(pic_path)