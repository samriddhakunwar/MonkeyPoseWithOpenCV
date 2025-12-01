# MonkeyPose - Gesture Recognition with Pose Matching

MonkeyPose is a real-time gesture recognition application that uses your webcam and hand/face landmarks to detect specific poses and display corresponding monkey images. Built with MediaPipe and OpenCV.

## Features

- **Real-time Gesture Detection**: Uses MediaPipe to detect face and hand landmarks
- **Multiple Pose Recognition**: Supports 8 different monkey poses based on various gestures
- **Live Webcam Feed**: Displays matched images in real-time on the webcam feed
- **Easy to Extend**: Simple function-based gesture detection system

## Supported Gestures

| Monkey  | Gesture               | Trigger                                          |
| ------- | --------------------- | ------------------------------------------------ |
| Monkey1 | Index Finger + Teeth  | Show index finger up with teeth showing (1 hand) |
| Monkey2 | Biting Index Finger   | Place index finger near mouth (1 hand)           |
| Monkey3 | Pointing + Hand Below | One hand below face pointing up (2 hands)        |
| Monkey4 | Both Hands Above Head | Both hands positioned above head (2 hands)       |
| Monkey5 | Wide Open Mouth       | Open mouth very wide                             |
| Monkey8 | Both Middle Fingers   | Show both middle fingers up (2 hands)            |

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- NumPy (`numpy`)
- Webcam

## Installation

1. **Clone or download this repository**

2. **Install dependencies**:

   ```bash
   pip install opencv-python mediapipe numpy
   ```

3. **Prepare reference images**:
   - Create a `monkey_refs` folder in the project directory
   - Add image files:
     - `monkey1.jpeg`
     - `monkey2.jpeg`
     - `monkey3.jpeg`
     - `monkey4.jpg`
     - `monkey5_converted.jpg`
     - `monkey8.jpg`

## Usage

1. **Run the application**:

   ```bash
   python monkey.py
   ```

2. **Interact with the webcam**:

   - Show different gestures to trigger corresponding monkey images
   - Press `q` to quit the application

3. **View results**:
   - Matched images display in a 200x200 overlay in the top-left corner
   - The main feed shows your face and hand landmarks

## File Structure

```
monkeypose/
├── monkey.py                 # Main application file
├── README.md                 # This file
├── monkey_refs/              # Reference images folder
│   ├── monkey1.jpeg
│   ├── monkey2.jpeg
│   ├── monkey3.jpeg
│   ├── monkey4.jpg
│   ├── monkey5_converted.jpg
│   └── monkey8.jpg
└── .gitignore               # Git ignore file (recommended)
```

## How It Works

### Gesture Detection Functions

- **`is_teeth_showing()`**: Detects if teeth are visible (mouth opening > 0.02)
- **`is_index_finger_up()`**: Checks if index finger is raised
- **`is_middle_finger_up()`**: Checks if middle finger is raised
- **`is_biting_index_finger()`**: Detects index finger proximity to mouth
- **`is_mouth_wide_open()`**: Detects wide mouth opening (> 0.03)
- **`is_both_hands_above_head()`**: Detects both hands above head
- **`is_one_hand_below_face_and_pointing()`**: Detects one hand below face pointing up
- **`is_both_middle_fingers_up()`**: Detects both middle fingers raised

### Detection Priority

When multiple gestures are detected, the priority order is:

1. Wide mouth (Monkey5)
2. Both middle fingers (Monkey8)
3. Biting index (Monkey2)
4. Index finger + teeth (Monkey1)
5. Both hands above head (Monkey4)
6. Hand below + pointing (Monkey3)

## Customization

### Adding New Gestures

1. **Create a detection function** in `monkey.py`:

   ```python
   def is_your_gesture(face_landmarks, hand_landmarks_list, frame):
       # Your detection logic here
       return True/False
   ```

2. **Add your image** to `monkey_refs/` folder (e.g., `monkey9.jpg`)

3. **Update the file loading** list:

   ```python
   for fname in [..., "monkey9.jpg"]:
   ```

4. **Add detection logic** in the gesture matching section:
   ```python
   elif is_your_gesture(...):
       best_match_img = ref_images.get("monkey9.jpg", default_image)
   ```

### Adjusting Thresholds

Modify these constants to fine-tune detection:

- `TEETH_THRESHOLD = 0.02` (in `is_teeth_showing()`)
- `WIDE_MOUTH_THRESHOLD = 0.03` (in `is_mouth_wide_open()`)
- Pixel differences in finger detection functions (e.g., `- 20` in middle/index finger checks)

## Troubleshooting

| Issue                 | Solution                                                           |
| --------------------- | ------------------------------------------------------------------ |
| Webcam not opening    | Ensure webcam is connected and not in use by other apps            |
| Images not displaying | Check `monkey_refs/` folder and file names match exactly           |
| Gestures not detected | Adjust thresholds or ensure good lighting conditions               |
| Slow performance      | Reduce frame resolution or lower detection confidence in MediaPipe |

## Performance Tips

- Ensure good lighting for better face/hand detection
- Keep hands clearly visible and unobstructed
- Use a high-quality webcam for better accuracy
- Close other CPU-intensive applications

## Dependencies Info

- **OpenCV**: Computer vision library for image processing
- **MediaPipe**: ML framework for pose, hand, and face detection
- **NumPy**: Numerical computing library

## License

This project is open source. Feel free to modify and distribute.

## Author

Created as a fun gesture recognition project using MediaPipe and OpenCV.

---

**Note**: This application requires a working webcam and good lighting conditions for optimal performance.
