import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import requests
#Provide your IBM Watson Device Credentials
organization = "pmei26"
deviceType = "NodeMCU"
deviceId = "mcu123"
authMethod = "token"
authToken = "smarthome123"


def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        print(type(cmd.data))
        i=cmd.data['command']
        if i=='LIGHTON':
                print("LIGHT ON IS RECEIVED")
                
                
        elif i=='LIGHTOFF':
                print("LIGHT OFF IS RECEIVED")
        

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        
        hum=random.randint(0, 100)
        #print(hum)
        temp =random.randint(0, 100)
        vibration =random.randint(0, 100)
        current =random.randint(0, 100)
        #Send Temperature & Humidity to IBM Watson
        data = { 'Temperature' : temp, 'Humidity': hum, 'vibration':vibration, 'current':current }
        #print (data)
        def myOnPublishCallback():
            print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "vibration = %s %%" % vibration, "current = %s %%" % current, "to IBM Watson")

        success = deviceCli.publishEvent("Weather", "json", data, qos=0, on_publish=myOnPublishCallback)
        if(temp<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=dILKXJy2ukqBYEZT38c1mztv4VaiP7enH59hblrACpwRsUjSOxu6YSQofPVJyGkm9d30FUiHs81ACjeZ&sender_id=FSTSMS&message=Temperature is low...please switch on the LIGHT.&language=english&route=p&numbers=8217577504')
                print(r.status_code)
        if(hum<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=dILKXJy2ukqBYEZT38c1mztv4VaiP7enH59hblrACpwRsUjSOxu6YSQofPVJyGkm9d30FUiHs81ACjeZ&sender_id=FSTSMS&message=Humidity is low ....please switch on the LIGHT.&language=english&route=p&numbers=8217577504')
                print(r.status_code)
        if(vibration<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=dILKXJy2ukqBYEZT38c1mztv4VaiP7enH59hblrACpwRsUjSOxu6YSQofPVJyGkm9d30FUiHs81ACjeZ&sender_id=FSTSMS&message=The motor vibration is too high...&language=english&route=p&numbers=8217577504')
                print(r.status_code)
        if(current<50):
                r = requests.get('https://www.fast2sms.com/dev/bulk?authorization=dILKXJy2ukqBYEZT38c1mztv4VaiP7enH59hblrACpwRsUjSOxu6YSQofPVJyGkm9d30FUiHs81ACjeZ&sender_id=FSTSMS&message=The Cylinder is going to be empty.Please book it soon.&language=english&route=p&numbers=8217577504')
                print(r.status_code)
        if not success:
            print("Not connected to IoTF")
        time.sleep(2)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()

