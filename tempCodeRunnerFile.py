import cv2
import mediapipe as mp
import math

# -----------------------------
# Initialize MediaPipe
# -----------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Start webcam
cap = cv2.VideoCapture(0)

# Verification states
blink_detected = False
left_done = False
right_done = False
verified = False

blink_counter = 0

# -----------------------------
# Helper Function
# -----------------------------
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

# -----------------------------
# Main Loop
# -----------------------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    instruction = "Show your face"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            landmarks = face_landmarks.landmark

            # Face detected
            cv2.putText(frame, "FACE DETECTED", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # -----------------------------
            # Blink Detection
            # -----------------------------
            left_eye_top = landmarks[159]
            left_eye_bottom = landmarks[145]

            eye_distance = distance(left_eye_top, left_eye_bottom)

            if eye_distance < 0.015:
                blink_counter += 1

            if blink_counter > 2:
                blink_detected = True

            # -----------------------------
            # Head Movement Detection
            # -----------------------------
            nose = landmarks[1]

            nose_x = nose.x

            if blink_detected:
                instruction = "Turn Head LEFT"

                if nose_x < 0.42:
                    left_done = True

            if left_done:
                instruction = "Turn Head RIGHT"

                if nose_x > 0.58:
                    right_done = True

            # -----------------------------
            # Verification
            # -----------------------------
            if blink_detected and left_done and right_done:
                verified = True
                instruction = "LIVE VERIFIED"

            elif not blink_detected:
                instruction = "BLINK YOUR EYES"

            # -----------------------------
            # Draw Face Box
            # -----------------------------
            x_min = int(min([lm.x for lm in landmarks]) * w)
            y_min = int(min([lm.y for lm in landmarks]) * h)
            x_max = int(max([lm.x for lm in landmarks]) * w)
            y_max = int(max([lm.y for lm in landmarks]) * h)

            color = (0, 255, 0) if verified else (0, 0, 255)

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), color, 2)

    # -----------------------------
    # UI Text
    # -----------------------------
    cv2.putText(frame, "AI LIVENESS DETECTION", (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.putText(frame, instruction, (30, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    # Progress Tracker
    cv2.putText(frame, f"Blink: {'YES' if blink_detected else 'NO'}", (30, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Left: {'YES' if left_done else 'NO'}", (30, 240),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.putText(frame, f"Right: {'YES' if right_done else 'NO'}", (30, 280),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    # Final Status
    status = "LIVE PERSON VERIFIED" if verified else "VERIFYING..."

    color = (0, 255, 0) if verified else (0, 0, 255)

    cv2.putText(frame, status, (30, 330),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("Liveness Detection System", frame)

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()