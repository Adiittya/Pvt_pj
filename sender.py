import minimalmodbus
import requests
import json
import time
from gpiozero import OutputDevice

# Set up the GPIO pin
relay = OutputDevice(18)  # Change this to the actual GPIO pin connected to your relay

def read_modbus_data():
    try:
        values = instrument.read_registers(1, 2, functioncode=4)
        temperature = values[0] / 10.0
        humidity = values[1] / 10.0

        # Control the relay based on the temperature
        if temperature > 30:  # Change this to your desired temperature threshold
            relay.on()
            relay_status = "ON"
        else:
            relay.off()
            relay_status = "OFF"

        return {"temperature": temperature, "humidity": humidity, "relay_status": relay_status}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    port = 'COM7'  # Change this to the actual serial port on your device
    baudrate = 9600
    stopbits = 1
    bytesize = 8
    parity = minimalmodbus.serial.PARITY_NONE
    instrument = minimalmodbus.Instrument(port, slaveaddress=1)
    instrument.serial.baudrate = baudrate
    instrument.serial.bytesize = bytesize
    instrument.serial.stopbits = stopbits
    instrument.serial.parity = parity

    server_address = 'http://13.60.37.152:5000/receive_data'  # Corrected URL

    while True:
        # Read Modbus data
        modbus_data = read_modbus_data()

        # Send data to the Flask server
        try:
            response = requests.post(server_address, data=json.dumps(modbus_data), headers={'Content-type': 'application/json'})
            if response.status_code == 200:
                print("Data sent successfully.")
            else:
                print(f"Failed to send data. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error sending data: {e}")

        # Wait for a short duration before reading Modbus data again
        time.sleep(1)
