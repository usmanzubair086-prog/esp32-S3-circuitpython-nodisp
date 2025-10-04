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
import random      # Needed for the unique "Fire Flicker" effect

# --- Color/Effect Definitions ---
# The Fire Flicker effect simulates a flame using randomized warm colors and brightness.
MAX_BRIGHTNESS = 0.6         # Peak brightness for the flicker
MIN_BRIGHTNESS = 0.1         # Minimum brightness
FLICKER_DELAY = 0.03         # Time delay between flickers (controls speed)


# --- 1. Display Shutdown (Power Saving) ---

print("Starting power-saving routine: Disabling TFT Display.")

# A. Release Software Resources
try:
    displayio.release_displays()
    print("  -> Display software resources released.")
except Exception:
    pass # Ignore errors if displayio is not fully fully initialized

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
        brightness=MIN_BRIGHTNESS, # Start at minimum brightness
        auto_write=False
    )
    print("NeoPixel initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not initialize NeoPixel: {e}")
    # Halt program if NeoPixel setup fails
    while True:
        time.sleep(1)


# --- 3. Main Loop: NeoPixel Animation ---

print("Starting NeoPixel Fire Flicker effect...")

def random_fire_color():
    """Generates a random warm color tuple (R, G, B)"""
    # Red component is always high (150-255)
    r = random.randint(150, 255)
    
    # Green component gives the orange/yellow tint (0-100)
    g = random.randint(0, 100) 
    
    # Blue component is always zero
    b = 0
    return (r, g, b)

def random_fire_brightness():
    """Generates a random brightness value within the defined range"""
    # Generates a float between MIN_BRIGHTNESS and MAX_BRIGHTNESS
    return random.uniform(MIN_BRIGHTNESS, MAX_BRIGHTNESS)

while True:
    # 1. Set a random warm color
    pixels[0] = random_fire_color()
    
    # 2. Set a random brightness level
    pixels.brightness = random_fire_brightness()
    
    # 3. Update the pixel
    pixels.show()
    
    # 4. Wait a short, random amount of time for a less predictable flicker
    time.sleep(random.uniform(FLICKER_DELAY * 0.5, FLICKER_DELAY * 1.5))
