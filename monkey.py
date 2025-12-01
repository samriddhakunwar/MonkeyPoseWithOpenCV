import cv2
import mediapipe as mp
import numpy as np
import os
import sys
import datetime

# Redirect stdout for debugging
sys.stdout = sys.__stdout__

print(f"### Script started at {datetime.datetime.now()}")
print(f"### Python version: {sys.version}")
print(f"### OpenCV version: {cv2.__version__}")

# Initialize MediaPipe
try:
    mp_face_mesh = mp.solutions.face_mesh
    mp_hands = mp.solutions.hands
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.05)
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.05)
    print(f"### MediaPipe initialized successfully at {datetime.datetime.now()}")
except Exception as e:
    print(f"### Error initializing MediaPipe: {str(e)} at {datetime.datetime.now()}")
    sys.exit(1)

# Function to extract face landmarks
def get_face_landmarks(image):
    if image is None:
        return None
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)
    if not results.multi_face_landmarks:
        return None
    return results.multi_face_landmarks[0].landmark

# Function to extract hand landmarks
def get_hand_landmarks(image, results):
    if image is None or not results.multi_hand_landmarks:
        return None
    h, w, _ = image.shape
    hand_landmarks_list = []
    for hand_landmarks in results.multi_hand_landmarks:
        points = [[lm.x * w, lm.y * h, lm.z] for lm in hand_landmarks.landmark]
        hand_landmarks_list.append((hand_landmarks, points))
    return hand_landmarks_list

# Teeth detection
def is_teeth_showing(landmarks):
    if not landmarks:
        return False
    upper_lip = np.array([landmarks[13].x, landmarks[13].y])
    lower_lip = np.array([landmarks[14].x, landmarks[14].y])
    mouth_opening = np.linalg.norm(upper_lip - lower_lip)
    TEETH_THRESHOLD = 0.02
    return mouth_opening > TEETH_THRESHOLD

# Wide mouth detection
def is_mouth_wide_open(landmarks):
    if not landmarks:
        return False
    upper_lip = np.array([landmarks[13].x, landmarks[13].y])
    lower_lip = np.array([landmarks[14].x, landmarks[14].y])
    mouth_opening = np.linalg.norm(upper_lip - lower_lip)
    WIDE_MOUTH_THRESHOLD = 0.03
    return mouth_opening > WIDE_MOUTH_THRESHOLD

# Index finger up check
def is_index_finger_up(hand_points):
    if len(hand_points) < 9:
        return False
    index_tip_y = hand_points[8][1]
    middle_base_y = hand_points[6][1]
    # Stricter: index must be significantly higher than middle finger base
    return index_tip_y < (middle_base_y - 20)

# Check if ANY hand has middle finger up
def any_hand_has_middle_finger_up(hand_landmarks_list):
    if not hand_landmarks_list:
        return False
    for _, hand_points in hand_landmarks_list:
        if is_middle_finger_up(hand_points):
            return True
    return False

# Index finger biting check
def is_biting_index_finger(face_landmarks, hand_points, frame):
    if not face_landmarks or len(hand_points) < 9:
        return False
    mouth_center = np.mean([[face_landmarks[13].x, face_landmarks[13].y],
                            [face_landmarks[14].x, face_landmarks[14].y]], axis=0)
    index_tip = hand_points[8]
    h, w, _ = frame.shape
    mouth_center = [mouth_center[0] * w, mouth_center[1] * h]
    distance = np.linalg.norm(np.array(index_tip[:2]) - np.array(mouth_center))
    return distance < 50

# One hand below face and another pointing
def is_one_hand_below_face_and_pointing(face_landmarks, hand_landmarks_list, frame):
    if not face_landmarks or len(hand_landmarks_list) < 2:
        return False
    h, w, _ = frame.shape
    face_center_y = np.mean([lm.y * h for lm in face_landmarks])
    below_face = False
    pointing = False
    for _, hand_points in hand_landmarks_list:
        hand_center_y = np.mean([p[1] for p in hand_points])
        if hand_center_y > face_center_y:
            below_face = True
        if is_index_finger_up(hand_points):
            pointing = True
    return below_face and pointing

# Both hands above head
def is_both_hands_above_head(face_landmarks, hand_landmarks_list, frame):
    if not face_landmarks or len(hand_landmarks_list) < 2:
        return False
    h, w, _ = frame.shape
    face_top_y = min([lm.y * h for lm in face_landmarks])
    hands_above = 0
    for _, hand_points in hand_landmarks_list:
        hand_center_y = np.mean([p[1] for p in hand_points])
        if hand_center_y < face_top_y:
            hands_above += 1
    return hands_above >= 2

# Middle finger up check
def is_middle_finger_up(hand_points):
    if len(hand_points) < 12:
        return False
    middle_tip_y = hand_points[12][1]
    ring_base_y = hand_points[10][1]
    index_tip_y = hand_points[8][1]
    middle_base_y = hand_points[6][1]

    # Middle finger must be significantly higher than ring finger base
    middle_up = middle_tip_y < (ring_base_y - 20)
    # Index finger must NOT be up (to avoid confusion with index finger pose)
    index_not_up = index_tip_y >= (middle_base_y - 20)

    return middle_up and index_not_up# Both middle fingers up check
def is_both_middle_fingers_up(hand_landmarks_list):
    if len(hand_landmarks_list) < 2:
        return False
    middle_up_count = 0
    for _, hand_points in hand_landmarks_list:
        if is_middle_finger_up(hand_points):
            middle_up_count += 1
    return middle_up_count >= 2

# Looking up check
def is_looking_up(face_landmarks):
    if not face_landmarks:
        return False
    # Get the nose tip (landmark 4) and chin (landmark 152)
    nose_y = face_landmarks[4].y
    chin_y = face_landmarks[152].y
    # If nose is significantly above chin, looking up
    return (chin_y - nose_y) > 0.15

# Draw landmarks
def draw_landmarks(image, landmarks, is_hand=False, color=(0, 255, 0)):
    if image is None or not landmarks:
        return
    h, w, _ = image.shape
    for lm in landmarks:
        cx, cy = int(lm.x * w), int(lm.y * h)
        cv2.circle(image, (cx, cy), 2, color, -1)
    if is_hand:
        for i in [4, 8, 12]:
            lm = landmarks[i]
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(image, (cx, cy), 4, (0, 0, 255), -1)

# Load reference images
ref_folder = r"C:\Users\Samriddha\Desktop\monkeypose\monkey_refs"
ref_images = {}
for fname in ["monkey1.jpeg", "monkey2.jpeg", "monkey3.jpeg", "monkey4.jpg", "monkey5_converted.jpg", "monkey8.jpg"]:
    img_path = os.path.join(ref_folder, fname)
    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        if img is not None:
            ref_images[fname] = img

# Default image (monkey1) and blank image for no match
default_image = cv2.resize(ref_images.get("monkey1.jpeg", np.zeros((200, 200, 3), dtype=np.uint8)), (200, 200))
blank_image = np.zeros((200, 200, 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    sys.exit(1)

try:
    last_match_time = datetime.datetime.now()
    current_match = blank_image  # Start with blank image, no default
    match_duration = 5  # seconds

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect landmarks
        face_results = face_mesh.process(rgb)
        hand_results = hands.process(rgb)

        face_landmarks = get_face_landmarks(frame) if face_results.multi_face_landmarks else None
        hand_landmarks = get_hand_landmarks(frame, hand_results)

        # Determine match (start with blank, only show if pose matches)
        best_match_img = blank_image
        if face_landmarks:
            # Check wide mouth FIRST (priority)
            if is_mouth_wide_open(face_landmarks):
                best_match_img = ref_images.get("monkey5_converted.jpg", default_image)
            elif hand_landmarks:
                teeth_showing = is_teeth_showing(face_landmarks)
                if len(hand_landmarks) == 1:
                    # Check biting FIRST (higher priority) to avoid collision with index up detection
                    if is_biting_index_finger(face_landmarks, hand_landmarks[0][1], frame):
                        best_match_img = ref_images.get("monkey2.jpeg", default_image)
                    # Monkey1: BOTH index finger up AND teeth showing required (only with 1 hand, NO middle fingers)
                    elif (is_index_finger_up(hand_landmarks[0][1]) and teeth_showing
                          and not is_middle_finger_up(hand_landmarks[0][1])):
                        best_match_img = ref_images.get("monkey1.jpeg", default_image)
                elif len(hand_landmarks) >= 2:
                    # Check both middle fingers up FIRST (higher priority)
                    if is_both_middle_fingers_up(hand_landmarks):
                        best_match_img = ref_images.get("monkey8.jpg", default_image)
                    # Check both hands above head SECOND
                    elif is_both_hands_above_head(face_landmarks, hand_landmarks, frame):
                        best_match_img = ref_images.get("monkey4.jpg", default_image)
                    # Check hand below face and pointing (only if NOT both middle fingers)
                    elif is_one_hand_below_face_and_pointing(face_landmarks, hand_landmarks, frame):
                        best_match_img = ref_images.get("monkey3.jpeg", default_image)

        # Update current match - change immediately when gesture changes
        if best_match_img is not current_match:
            current_match = best_match_img
            last_match_time = datetime.datetime.now()

            # Safe match name printing
            matched_name = "default"
            for name, img in ref_images.items():
                if np.array_equal(img, current_match) if img is not None and current_match is not None else img is current_match:
                    matched_name = name
                    break
            print(f"### Gesture detected: Displaying {matched_name} at {datetime.datetime.now()}")

        # Resize for overlay
        if current_match is not None and not np.array_equal(current_match, blank_image):
            overlay_img = cv2.resize(current_match, (200, 200))
            frame[10:210, 10:210] = overlay_img

        # Draw landmarks
        if face_results.multi_face_landmarks:
            draw_landmarks(frame, face_results.multi_face_landmarks[0].landmark)
        if hand_results.multi_hand_landmarks:
            for hand_landmarks in hand_results.multi_hand_landmarks:
                draw_landmarks(frame, hand_landmarks.landmark, is_hand=True)

        # Show webcam
        cv2.imshow("Monkey Pose Matcher", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    cap.release()
    cv2.destroyAllWindows()
    face_mesh.close()
    hands.close()
