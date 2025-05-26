# Final Project (Individual): "Aerial Threat Detection: Soldier and Civilian Classification Using Drone Vision and Deep Learning"

[![Open Training Code In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1R_2fwjSQjpwR9k66QVFUqtVJzTt6Um9h?usp=sharing) [![Militar Dataset]()](https://universe.roboflow.com/escola-naval-4yw3p/tracking-military-rca)



## Project Overview:

As tensions escalate and conflict looms, the ability to identify and classify individuals from aerial surveillance becomes a crucial defense capability. This project proposes the development of a computer vision system that can classify and using aerial imagery captured by drones. As a student of Computer Science / Information Technology, your role is to contribute to national defense through to support reconnaissance and humanitarian operations.

* Build an image classification model to distinguish from in aerial images.
* Utilize drone footage or images from publicly available datasets (Roboflow). 
* Integrate the trained model into a drone simulation (optional: OpenCV/streamed video).
* Provide an interface or system prototype that could visualize classifications in real-time.

1. [x] Dataset Preparation
Use to search and collect labeled datasets of “soldiers,” “civilians,” or “person” classes.
If needed, augment the dataset to improve generalization (rotate, flip, scale).

* Possible Data: https://universe.roboflow.com/militarypersons/uav-person-3
* Possible Data: https://universe.roboflow.com/minwoo/combatant-dataset
* Possible Data: https://universe.roboflow.com/xphoenixua-nlncq/soldiers-detection-spf
* Possible Data: https://universe.roboflow.com/folks/look-down-folks

Chosen Dataset for the current project : 📦 [tracking-military-rca Dataset](https://universe.roboflow.com/escola-naval-4yw3p/tracking-military-rca)


- [x] 2. Model Selection
Use YOLOv5 or YOLOv8 for real-time object detection and classification.
Train the model using annotated drone-like images.
Evaluate using metrics: precision, recall, mAP (mean Average Precision).

Selected Pretrained Model : For this project, a pretrained **YOLOv8m** model was used and was trained to the selected data set trakcing-military-rca from roboflow.

Evaluation can be found in the Google Colab notebook . [![Open Training Code In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1R_2fwjSQjpwR9k66QVFUqtVJzTt6Um9h?usp=sharing)


- [ ] 3. System Development
Integrate the trained model with a video stream (e.g., drone footage simulation).
Draw bounding boxes with class labels (e.g., “Soldier”, “Civilian”).


- [ ] 4. Testing and Evaluation
Test the model on unseen images and video feeds.
Assess accuracy in various lighting and altitude conditions.
Discuss potential real-world use and ethical considerations.



## Tools and Technologies:
Python, YOLOv5 / YOLOv8 or Other models, Roboflow, OpenCV, PyTorch or TensorFlow, Google Colab or local GPU.


## Expected Output:
- [ ] A working prototype capable of detecting and classifying individuals in aerial footage. (Github, Google Drive)
- [ ] A report or presentation detailing the model design, performance, and recommendations for real-world deployment.


## Ethical Note:
This project is conceptual and strictly educational. It is not intended for real-life military application without proper ethical evaluation and government oversight.
