import cv2
import time
import numpy as np
import pyautogui
import mediapipe as mp

pyautogui.FAILSAFE = False

CAM_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
SCROLL_SPEED = 40  # how much to scroll per step
COOLDOWN_SEC = 0.02  # time between scrolls
UP_THRESHOLD = 0.7   # hand higher than this = scroll up
DOWN_THRESHOLD = 0.5 # hand lower than this = scroll down

mp_hands = mp.solutions.hands

def hand_center_y(landmarks):
    ids = [0, 5, 9, 13, 17]
    ys = [landmarks[i].y for i in ids]
    return float(np.median(ys))

def main():
    cap = cv2.VideoCapture(CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    hands = mp_hands.Hands(False, 1, 0, 0.5, 0.5)
    last_scroll_t = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res = hands.process(frame_rgb)

        if res.multi_hand_landmarks:
            hand_landmarks = res.multi_hand_landmarks[0].landmark
            cy = hand_center_y(hand_landmarks)

            now = time.time()
            if now - last_scroll_t >= COOLDOWN_SEC:
                if cy < UP_THRESHOLD:
                    pyautogui.scroll(SCROLL_SPEED)
                    last_scroll_t = now
                elif cy > DOWN_THRESHOLD:
                    pyautogui.scroll(-SCROLL_SPEED)
                    last_scroll_t = now

        cv2.imshow("Continuous Virtual Scroll", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()

