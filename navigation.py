import torchvision
import torch
import torchvision.transforms as transforms
import torch.nn.functional as F
import cv2
import PIL.Image
import numpy as np
import traitlets
from jetbot import Camera, bgr8_to_jpeg
from jetbot import Robot

# Hint : Look at Road Following and Collision Avoidance Lab

camera = Camera()
traitlets.dlink((camera, 'value'), transform=bgr8_to_jpeg)
robot = Robot()

#Collision Avoidance
ca_model = torchvision.models.alexnet(pretrained=False)
ca_model.classifier[6] = torch.nn.Linear(model.classifier[6].in_features, 2)
ca_model.load_state_dict(torch.load('best_model.pth'))
device = torch.device('cuda')
ca_model = ca_model.to(device)
ca_mean = 255.0 * np.array([0.485, 0.456, 0.406])
ca_stdev = 255.0 * np.array([0.229, 0.224, 0.225])
normalize = torchvision.transforms.Normalize(ca_mean, ca_stdev)

def collision_avoidance_preprocessing(camera_value):
    """Preprocessing for collision avoidance."""

def collision_avoidance(x):
    """This will determine the next start point which will be 
    which will be demarcated by the presence of another bot."""
    # Collision avoidance has to be trained to detect a bot as
    # and obstacle. This will then be called in the road following function.

#Road following support variables
angle = 0.0
angle_last = 0.0
mean = torch.Tensor([0.485, 0.456, 0.406]).cuda().half()
std = torch.Tensor([0.229, 0.224, 0.225]).cuda().half()

# Instantiating the road following network.
rf_model = torchvision.models.resnet18(pretrained=False)
rf_model.fc = torch.nn.Linear(512, 2)
rf_model.load_state_dict(torch.load('best_steering_model_xy.pth'))
rf_model = rf_model.to(device)
rf_model = rf_model.eval().half()

def road_following_preprocessing(image):
    "Preprocesses the image for road following."
    ...
    
def road_following(change):
    "The main function to navigate in the race."
    ...
    # 1. This will ideally have the road following code
    # 2. This method will also call the collision avoidance 
    #       function which will detect the presence of a bot.
    # 3. Once the collision is detected it will verify it's position
    #       is within the range of the next start point
    # 4. If it is so, it will call the bot detected function
    #       which will publish a message on the appropriate topic.
  
def collision_detected():
    """This will publish the message on the topic for the 
    next bot to run."""
    ...

def move_to_start():
    """Calibrate the bot to reach the start positions."""

def sprint():
    """Navigate through the track."""
