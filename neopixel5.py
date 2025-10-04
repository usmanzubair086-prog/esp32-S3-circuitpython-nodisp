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
# Removed 'random' as it is not needed for this effect

# --- Color/Effect Definitions (Ocean Wave) ---
# Simulates a gentle ocean wave by smoothly cycling between blue and cyan.
WAVE_SPEED = 0.02           # Delay between color steps (controls speed/smoothness)
BRIGHTNESS = 0.5            # Fixed brightness for smooth color transitions
color_step = 0              # Global variable to track the position in the color cycle


def ocean_wheel(pos):
    """Generates a color that cycles between deep blue and bright cyan/aqua."""
    pos = pos % 256
    
    if pos < 128:
        # Blue to Cyan (Green component fades in)
        g = pos * 2
        return (0, g, 255)
    else:
        # Cyan back to Blue (Green component fades out)
        pos -= 128
        g = 255 - pos * 2
        return (0, g, 255)


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
        brightness=BRIGHTNESS, # Set fixed brightness for this effect
        auto_write=False
    )
    print("NeoPixel initialized successfully.")
except Exception as e:
    print(f"FATAL ERROR: Could not initialize NeoPixel: {e}")
    # Halt program if NeoPixel setup fails
    while True:
        time.sleep(1)


# --- 3. Main Loop: NeoPixel Animation ---

print("Starting NeoPixel Ocean Wave effect (Blue/Cyan cycle)...")

while True:
    # 1. Set the color based on the current step
    pixels[0] = ocean_wheel(color_step)
    
    # 2. Update the pixel
    pixels.show()
    
    # 3. Increment the color step
    # Removed 'global color_step' as it is unnecessary in the module scope
    color_step += 1
    
    # 4. Wait for the next step
    time.sleep(WAVE_SPEED)
