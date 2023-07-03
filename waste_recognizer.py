import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp

# Load the TFLite model
model_path = "model.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()

# Get model input details
input_details = interpreter.get_input_details()
input_shape = input_details[0]['shape']
input_mean = 127.5
input_std = 127.5

# Define class labels
class_labels = ['organic', 'recycling']

# Open default camera
cap = cv2.VideoCapture(0)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Constants for the box outline
box_size = 300  # Size of the box
screen_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
screen_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
box_x = int((screen_width - box_size) / 2)  # X-coordinate of the top-left corner of the box
box_y = int((screen_height - box_size) / 2)  # Y-coordinate of the top-left corner of the box

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while True:
        # Read frame from the camera
        ret, frame = cap.read()

        if not ret:
            break

        # Hand detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        # Waste classification
        if results.multi_hand_landmarks:
            # Extract the region of interest (ROI) from the frame
            roi = frame[box_y:box_y + box_size, box_x:box_x + box_size]

            # Preprocess the ROI for waste classification
            resized_frame = cv2.resize(roi, (input_shape[1], input_shape[2]))
            normalized_frame = (resized_frame.astype(np.float32) - input_mean) / input_std
            input_data = np.expand_dims(normalized_frame, axis=0)

            # Set the model input
            interpreter.set_tensor(input_details[0]['index'], input_data)

            # Run inference
            interpreter.invoke()

            # Get the model output
            output_details = interpreter.get_output_details()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            class_index = np.argmax(output_data)
            confidence = output_data[0][class_index]

            # Get waste class label
            if confidence > 0.5:
                waste_class = class_labels[class_index]
            else:
                waste_class = "Unknown"

            # Draw waste class label on the frame
            cv2.putText(frame, f"Waste Class: {waste_class}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Render hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Draw the box outline on the frame
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_size, box_y + box_size), (0, 0, 255), 2)

        cv2.imshow('Hand Tracking', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
