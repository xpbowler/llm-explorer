import cv2
import numpy as np
import tensorflow as tf
import serial 
import time


interpreter = tf.lite.Interpreter(model_path='1.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
input_height = input_details[0]['shape'][1]
input_width = input_details[0]['shape'][2]
input_type = input_details[0]['dtype']  # Get the data type of the model input


ser = serial.Serial('/dev/cu.usbmodem11101', 9600)

def is_centered(bbox, frame_width, frame_height, tolerance=0.18):
    """
    Determine if the person's bounding box is centered in the frame.
    """
    x_center = (bbox[1] + bbox[3]) / 2.0
    y_center = (bbox[0] + bbox[2]) / 2.0
    frame_center = (frame_width / 2, frame_height / 2)
    
    x_tolerance = frame_width * tolerance
    y_tolerance = frame_height * tolerance
    
    return abs(x_center - frame_center[0]) <= x_tolerance and abs(y_center - frame_center[1]) <= y_tolerance

def rotate(object):
    cap = cv2.VideoCapture(0)
    print("Finding " + object + "...")
    to_send = "left 0.1 2"
    ser.write(to_send.encode())
    time.sleep(1)

    ret, frame = cap.read()

    frame_resized = cv2.resize(frame, (input_width, input_height))

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
        if scores[i] > 0.35 and (50<=int(classes[i])<=60):  # Confidence threshold and object class ID
            ymin, xmin, ymax, xmax = boxes[i]
            (left, right, top, bottom) = (xmin * frame.shape[1], xmax * frame.shape[1],
                                        ymin * frame.shape[0], ymax * frame.shape[0])

            # Check if the object is centered
            if is_centered([top, left, bottom, right], frame.shape[1], frame.shape[0]):
                cap.release()
                print("Found " + object + "!")
                return True
    cap.release()
    return False

def parse(output):
    """parse output from GPT-4"""
    return output