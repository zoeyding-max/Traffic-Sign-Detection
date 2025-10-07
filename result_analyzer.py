"""
Results Analyzer
Analyzes YOLO detection results and generates statistics
"""

import numpy as np
from config import STATS_PRECISION


class ResultsAnalyzer:
    """Analyzes detection results and generates statistics"""
    
    @staticmethod
    def extract_detections(results):
        """
        Extract detection information from YOLO results
        
        Args:
            results: YOLO results object
            
        Returns:
            Dictionary with detection data
        """
        if len(results.boxes) == 0:
            return None
            
        classes = results.boxes.cls.cpu().numpy()
        confidences = results.boxes.conf.cpu().numpy()
        boxes = results.boxes.xyxy.cpu().numpy()
        names = results.names
        
        detections = []
        for i in range(len(classes)):
            detection = {
                'class_id': int(classes[i]),
                'class_name': names[int(classes[i])],
                'confidence': float(confidences[i]),
                'box': boxes[i].tolist()
            }
            detections.append(detection)
            
        return detections
    
    @staticmethod
    def group_by_class(detections):
        """
        Group detections by class
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            Dictionary grouped by class name
        """
        if not detections:
            return {}
            
        class_groups = {}
        for detection in detections:
            class_name = detection['class_name']
            
            if class_name not in class_groups:
                class_groups[class_name] = {
                    'count': 0,
                    'confidences': [],
                    'boxes': []
                }
            
            class_groups[class_name]['count'] += 1
            class_groups[class_name]['confidences'].append(detection['confidence'])
            class_groups[class_name]['boxes'].append(detection['box'])
        
        # Calculate max confidence and representative box for each class
        for class_name in class_groups:
            confidences = class_groups[class_name]['confidences']
            boxes = class_groups[class_name]['boxes']
            
            max_conf_idx = np.argmax(confidences)
            class_groups[class_name]['max_confidence'] = confidences[max_conf_idx]
            class_groups[class_name]['representative_box'] = boxes[max_conf_idx]
            
        return class_groups
    
    @staticmethod
    def calculate_statistics(detections):
        """
        Calculate detection statistics
        
        Args:
            detections: List of detection dictionaries
            
        Returns:
            Dictionary with statistics
        """
        if not detections:
            return {
                'total_detections': 0,
                'unique_classes': 0,
                'avg_confidence': 0.0,
                'max_confidence': 0.0,
                'min_confidence': 0.0
            }
        
        confidences = [d['confidence'] for d in detections]
        unique_classes = len(set(d['class_name'] for d in detections))
        
        stats = {
            'total_detections': len(detections),
            'unique_classes': unique_classes,
            'avg_confidence': np.mean(confidences),
            'max_confidence': np.max(confidences),
            'min_confidence': np.min(confidences)
        }
        
        return stats
    
    @staticmethod
    def format_statistics(stats):
        """
        Format statistics for display
        
        Args:
            stats: Statistics dictionary
            
        Returns:
            Formatted string
        """
        if stats['total_detections'] == 0:
            return 'No objects detected'
        
        precision = STATS_PRECISION
        
        formatted = f"""
Total Detections: {stats['total_detections']}
Unique Classes: {stats['unique_classes']}
Average Confidence: {stats['avg_confidence']:.{precision}%}
Max Confidence: {stats['max_confidence']:.{precision}%}
Min Confidence: {stats['min_confidence']:.{precision}%}
        """
        
        return formatted.strip()
    
    @staticmethod
    def format_box_coordinates(box):
        """
        Format box coordinates for display
        
        Args:
            box: List of coordinates [x1, y1, x2, y2]
            
        Returns:
            Formatted string
        """
        return f"({int(box[0])}, {int(box[1])}, {int(box[2])}, {int(box[3])})"