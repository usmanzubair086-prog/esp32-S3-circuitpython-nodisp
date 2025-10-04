# CircuitPython Main Program (code.py)
#
# This script first ensures the TFT display is fully shut down
# to conserve power, then initializes and reads data from the
# BMP280 temperature and pressure sensor via I2C.
#
# PREREQUISITE LIBRARIES (Must be in your lib folder):
# 1. adafruit_bus_device
# 2. adafruit_bmp280

import board
import time
import busio
import displayio
import digitalio # Needed for backlight control
import adafruit_bmp280

# --- 1. Display Shutdown (Power Saving) ---

print("Starting power-saving routine: Disabling TFT Display.")

# A. Release Software Resources
try:
    displayio.release_displays()
    print("  -> Display software resources released.")
except Exception:
    pass # Ignore errors if displayio is not fully initialized

# B. Control Backlight Pin for Physical Power Off
try:
    # Attempt to use the standard backlight pin name for the Feather S3 TFT
    if hasattr(board, 'TFT_BACKLIGHT'):
        backlight = digitalio.DigitalInOut(board.TFT_BACKLIGHT)
        backlight.direction = digitalio.Direction.OUTPUT
        
        # Setting the pin low turns off the backlight (often wired to be active high)
        backlight.value = False
        print("  -> Backlight pin set LOW. Display should be off.")
    else:
        print("  -> WARNING: Backlight pin 'TFT_BACKLIGHT' not found.")

except Exception as e:
    print(f"FATAL ERROR during backlight control: {e}")

print("TFT Display shutdown sequence complete.")
print("-" * 30)


# --- 2. Sensor Setup ---

# Initialize the I2C bus using the default board pins (SCL and SDA)
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C bus initialized successfully.")
except Exception as e:
    print(f"Error initializing I2C bus: {e}")
    # Halt program if I2C fails
    while True:
        time.sleep(1)

# Initialize the BMP280 sensor object
try:
    # Using the fully qualified, legacy class name to resolve potential ImportErrors
    # The default I2C address is 0x77. Change to: adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x76) if needed.
    bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
    print("BMP280 sensor found and initialized.")
except ValueError:
    print("BMP280 not found at default I2C address (0x77). Check wiring or address (try 0x76).")
    while True:
        time.sleep(5)
except Exception as e:
    print(f"An unexpected error occurred during BMP280 initialization: {e}")
    while True:
        time.sleep(5)


# --- 3. Main Loop: Read and Print Data ---

print("Starting BMP280 data logger...")

while True:
    try:
        # Read sensor data
        temperature_c = bmp280.temperature
        temperature_f = (temperature_c * 9 / 5) + 32
        pressure = bmp280.pressure
        altitude = bmp280.altitude

        # Print data to the serial console (Python Interpreter)
        print("-" * 30)
        print(f"Temperature: {temperature_c:.2f} C / {temperature_f:.2f} F")
        print(f"Pressure:    {pressure:.2f} hPa")
        print(f"Altitude:    {altitude:.2f} meters")
        print("-" * 30)

    except Exception as e:
        print(f"Error reading sensor data: {e}")

    # Wait for 2 seconds before the next reading
    time.sleep(2)
