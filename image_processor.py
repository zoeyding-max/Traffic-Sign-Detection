"""
Image Processing Utilities
Handles image reading, processing, and display conversion
"""

import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt


class ImageProcessor:
    """Utilities for image processing and display"""
    
    @staticmethod
    def read_image(image_path):
        """
        Read image from file
        
        Args:
            image_path: Path to image file
            
        Returns:
            numpy array of image or None if failed
        """
        image = cv2.imread(image_path)
        return image
    
    @staticmethod
    def save_image(image, output_path):
        """
        Save image to file
        
        Args:
            image: numpy array of image
            output_path: Path to save image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            cv2.imwrite(output_path, image)
            return True
        except Exception:
            return False
    
    @staticmethod
    def numpy_to_pixmap(image):
        """
        Convert numpy array to QPixmap for display
        
        Args:
            image: numpy array (BGR format)
            
        Returns:
            QPixmap object
        """
        # Convert BGR to RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        
        # Convert to QImage
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, 
                         QImage.Format_RGB888)
        
        # Convert to QPixmap
        return QPixmap.fromImage(qt_image)
    
    @staticmethod
    def scale_pixmap(pixmap, label_size, keep_aspect_ratio=True):
        """
        Scale pixmap to fit label
        
        Args:
            pixmap: QPixmap to scale
            label_size: QSize of target label
            keep_aspect_ratio: Whether to maintain aspect ratio
            
        Returns:
            Scaled QPixmap
        """
        if keep_aspect_ratio:
            return pixmap.scaled(label_size, Qt.KeepAspectRatio, 
                               Qt.SmoothTransformation)
        else:
            return pixmap.scaled(label_size, Qt.IgnoreAspectRatio,
                               Qt.SmoothTransformation)