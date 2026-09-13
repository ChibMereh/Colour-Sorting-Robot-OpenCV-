import cv2
import time
import sys
import serial

CAMERA_INDEX = 0
SERIAL_PORT = 'COM5'
BAUDRATE = 9600

MIN_INTERVAL_BETWEEN_COMMANDS = 0.2
SHOW_WINDOW = True

AREA_THRESHOLD = 500  # minimum pixel area for detection

# --- BLUE COLOR RANGE ---
LOWER_BLUE = (100, 120, 70)
UPPER_BLUE = (140, 255, 255)

# --- RED COLOR RANGE (two HSV ranges) ---
LOWER_RED1 = (0, 120, 70)
UPPER_RED1 = (10, 255, 255)
LOWER_RED2 = (170, 120, 70)
UPPER_RED2 = (180, 255, 255)

# ----------------------------
# CAMERA SETUP
# ----------------------------
cap = cv2.VideoCapture(CAMERA_INDEX)
if not cap.isOpened():
    print("Cannot open camera")
    sys.exit(1)

# ----------------------------
# SERIAL SETUP
# ----------------------------
ser = None
try:
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)
    print(f"Connected to serial port {SERIAL_PORT}")
except Exception as e:
    print("Serial connection failed:", e)
    ser = None


# ----------------------------
# SEND COMMAND FUNCTION
# ----------------------------
last_cmd_time = 0

def send_cmd(cmd):
    global last_cmd_time
    now = time.time()

    if now - last_cmd_time < MIN_INTERVAL_BETWEEN_COMMANDS:
        return

    last_cmd_time = now

    if ser:
        try:
            ser.write(cmd)
            ser.flush()
            print("Sent:", cmd)
        except Exception as e:
            print("Serial write error:", e)
    else:
        print("Serial not available")


# ----------------------------
# STATE MACHINE
# ----------------------------
state = "stop"
print("Running... Press Q to quit.")

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to read frame.")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # BLUE detection
    mask_blue = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
    blue_area = cv2.countNonZero(mask_blue)
    blue_detected = blue_area > AREA_THRESHOLD

    # RED detection
    mask_red1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask_red2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask_red = mask_red1 + mask_red2
    red_area = cv2.countNonZero(mask_red)
    red_detected = red_area > AREA_THRESHOLD

    # ----------------------------
    # DECISION LOGIC
    # ----------------------------
    if blue_detected:
        if state != "forward":
            state = "forward"
            send_cmd(b"f\n")   # forward

    elif red_detected:
        if state != "reverse":
            state = "reverse"
            send_cmd(b"r\n")   # reverse

    else:
        if state != "stop":
            state = "stop"
            send_cmd(b"s\n")   # stop

    # ----------------------------
    # VISUALIZATION
    # ----------------------------
    display = frame.copy()

    # Highlight detected edges
    edges_blue = cv2.Canny(mask_blue, 50, 150)
    edges_red = cv2.Canny(mask_red, 50, 150)

    display[edges_blue > 0] = (255, 0, 0)   # blue edges
    display[edges_red > 0] = (0, 0, 255)    # red edges

    cv2.putText(display,
                f"Blue: {blue_area}  Red: {red_area}  State: {state}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2)

    if SHOW_WINDOW:
        cv2.imshow("Camera View", frame)
        cv2.imshow("Blue Mask", mask_blue)
        cv2.imshow("Red Mask", mask_red)
        cv2.imshow("Detection View", display)

    # Quit logic
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        send_cmd(b"s\n")
        break

cap.release()
cv2.destroyAllWindows()
if ser:
    ser.close()
