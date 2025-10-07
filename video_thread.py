"""
Video Processing Thread
Handles video/camera processing in separate thread for UI responsiveness
"""

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal


class VideoThread(QThread):
    """Worker thread for video/camera processing"""
    
    frame_ready = pyqtSignal(np.ndarray)  # Emits processed frames
    finished = pyqtSignal()  # Emits when processing complete
    error_occurred = pyqtSignal(str)  # Emits error messages
    
    def __init__(self, source, model_handler):
        """
        Initialize video thread
        
        Args:
            source: Video file path or camera index (0 for default camera)
            model_handler: ModelHandler instance for inference
        """
        super().__init__()
        self.source = source
        self.model_handler = model_handler
        self.running = True
        
    def run(self):
        """Process video frames in separate thread"""
        cap = None
        try:
            cap = cv2.VideoCapture(self.source)
            
            if not cap.isOpened():
                self.error_occurred.emit("Failed to open video source")
                return
            
            while self.running and cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # Run YOLO detection
                try:
                    results = self.model_handler.predict(frame)
                    annotated_frame = self.model_handler.get_annotated_image(results)
                    self.frame_ready.emit(annotated_frame)
                except Exception as e:
                    self.error_occurred.emit(f"Detection error: {str(e)}")
                    break
                    
        except Exception as e:
            self.error_occurred.emit(f"Video processing error: {str(e)}")
        finally:
            if cap is not None:
                cap.release()
            self.finished.emit()
        
    def stop(self):
        """Stop video processing"""
        self.running = False