# Hand-Gesture Virtual Scroll Controller

A computer vision app that lets you scroll the screen up and down using hand position tracked through your webcam no mouse or trackpad needed. Built with Python, OpenCV and MediaPipe.

## What it does

- Opens your webcam and tracks your hand in real time using MediaPipe Hands
- Computes a stable vertical reference point from the hand's palm landmarks
- Scrolls the screen **up** when your hand is held high in the frame, and **down** when held low
- Scrolling is continuous while your hand stays in the trigger zone, with a short cooldown between scroll events to keep motion smooth
- Shows a live webcam feed so you can see what the app is tracking

## How it works

1. **Hand landmark detection** — Each frame is processed through MediaPipe's `Hands` model, which returns 21 landmark points per detected hand.
2. **Stable center point** — Rather than relying on a single fingertip (which can jitter), the vertical center is computed as the **median y-position** of five palm-base landmarks (wrist and the base of each finger), giving a steadier reference than any one point alone.
3. **Threshold-based scroll direction** — The hand's normalized vertical position (0 = top of frame, 1 = bottom) is compared against two thresholds:
   - Above the **up threshold** → scroll up
   - Below the **down threshold** → scroll down
   - In between → no scroll (a neutral "dead zone")
4. **Cooldown timing** — A minimum time gap between scroll actions prevents the scroll from firing every single frame, keeping the motion controllable rather than erratic.
5. **System-level scrolling** — Actual scroll events are sent via `pyautogui.scroll()`, so they affect whatever window/app currently has focus on your system not just the webcam preview.

## Tech stack

- Python
- OpenCV (`cv2`)
- MediaPipe (`mediapipe.solutions.hands`)
- PyAutoGUI (system scroll control)
- NumPy

## Running it locally

```bash
git clone https://github.com/<your-username>/hand-gesture-scroll-controller.git
cd hand-gesture-scroll-controller

pip install opencv-python mediapipe pyautogui numpy
python scroll_controller.py
```

Press `q` with the video window focused to quit.

## Configuration

All key behavior is controlled by constants at the top of the script:

| Setting | Purpose |
|---|---|
| `CAM_INDEX` | Which webcam to use (0 = default) |
| `FRAME_WIDTH` / `FRAME_HEIGHT` | Capture resolution |
| `SCROLL_SPEED` | How much to scroll per triggered step |
| `COOLDOWN_SEC` | Minimum time between scroll events |
| `UP_THRESHOLD` / `DOWN_THRESHOLD` | Normalized vertical positions that trigger scroll up/down |

Tune the thresholds and cooldown to match your webcam framing and how sensitive you want the scrolling to feel.

## Usage notes

- Keep your hand clearly visible and reasonably centered in the frame for stable tracking
- The dead zone between `DOWN_THRESHOLD` and `UP_THRESHOLD` is intentional — it gives you a resting hand position that doesn't trigger any scrolling
- Since scroll events go to whatever window has OS focus, click into the app/document you want to scroll before raising your hand
- `pyautogui.FAILSAFE` is disabled, so moving your cursor to a screen corner won't act as an emergency stop close the webcam window (`q`) to stop the app instead

## Limitations

- Tracks only a single hand at a time (`max_num_hands=1`)
- Detection quality depends on lighting and how clearly the hand is visible against the background
- Thresholds are fixed values tuned for a roughly centered, front-facing hand different camera placements may need retuning
- No horizontal/click gesture support this script only handles vertical scroll

## Project structure

```
├── scroll_controller.py
├── requirements.txt
└── README.md
```
