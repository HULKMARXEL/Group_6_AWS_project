import time, math, audioop, pyaudio, csv, uuid
from datetime import datetime
from S3 import upload_to_aws
from forecast import forecast_data

identifier = str(uuid.uuid4())

print(identifier + " is online")

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

header = ["item_id", "timestamp", "target_value"]

f = open('store.csv', 'w', newline='')
writer = csv.writer(f)

# write the header
writer.writerow(header)

for id in range(10 * 60):
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

    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    
    writer.writerow([identifier, dt_string, avg])

f.close()

upload_to_aws("store.csv", 'group-6-marxel-train-data', identifier + ".csv")

forecast_data(identifier)