from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
import subprocess
import os
import serial 
import time 
import cv2
from ultralytics import YOLO
import requests

model = YOLO('yolov8n.pt')
post_delay = 5
prev_post = 0 
num_persons = 0 

ser = serial.Serial('/dev/cu.usbmodem11101', 9600)
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0)


@tool 
def execute_motor_inputs(commands):
    """Execute a list of motor commands in the format that will control your movement. Each command will have the format [direction,time_interval,speed] where direction is either (forward, backward, left, or right) and time_interval is a double representing time of travel in seconds and speed is an integer from 1-10 representing the speed of the motor."""
    ret = None
    for command in commands:
        print(command)
        to_send = ""
        for c in command:
            to_send += str(c) + " "
        ser.write(to_send.encode())
        time_to_sleep = float(command[1]) + 0.9
        time.sleep(time_to_sleep)

def rotate(object):
    cap = cv2.VideoCapture(0)
    found = False
    while cap.isOpened() and not found:        
        success, frame = cap.read()
        if not success: break

        frame_center = (frame.shape[1] / 2, frame.shape[0] / 2) 

        # Assume 'model.predict' returns the detection results in a structured format that includes bounding boxes
        results = model.predict(source=frame, classes=[0, 1], conf=0.2)

        for detection in results.detections:
            bbox = detection.bbox  # Assuming bbox format is [x_center, y_center, width, height]
            object_center = (bbox[0], bbox[1])

            # Define a tolerance for being "in the center", e.g., within 10% of the frame dimensions
            tolerance = 0.1
            x_tolerance = frame.shape[1] * tolerance
            y_tolerance = frame.shape[0] * tolerance

            # Check if the object's center is within the tolerance of the frame's center
            if abs(object_center[0] - frame_center[0]) <= x_tolerance and abs(object_center[1] - frame_center[1]) <= y_tolerance:
                found = True
                break  # Object is centered, exit the loop




@tool 
def find_object(object):
    """Rotate your body until the object to find in the camera is in the center of the frame. Then stop rotating"""
    rotate(object)
    





tools = [execute_motor_inputs, find_object]
