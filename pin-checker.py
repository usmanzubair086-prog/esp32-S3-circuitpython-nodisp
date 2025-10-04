# CircuitPython Pin Introspection Utility for Debugging
#
# This script lists all pin names available in the 'board' module

import board
import microcontroller
import time
import sys

# --- Pin Introspection Utility ---

print("--- BOARD PIN CHECKER ---")
print("Listing all available pin names in the 'board' module:")
print("-" * 30)

pin_found = False
try:
    for name in sorted(dir(board)):
        # Skip internal or non-pin related attributes
        if name.startswith("_"):
            continue

        # Get the attribute from the board module
        pin = getattr(board, name)
        
        # Check if the attribute is a Pin object (which represents a GPIO)
        if isinstance(pin, microcontroller.Pin):
            print(f"Pin Name: {name}")
            pin_found = True
except Exception as e:
    print(f"An error occurred while inspecting pins: {e}")

if not pin_found:
    print("-" * 30)
    print("WARNING: No physical pins were found.")
    print("Please ensure you are using the correct and current CircuitPython firmware for the ESP32-S3 TFT.")
else:
    print("-" * 30)
    print("ACTION REQUIRED:")
    print("Look closely through the list above for the names corresponding to GPIO 7 and GPIO 39.")
    print("The correct names might be IO7, D7, or even specific names like TFT_CS or TFT_DC.")
    print("Once found, update the 'tft_cs' and 'tft_dc' variables in your main code.")

# The script runs once and then loops infinitely to keep the board alive
while True:
    time.sleep(10)
