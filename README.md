# LLM Explorer

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE.md)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/xpbowler/llm-explorer.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/xpbowler/llm-explorer)

## Inspiration 

Controlling robot behavior historically relies on well-defined algorithms, control loops, and functions that always give the same output given the same input. It relies on largely numerical data+computation. However, you cannot control robot behavior with text as it has 'meaning' behind it with substantial input variability and inconsistencies. The key insight to this project was the idea of using LLM agents for defining and deciding robot behaviour, allowing for language-based decision making. We thought the best way to interpret this meaning is through natural language with LLMs and then allow it to convert its 'intent' into real world actions through the use of tools we define and provide.

## What it does
Our project is a voice-controlled robot using LLM agents. With only voice input, it is capable of identifying a target object, and driving towards it. Once the object has been reached, it plays a little surprise tune to celebrate!

## How we built it
LLMExplorer relies on LLM agents as the 'brain', if you will, to control the actions of the robot and decision making process. This is a key innovation in the space of robotics, as LLMExplorer is able to perceive the world around it through natural language as a modal of communication.

We define tools for the core LLM agents that is trained specifically on using tool usage. Tools are user defined functions that we then pass into the LLM.

The pipeline starts with OpenAI Whisper speech-to-text, which is then passed into the LLM. The LLM then parses the information, extracting meaning and intent from the text. It is able to use the functions 'available' to it and send well defined inputs to control the arduino. The control inputs are then parsed with a parser and converted into motor actuations that control the robot movement.

## 🔨 Installation

Requirements :

|        Name         |               Description               | Required | Default value |                   Limitations                    |
|:-------------------:|:---------------------------------------:|:--------:|:-------------:|:------------------------------------------------:|
|`python`   |   Python  |    ✅     |       ❌       |  Recommended v3.10.10  |
|  `Tensorflow-lite`  | Running ssd-mobilenet model  |    ✅     |       ✅       |         Recommended v2.10.0                 |
|   `opencv-python`   |        cv2       |    ✅     |       ❌       |              Recommended v.4.8.0.76            |

  
Github file structure:

```bash
.
├── arduino_controller
├── tools 
│   ├── agentUtil.py # Define LLM agent 
│   ├── functions.py # Provide tools to agent
│   ├── utils.py # Helper functions for world interactibility
├── utility # Define methods for information input (sound, video)
│   ├── camera.py
│   ├── speech_rec.py
├── README.md
├── main.py # Root python script
├── requirements.txt
└── ssd-mobilenet.tflite
```

Instructions:

1. Clone the repository 
```bash
$ git clone https://github.com/xpbowler/llm-explorer
```

(Optional) Set up python virtual environment
```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

2. Install required dependencies
```bash
$ pip install -r requirements.txt
```

3. Set OPENAI_API_KEY environment variable
```bash
$ nano ~./bashrc
$ export OPENAI_API_KEY="YOUR_API_KEY"
```
(venv)
```bash
$ nano venv/bin/activate
$ export OPENAI_API_KEY="YOUR_API_KEY"
```

4. Configure/test microphone input and video input with `python camera.py`

5. Run root python script with
```bash
$ python main.py
```
