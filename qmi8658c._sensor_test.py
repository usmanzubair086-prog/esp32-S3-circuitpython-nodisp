# CircuitPython Main Program (code.py)
#
# This script first ensures the TFT display is fully shut down
# to conserve power, then initializes and reads data from the
# QMI8658C IMU sensor (Accelerometer, Gyro, and Temp) via I2C.
#
# PREREQUISITE LIBRARIES (Must be in your lib folder):
# 1. qmi8658c (User's specific library name/structure)

import board
import time
import busio       # busio is implicitly required for board.I2C()
import displayio
import digitalio   # Needed for backlight control
import qmi8658c    # User's specified IMU library

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
print("-" * 40)


# --- 2. Sensor Setup ---

# Initialize the I2C bus using the board's default I2C setup (board.SCL/board.SDA)
try:
    i2c = board.I2C()
    print("I2C bus initialized successfully.")
except Exception as e:
    print(f"Error initializing I2C bus: {e}")
    # Halt program if I2C fails
    while True:
        time.sleep(1)

# Initialize the QMI8658C sensor object using the user's specific module structure
try:
    sensor = qmi8658c.QMI8658C(i2c)
    print("QMI8658C IMU sensor found and initialized.")
except Exception as e:
    print(f"An unexpected error occurred during QMI8658C initialization: {e}")
    print("Check if the 'qmi8658c' library is correctly installed and named.")
    while True:
        time.sleep(5)


# --- 3. Main Loop: Read and Print Data ---

print("Starting QMI8658C data logger...")

while True:
    try:
        # Get acceleration data in m/s^2
        acc_x, acc_y, acc_z = sensor.acceleration
        
        # Get gyroscope data in degrees/s
        gyro_x, gyro_y, gyro_z = sensor.gyro
        
        # Get temperature data
        temperature = sensor.temperature

        # Print data using user's requested format
        print("-" * 40)
        print("Acceleration: (%.2f, %.2f, %.2f) m/s^2" % (acc_x, acc_y, acc_z))
        print("Gyroscope:    (%.2f, %.2f, %.2f) degrees/s" % (gyro_x, gyro_y, gyro_z))
        print("Temperature:  %.2f °C" % temperature)
        print("-" * 40)

    except Exception as e:
        print(f"Error reading sensor data: {e}")

    # Add a delay to prevent flooding the serial monitor (0.5s)
    time.sleep(0.5)
