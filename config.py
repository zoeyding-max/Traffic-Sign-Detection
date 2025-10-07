"""
Configuration file for Traffic Sign Recognition System
Contains all configurable parameters and constants
"""

# Model Configuration
MODEL_NAME = 'yolov8n.pt'  # YOLOv8 nano for speed
CONFIDENCE_THRESHOLD = 0.25
IOU_THRESHOLD = 0.45

# Image Processing
IMAGE_SIZE = (640, 640)
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp']

# Video Processing
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv']
DEFAULT_CAMERA_INDEX = 0

# Output
OUTPUT_FOLDER_NAME = 'detected_output'
OUTPUT_IMAGE_PREFIX = 'detected_'

# UI Configuration
WINDOW_TITLE = 'Traffic Sign Recognition System - AI Hackathon'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# Colors (for future customization)
PRIMARY_COLOR = '#4CAF50'
SECONDARY_COLOR = '#45a049'
BACKGROUND_COLOR = '#1a1a2e'
TABLE_BG_COLOR = '#2d2d44'

# Detection Statistics
STATS_PRECISION = 2  # Decimal places for confidence scores