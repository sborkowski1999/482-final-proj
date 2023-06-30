import cv2
# importing mediapipe and reference it as mp
import mediapipe as mp
import time
# setting up the mediapipe 3D object detection
mp_objectron = mp.solutions.objectron
# setting-up the drawing utility 
mp_drawing = mp.solutions.drawing_utils
# capturing the video
cap = cv2.VideoCapture(0)
# objectron is the 3D object detection and various of its ML performance parameters # need to be defined. # we also specify the objectron only detect one object namely a ‘Cup’ 
# this can be changed to detect another object or multiple objects
with mp_objectron.Objectron(static_image_mode=False, max_num_objects=2, min_detection_confidence=0.5, min_tracking_confidence=0.8, model_name='Cup') as objectron: 
    while cap.isOpened():
    
        success, image = cap.read() 
        start = time.time()

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Convert the BGR image to RGB. image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference. 
        image.flags.writeable = False 
        results = objectron.process(image)
    
        image.flags.writeable = True

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) 
    # Start the detection 
        if results.detected_objects:
            for detected_object in results.detected_objects:
                    mp_drawing.draw_landmarks(image, detected_object.landmarks_2d, mp_objectron.BOX_CONNECTIONS)
                    mp_drawing.draw_axis(image, detected_object.rotation, detected_object.translation) 
    
        end = time.time()
        totalTime = end - start 
        fps = 1 / totalTime 
        cv2.putText(image, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2) 
        cv2.imshow('MediaPipe Objectron', image) 
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()

#with mp_objectron.Objectron(static_image_mode=False, max_num_objects=2, min_detection_confidence=0.5, min_tracking_confidence=0.8, model_name='Shoe') as objectron:

