from datetime import datetime
import json
import requests


url = 'https://BT66EPW32IRIOCFX.anvil.app/_/private_api/GAFUXPPCWMB5WN52G4LWMXSI/upload'

def send_info(decibel):
    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    body = json.dumps({
        "datetime": dt_string,
        "decibel": decibel,
        'location':'vivo_city',
        'no_of_ppl':2   
    })

    
    request=requests.post(url, json=body)
    print(request)
    print('Sent: "' + body + '" to: "' + url + '"')

if __name__ == "__main__":
    send_info(13)