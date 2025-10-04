# CircuitPython Main Program (code.py)
#
# This script first ensures the TFT display is fully shut down
# to conserve power, then initializes the onboard NeoPixel
# and runs a color cycle animation.
#
# PREREQUISITE LIBRARIES (Must be in your lib folder):
# 1. adafruit_bus_device (still useful for other components, though not strictly needed here)
# 2. neopixel

import board
import time
import displayio
import digitalio   # Needed for backlight control
import neopixel    # Library for NeoPixel control

# --- Color Definitions for Blinking Effect ---
RED = (255, 0, 0)
BLUE = (0, 0, 255)


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


# --- 2. NeoPixel Setup ---

# Define the onboard NeoPixel. The Feather S3 TFT usually has 1 NeoPixel.
# Using 'board.NEOPIXEL' for the pin definition.
try:
    num_pixels = 1
    pixels = neopixel.NeoPixel(
        board.NEOPIXEL, 
        num_pixels, 
        brightness=0.5, # Increased brightness slightly for a clearer flash
        auto_write=False
    )
    print("NeoPixel initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not initialize NeoPixel: {e}")
    # Halt program if NeoPixel setup fails
    while True:
        time.sleep(1)


# --- 3. Main Loop: NeoPixel Animation ---

print("Starting NeoPixel Red/Blue alternating flash...")

while True:
    # Set to RED
    pixels[0] = RED
    pixels.show()
    time.sleep(0.25) # Wait a quarter second for a clear flash effect

    # Set to BLUE
    pixels[0] = BLUE
    pixels.show()
    time.sleep(0.25) # Wait a quarter second
