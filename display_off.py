# CircuitPython Display Shutdown Script
# (Updated to physically disable the backlight)
#
# This file explicitly releases all display resources and attempts to turn
# off the display's backlight, then enters a sleep loop.
#
# Use this when your main program (code.py) is crashing due to a faulty or
# incorrectly initialized display, and you need to ensure the display is
# completely disabled at boot.

import board
import time
import displayio
import digitalio # Needed to control the backlight pin

print("Attempting to release all display resources...")

# 1. Release Software Resources
try:
    displayio.release_displays()
    print("SUCCESS: Display software resources released.")
except Exception as e:
    print(f"WARNING: displayio.release_displays failed: {e}")

# 2. Control Backlight Pin for Physical Power Off
try:
    # Attempt to use the standard backlight pin name for the Feather S3 TFT
    if hasattr(board, 'TFT_BACKLIGHT'):
        print("Attempting to disable backlight using board.TFT_BACKLIGHT...")
        backlight = digitalio.DigitalInOut(board.TFT_BACKLIGHT)
        backlight.direction = digitalio.Direction.OUTPUT
        
        # Setting the pin low usually turns off the backlight (depending on wiring)
        backlight.value = False
        print("SUCCESS: Backlight physically disabled.")
    else:
        print("WARNING: board.TFT_BACKLIGHT pin not found in this firmware.")

except Exception as e:
    print(f"FATAL ERROR during backlight control: {e}")

# Enter an infinite sleep loop to prevent the program from exiting
while True:
    time.sleep(5)
