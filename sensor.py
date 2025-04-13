import requests
import serial

# Replace with your correct COM port (Windows: "COM3", Linux/Mac: "/dev/ttyUSB0")
arduino = serial.Serial("COM5", 9600, timeout=1)

server_url = "http://127.0.0.1:5000/fire"  # Replace with your actual server URL

while True:
    message = arduino.readline().decode().strip()  # Read from Arduino
    if message:
        print("Received:", message)
        if(message=="Alert Type: FIRE HIGH" or (message=="Flame state: HIGH (Fire Detected)")):
            response = requests.post(server_url, json={"message": message})  # Send to server
            print("Server Response:", response.status_code)
