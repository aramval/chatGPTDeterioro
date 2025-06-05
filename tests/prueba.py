import serial

try:
    arduino = serial.Serial('COM4', 9600, timeout=1)
    print("✅ Puerto COM4 abierto correctamente")
    arduino.close()
except Exception as e:
    print(f"❌ Error: {e}")
