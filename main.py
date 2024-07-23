from machine import ADC, Pin, I2C, RTC
from Lcd16x2 import LCD
from dht import DHT11 #InvalidPulseCount
import network
import utime
import BlynkLib    # interacting with Blynk server
import os          # Add the 'os' module for file operations

"""
Initialize the sensora on the given GPIO pin.

:param pin_number: GPIO pin number to which the sensor is connected
:return: ADC, Pin object
"""
# Define the GPIO pins for the device pins
adc_light = ADC(Pin(28))  # type: ignore # Check light intensity around 
adc_soil = ADC(Pin(26))       # Check moisture level in soil
adc_full_scale = 65535          # Full-scale range of the ADC (2^16 - 1 for a 16-bit ADC)


# ACTUATORS OBJECT INPUT & OUTPUT PINS
pump = Pin(15, Pin.OUT)
lamp = Pin(13, Pin.OUT)
vent = Pin(14, Pin.OUT)
dht = DHT11(Pin(16, Pin.IN, Pin.PULL_UP))  # dht11 temperature/humidity sensor

#Set all devices in OFF Mode
pump.low()
lamp.low()
vent.low()

rtc = RTC()  # Initialize the RTC

SENSOR_DATA_FILE = 'data' # create a file directory to store sensor data in csv format.

# Calibration maximum and minimum values
min_moist = '00000000000'  # Enter Minimum Water level here.
max_moist = '00000000000'  # Enter Maximum water level here.

'''
# Blynk authentication token and Initialize Blynk
BLYNK_AUTH = "xxxxxxxxxxxx"  #Enter your blynk cloud token here example: oj-D5CbRpVO5VWZnFFVq4j4N_SmsVxLn
blynk = BlynkLib.Blynk(BLYNK_AUTH)
'''

#Create Wifi-network Connection Accessibility
CREDENTIALS_FILE = 'wifi_credentials.txt'
# Store Wifi credentials
def save_credentials(ssid, key):
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f'{ssid}\n{key}\n')

# Initialize current credentials for wifi accessibily
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            ssid = f.readline().strip()
            key = f.readline().strip()
        return ssid, key
    except OSError:
        return None, None
# Coonect to the Availabel router
def do_connect(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, key)
        for _ in range(15):  # Attempt to connect for 15 seconds
            if wlan.isconnected():
                break
            utime.sleep(1)
            print('Trying to connect...')
    if wlan.isconnected():
        print('Network config:', wlan.ifconfig())
        print('Connected.')
        utime.sleep(2)
        return True
    else:
        print('Failed to connect.')
        return False

#Read moisture sensor values
def read_moisture():

    """
    Read the moisture value from the sensor.
    
    :param adc: ADC object initialized for the moisture sensor
    :return: Moisture level as an integer value
    """

    # Read the analog value from the sensor (0-65535 for 16-bit ADC)
    adc_value = adc_soil.read_u16()

    # Convert raw value to a percentage (assuming 0 is fully dry and 65535 is fully wet)
    #moisture = (max_moist - adc_value)*100/(max_moist-min_moist)  
    moisture = (adc_value / adc_full_scale) * 100
    # print values
    #print("moisture: " + "%.2f" % moisture +"% (adc: "+str(adc_value)+")")
    print(f"Moisture Level: {moisture:.2f}%")
    return moisture

#Function for Triggering Water Pump
def trigger_pump():
            
            threshold = read_moisture()
            if threshold < 50:
                 pump.high()
            else:
                pump.low()
            utime.sleep(5)


def read_light_intensity():
    adc_light = ADC(Pin(28)) # get photo data
    light_value = (adc_light / adc_full_scale) * 100 # type: ignore






















# Function for Checking connections
def maintain_connection(ssid, key):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while True:
        if not wlan.isconnected():
            print('Connection lost. Reconnecting...')
            wlan.connect(ssid, key)
            for _ in range(15):  # Attempt to reconnect for 15 seconds
                if wlan.isconnected():
                    break
                utime.sleep(1)
                print('Reconnecting...')
        else:
            print('Connection Established.')
        utime.sleep(10)  # Check connection status every 10 seconds

# Main Loop 
def main():
    ssid, key = load_credentials()
    if ssid and key:
        print(f'Found stored credentials for SSID: {ssid}')
        if not do_connect(ssid, key):
            ssid = input("Enter Wifi SSID: ")
            key = input("Enter Wifi PASSWORD: ")
            if do_connect(ssid, key):
                save_credentials(ssid, key)
    else:
        ssid = input("Enter Wifi SSID: ")
        key = input("Enter Wifi PASSWORD: ")
        if do_connect(ssid, key):
            save_credentials(ssid, key)
    
    # Maintain connetion
    maintain_connection(ssid, key)

    # Read Plant Soil Moisture Level
    read_moisture()
    # Trigger water Pump ON/OFF based on the moisture threshold 
    trigger_pump()

#Run main Loop
if __name__ == '__main__':
    main()



