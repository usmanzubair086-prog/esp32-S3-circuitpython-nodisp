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

# --- Color/Effect Definitions ---
PULSE_COLOR = (128, 0, 128)  # A medium intensity Purple
MAX_BRIGHTNESS = 0.6         # Peak brightness for the pulse
FADE_RATE = 0.02             # How quickly the brightness changes per step
PULSE_SPEED = 0.01           # Delay between brightness changes (controls smoothness)


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
        brightness=0.0, # Start at zero brightness
        auto_write=False
    )
    # Set the color of the pixel once
    pixels[0] = PULSE_COLOR
    print("NeoPixel initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not initialize NeoPixel: {e}")
    # Halt program if NeoPixel setup fails
    while True:
        time.sleep(1)


# --- 3. Main Loop: NeoPixel Animation ---

print("Starting NeoPixel Purple Pulsing (Breathing) effect...")

current_brightness = 0.0

while True:
    # --- Fade In (0.0 to MAX_BRIGHTNESS) ---
    while current_brightness < MAX_BRIGHTNESS:
        current_brightness += FADE_RATE
        if current_brightness > MAX_BRIGHTNESS:
            current_brightness = MAX_BRIGHTNESS
        
        pixels.brightness = current_brightness
        pixels.show()
        time.sleep(PULSE_SPEED)

    # --- Fade Out (MAX_BRIGHTNESS to 0.0) ---
    while current_brightness > 0.0:
        current_brightness -= FADE_RATE
        if current_brightness < 0.0:
            current_brightness = 0.0
        
        pixels.brightness = current_brightness
        pixels.show()
        time.sleep(PULSE_SPEED)
