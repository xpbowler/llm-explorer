from langchain.agents import tool
from langchain.chat_models import ChatOpenAI
import subprocess
import os
import serial 
import time 

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
        time_to_sleep = int(command[1]) + 0.5
        time.sleep(time_to_sleep)

        # received = ""
        # while ser.in_waiting > 0:
        #     received += ser.readline().decode()
        # print(received)

tools = [execute_motor_inputs]
