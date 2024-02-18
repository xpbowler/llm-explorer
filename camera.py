import cv2
import numpy as np
import tensorflow as tf

# Load the TFLite model
interpreter = tf.lite.Interpreter(model_path='1.tflite')
interpreter.allocate_tensors()

# Get model details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_height = input_details[0]['shape'][1]
input_width = input_details[0]['shape'][2]
input_type = input_details[0]['dtype']  # Get the data type of the model input

def is_centered(bbox, frame_width, frame_height, tolerance=0.15):
    """
    Determine if the person's bounding box is centered in the frame.
    """
    x_center = (bbox[1] + bbox[3]) / 2.0
    y_center = (bbox[0] + bbox[2]) / 2.0
    frame_center = (frame_width / 2, frame_height / 2)
    
    x_tolerance = frame_width * tolerance
    y_tolerance = frame_height * tolerance
    
    return abs(x_center - frame_center[0]) <= x_tolerance and abs(y_center - frame_center[1]) <= y_tolerance

cap = cv2.VideoCapture(0)  # or your video source

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess the frame
    frame_resized = cv2.resize(frame, (input_width, input_height))

    # Adjust preprocessing based on the model's expected input data type
    if input_type == np.float32:
        # If the model expects float32 input, normalize the input data
        input_data = np.expand_dims(frame_resized, axis=0)
        input_data = (np.float32(input_data) - 127.5) / 127.5
    elif input_type == np.uint8:
        # If the model expects uint8 input, use the resized frame directly
        input_data = np.expand_dims(frame_resized, axis=0).astype(np.uint8)
    else:
        raise ValueError("Model input type not supported")

    # Run inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()

    # Parse the output
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]  # Bounding box coordinates
    classes = interpreter.get_tensor(output_details[1]['index'])[0]  # Class IDs
    scores = interpreter.get_tensor(output_details[2]['index'])[0]  # Confidence scores

    for i in range(len(scores)):
        if scores[i] > 0.4 and (50<=int(classes[i])<=60):  # Confidence threshold and person class ID
            ymin, xmin, ymax, xmax = boxes[i]
            (left, right, top, bottom) = (xmin * frame.shape[1], xmax * frame.shape[1],
                                          ymin * frame.shape[0], ymax * frame.shape[0])

            # Check if the person is centered
            if is_centered([top, left, bottom, right], frame.shape[1], frame.shape[0]):
                print("Person is centered.")
                cv2.rectangle(frame, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
