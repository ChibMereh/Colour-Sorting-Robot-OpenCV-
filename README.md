# Colour Sorting Robot (OpenCV + Arduino)

This project sorts items by color using a webcam and an Arduino-controlled motor.

## How it works
- `projectcv2.py` captures live camera frames and detects **blue** and **red** colors in HSV.
- Based on the detected color, Python sends serial commands to Arduino:
  - `f` → move forward (blue detected)
  - `r` → move reverse (red detected)
  - `s` → stop (no target color detected)
- `Sorting Robot.ino` receives those commands and drives the motor pins.

## Files
- `projectcv2.py` – OpenCV color detection + serial communication.
- `Sorting Robot.ino` – Arduino motor control logic.

## Requirements
- Python 3
- OpenCV (`cv2`)
- PySerial (`serial`)
- Arduino board connected over serial
- Webcam

## Notes
- Default serial settings in Python:
  - Port: `COM5`
  - Baud rate: `9600`
- If your Arduino is on a different port, update `SERIAL_PORT` in `projectcv2.py`.

## Run
1. Upload `Sorting Robot.ino` to your Arduino.
2. Install Python dependencies.
3. Run:
   ```bash
   python projectcv2.py
   ```
4. Press `q` to quit.
