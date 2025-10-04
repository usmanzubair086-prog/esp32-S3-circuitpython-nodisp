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
        brightness=0.3, # Keep brightness moderate
        auto_write=False
    )
    print("NeoPixel initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not initialize NeoPixel: {e}")
    # Halt program if NeoPixel setup fails
    while True:
        time.sleep(1)

# Helper function to convert wheel position (0-255) to an RGB color tuple
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int(pos * 3), int(255 - pos * 3), 0)
    if pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    pos -= 170
    return (0, int(pos * 3), int(255 - pos * 3))


# --- 3. Main Loop: NeoPixel Animation ---

print("Starting NeoPixel color cycle...")
i = 0

while True:
    # Cycle the color of the single NeoPixel
    color = wheel(i & 255)
    pixels[0] = color
    pixels.show()

    # Increment the color wheel index
    i += 1
    if i > 255:
        i = 0
    
    # Fast update rate for smooth animation
    time.sleep(0.01)
