"""
Model Handler for YOLO Detection
Handles model loading, inference, and optimization
"""

import numpy as np
from ultralytics import YOLO
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, IMAGE_SIZE


class ModelHandler:
    """Handles YOLO model operations"""
    
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Load YOLOv8 model with optimization"""
        try:
            # Load YOLOv8 model
            self.model = YOLO(MODEL_NAME)
            
            # Warm up model with dummy input for faster inference
            dummy_img = np.zeros((*IMAGE_SIZE, 3), dtype=np.uint8)
            self.model(dummy_img, verbose=False)
            
            return True, "Model loaded successfully"
            
        except Exception as e:
            return False, f"Failed to load model: {str(e)}"
    
    def predict(self, image, conf=None, iou=None):
        """
        Run inference on image
        
        Args:
            image: numpy array of image
            conf: confidence threshold (optional)
            iou: IoU threshold (optional)
            
        Returns:
            YOLO results object
        """
        if self.model is None:
            raise ValueError("Model not loaded")
            
        conf = conf or CONFIDENCE_THRESHOLD
        iou = iou or IOU_THRESHOLD
        
        results = self.model(image, conf=conf, iou=iou)
        return results[0]
    
    def get_annotated_image(self, results):
        """Get annotated image from results"""
        return results.plot()
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.model is not None
"""
Model Handler for YOLO Detection
Handles model loading, inference, and optimization
"""

import numpy as np
from ultralytics import YOLO
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, IMAGE_SIZE


class ModelHandler:
    """Handles YOLO model operations"""
    
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Load YOLOv8 model with optimization"""
        try:
            # Load YOLOv8 model
            self.model = YOLO(MODEL_NAME)
            
            # Warm up model with dummy input for faster inference
            dummy_img = np.zeros((*IMAGE_SIZE, 3), dtype=np.uint8)
            self.model(dummy_img, verbose=False)
            
            return True, "Model loaded successfully"
            
        except Exception as e:
            return False, f"Failed to load model: {str(e)}"
    
    def predict(self, image, conf=None, iou=None):
        """
        Run inference on image
        
        Args:
            image: numpy array of image
            conf: confidence threshold (optional)
            iou: IoU threshold (optional)
            
        Returns:
            YOLO results object
        """
        if self.model is None:
            raise ValueError("Model not loaded")
            
        conf = conf or CONFIDENCE_THRESHOLD
        iou = iou or IOU_THRESHOLD
        
        results = self.model(image, conf=conf, iou=iou)
        return results[0]
    
    def get_annotated_image(self, results):
        """Get annotated image from results"""
        return results.plot()
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.model is not None
"""
Model Handler for YOLO Detection
Handles model loading, inference, and optimization
"""

import numpy as np
from ultralytics import YOLO
from config import MODEL_NAME, CONFIDENCE_THRESHOLD, IOU_THRESHOLD, IMAGE_SIZE


class ModelHandler:
    """Handles YOLO model operations"""
    
    def __init__(self):
        self.model = None
        
    def load_model(self):
        """Load YOLOv8 model with optimization"""
        try:
            # Load YOLOv8 model
            self.model = YOLO(MODEL_NAME)
            
            # Warm up model with dummy input for faster inference
            dummy_img = np.zeros((*IMAGE_SIZE, 3), dtype=np.uint8)
            self.model(dummy_img, verbose=False)
            
            return True, "Model loaded successfully"
            
        except Exception as e:
            return False, f"Failed to load model: {str(e)}"
    
    def predict(self, image, conf=None, iou=None):
        """
        Run inference on image
        
        Args:
            image: numpy array of image
            conf: confidence threshold (optional)
            iou: IoU threshold (optional)
            
        Returns:
            YOLO results object
        """
        if self.model is None:
            raise ValueError("Model not loaded")
            
        conf = conf or CONFIDENCE_THRESHOLD
        iou = iou or IOU_THRESHOLD
        
        results = self.model(image, conf=conf, iou=iou)
        return results[0]
    
    def get_annotated_image(self, results):
        """Get annotated image from results"""
        return results.plot()
    
    def is_loaded(self):
        """Check if model is loaded"""
        return self.model is not None