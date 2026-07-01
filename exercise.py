import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils


def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(
        c[1] - b[1], c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1], a[0] - b[0]
    )

    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


cap = cv2.VideoCapture(0)

counter = 0
stage = "UP"

with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as pose:

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark

            hip = [
                landmarks[
                    mp_pose.PoseLandmark.LEFT_HIP.value
                ].x,
                landmarks[
                    mp_pose.PoseLandmark.LEFT_HIP.value
                ].y
            ]

            knee = [
                landmarks[
                    mp_pose.PoseLandmark.LEFT_KNEE.value
                ].x,
                landmarks[
                    mp_pose.PoseLandmark.LEFT_KNEE.value
                ].y
            ]

            ankle = [
                landmarks[
                    mp_pose.PoseLandmark.LEFT_ANKLE.value
                ].x,
                landmarks[
                    mp_pose.PoseLandmark.LEFT_ANKLE.value
                ].y
            ]

            angle = calculate_angle(
                hip,
                knee,
                ankle
            )

            if angle > 160:
                stage = "UP"

            if angle < 90 and stage == "UP":
                stage = "DOWN"

            if angle > 160 and stage == "DOWN":
                counter += 1
                stage = "UP"

            cv2.putText(
                image,
                f'Angle: {int(angle)}',
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

        except:
            pass

        cv2.rectangle(
            image,
            (0, 0),
            (250, 90),
            (0, 0, 0),
            -1
        )

        cv2.putText(
            image,
            'SQUATS',
            (10, 25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        cv2.putText(
            image,
            f'COUNT: {counter}',
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.putText(
            image,
            f'STAGE: {stage}',
            (10, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        cv2.imshow(
            "Squat Counter",
            image
        )

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
