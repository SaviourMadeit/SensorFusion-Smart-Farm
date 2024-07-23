from machine import ADC, Pin, I2C, RTC 
from Lcd16x2 import LCD
from dht import DHT11 #InvalidPulseCount
import network                        
import utime                          
import BlynkLib    # interacting with Blynk server
import os          # Add the 'os' module for file operations

"""
Initialize the sensor and Actuator on the given GPIO pin.

:param pin_number: GPIO pin number to which the sensor is connected
:return: ADC, Pin object
"""
# Initialize sensors
adc_soil_moisture = ADC(Pin(26))
adc_light = ADC(Pin(27))
adc_soil_temp = ADC(Pin(28))
dht = DHT11(Pin(16, Pin.IN, Pin.PULL_UP))

'''
# these objects are not in use for now
adc_npk = ADC(Pin(30))
adc_co2 = ADC(Pin(31))
adc_soil_ph = ADC(Pin(29))
bme_sensor = bme280.BME280(I2C(0))
'''

# Actuator pins
pump = Pin(15, Pin.OUT) # Water Pump
lamp = Pin(13, Pin.OUT) # Artificial Lamp
vent = Pin(14, Pin.OUT) # Ventilation Fan
heat = Pin(12, Pin.OUT) # Heating device

#Set all devices in OFF Mode
pump.low()
lamp.low()
vent.low()

rtc = RTC()  # Initialize the RTC

# File and network setup
SENSOR_DATA_FILE = 'data.csv'  # File for storing sensor data
CREDENTIALS_FILE = 'wifi_credentials.txt'  #Create Wifi-network Connection Accessibility
BLYNK_AUTH = "xxxxxxxxxxxx"  # Blynk cloud token
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# Crop data storage
crops_data = {}

# Calibration maximum and minimum values
adc_full_scale = 65535

# Store Wifi credentials
def save_credentials(ssid, key):
    with open(CREDENTIALS_FILE, 'w') as f:
        f.write(f'SSID: {ssid}\nPASS: {key}\n')

# Initialize current credentials for wifi accessibily
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, 'r') as f:
            ssid = f.readline().strip().split(': ')[1]
            key = f.readline().strip().split(': ')[1]
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
    try:
        adc_value = adc_soil_moisture.read_u16()
        moisture = (adc_value / adc_full_scale) * 100
        print(f"Moisture Level: {moisture:.2f}% (ADC Value: {adc_value})")
        return moisture
    except Exception as e:
        print(f"Error reading moisture: {e}")
        return None

def read_light_intensity():
    try:
        adc_value = adc_light.read_u16()
        adc_light_intensity = (adc_value / adc_full_scale) * 100
        print(f"Light Intensity: {adc_light_intensity:.2f}%")
        return adc_light_intensity
    except Exception as e:
        print(f"Error reading light intensity: {e}")
        return None

def read_soil_temp():
    try:
        adc_value = adc_soil_temp.read_u16()
        soil_temp = (adc_value / adc_full_scale) * 100  # Adjust as needed for temperature scale
        print(f"Soil Temperature: {soil_temp:.2f}°C")
        return soil_temp
    except Exception as e:
        print(f"Error reading soil temperature: {e}")
        return None

def dht_sensor_value():
    try:
        sensor = DHT11(dht)
        sensor.measure()
        temperature = sensor.temperature()
        humidity = sensor.humidity()
        print(f"Temp: {temperature}°C, Humidity: {humidity}%")
        return temperature, humidity
    except Exception as e:
        print(f"Error reading DHT values: {e}")
        return None, None




# Function declearation not in use uncomment when in use
'''
def read_soil_ph():
    try:
        adc_value = adc_soil_ph.read_u16()
        soil_ph = (adc_value / adc_full_scale) * 14  # Assuming pH range is 0-14
        print(f"Soil pH: {soil_ph:.2f}")
        return soil_ph
    except Exception as e:
        print(f"Error reading soil pH: {e}")
        return None

def read_npk():
    try:
        npk_values = [adc_npk.read_u16() for _ in range(3)]  # Adjust for NPK sensors
        print(f"NPK Levels: Nitrogen: {npk_values[0]}, Phosphorus: {npk_values[1]}, Potassium: {npk_values[2]}")
        return npk_values
    except Exception as e:
        print(f"Error reading NPK values: {e}")
        return None

def read_co2():
    try:
        adc_value = adc_co2.read_u16()
        co2_level = (adc_value / adc_full_scale) * 1000  # Adjust as needed for CO2 concentration
        print(f"CO2 Concentration: {co2_level:.2f} ppm")
        return co2_level
    except Exception as e:
        print(f"Error reading CO2 concentration: {e}")
        return None
'''
# Take User Input on Specific Crop data 
def input_crop_data():
    global crops_data
    crop_name = input("Enter crop name: ")
    light_intensity = float(input("Enter ideal light intensity (percentage): "))
    moisture_level = float(input("Enter ideal soil moisture level (percentage): "))
    temp_min = float(input("Enter minimum soil temperature (°C): "))
    temp_max = float(input("Enter maximum soil temperature (°C): "))
    temp_min_air = float(input("Enter minimum air temperature (°C): "))
    temp_max_air = float(input("Enter maximum air temperature (°C): "))
    humidity_min = float(input("Enter minimum air humidity (%): "))
    humidity_max = float(input("Enter maximum air humidity (%): "))
        #ph_min = float(input("Enter minimum soil pH level: "))
    #ph_max = float(input("Enter maximum soil pH level: "))
    #npk_nitrogen = float(input("Enter ideal Nitrogen level: "))
    #npk_phosphorus = float(input("Enter ideal Phosphorus level: "))
    #npk_potassium = float(input("Enter ideal Potassium level: "))
    #co2_level = float(input("Enter ideal CO2 concentration (ppm): "))

    growth_stages = {
        "seedling": {
            "light": light_intensity * 0.8,
            "moisture": moisture_level * 0.8,
            "temp_min": temp_min,
            "temp_max": temp_max,
            #"ph_min": ph_min,
            #"ph_max": ph_max,
            #"npk": [npk_nitrogen * 0.8, npk_phosphorus * 0.8, npk_potassium * 0.8],
            #"co2": co2_level * 0.8
        },
        "vegetative": {
            "light": light_intensity,
            "moisture": moisture_level,
            "temp_min": temp_min,
            "temp_max": temp_max,
            #"ph_min": ph_min,
            #"ph_max": ph_max,
            #"npk": [npk_nitrogen, npk_phosphorus, npk_potassium],
            #"co2": co2_level
        },
        "flowering": {
            "light": light_intensity * 1.2,
            "moisture": moisture_level * 0.8,
            "temp_min": temp_min,
            "temp_max": temp_max,
            #"ph_min": ph_min,
            #"ph_max": ph_max,
            #"npk": [npk_nitrogen * 1.2, npk_phosphorus * 1.2, npk_potassium * 1.2],
            #"co2": co2_level * 1.2
        }
    }
    
    crops_data[crop_name] = {
        "growth_stages": growth_stages
    }

def control_environment(crop_name, growth_stage):
    if crop_name not in crops_data:
        print(f"Crop '{crop_name}' not found.")
        return

    stage_data = crops_data[crop_name]["growth_stages"].get(growth_stage, {})
    
    if not stage_data:
        print(f"Growth stage '{growth_stage}' not found for crop '{crop_name}'.")
        return


    # Create objects for various sensor data functions
    moisture = read_moisture()
    light = read_light_intensity()
    soil_temp = read_soil_temp()
    air_temp, humidity = dht_sensor_value()
    #soil_ph = read_soil_ph()
    #npk = read_npk()
    #co2 = read_co2()

    if moisture is not None and moisture < stage_data["moisture"]:
        pump.high()
        print("Pump ON")
    else:
        pump.low()
        print("Pump OFF")

    if light is not None and light < stage_data["light"]:
        lamp.high()
        print("Lamp ON")
    else:
        lamp.low()
        print("Lamp OFF")

    if air_temp is not None and humidity is not None:
            if air_temp < stage_data["temp_min_air"] or air_temp > stage_data["temp_max_air"]:
                vent.high()
                print("Vent ON for air temperature")
            else:
                vent.low()
                print("Air temperature within range")
            
            if humidity < stage_data["humidity_min"] or humidity > stage_data["humidity_max"]:
                print("Adjust humidity")
    else:
        print("Humidity within range")
    '''
    if soil_temp is not None:
        if soil_temp < stage_data["temp_min"] or soil_temp > stage_data["temp_max"]:
            heat.high()  # Example control for temperature; adjust as needed
            print("Vent ON")
        else:
            heat.low()
            print("Vent OFF")

    if soil_ph is not None:
        if soil_ph < stage_data["ph_min"] or soil_ph > stage_data["ph_max"]:
            print("Adjust soil pH") # Placeholder action; implement specific control

     if npk is not None:
        if any(npk[i] < stage_data["npk"][i] for i in range(3)):
            print("Add fertilizer")  # Placeholder action; implement specific control
        else:
            print("NPK levels within range")
    
    if co2 is not None:
        if co2 < stage_data["co2"]:
            print("Increase CO2")  # Placeholder action; implement specific control
        else:
            print("CO2 levels within range")
    '''

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

    # Take Crop data, manage and control sensor parameters for Crop growth
    crop_name = input("Enter the crop name: ")
    growth_stage = input("Enter the growth stage (seedling, vegetative, flowering): ")
    
    input_crop_data()
    control_environment(crop_name, growth_stage)

#Run main Loop
if __name__ == '__main__':
    main()



