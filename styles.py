"""
UI Styling for Traffic Sign Recognition System
Contains all CSS stylesheets for PyQt5 components
"""

def get_main_stylesheet():
    """Returns the main application stylesheet"""
    return """
        QMainWindow {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #1a1a2e, stop:1 #16213e);
        }
        
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #45a049);
            color: white;
            border: none;
            padding: 12px 24px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 8px;
            min-height: 40px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #45a049, stop:1 #3d8b40);
        }
        
        QPushButton:pressed {
            background: #3d8b40;
        }
        
        QLabel {
            color: #ffffff;
            font-size: 13px;
        }
        
        QTableWidget {
            background-color: #2d2d44;
            alternate-background-color: #252538;
            color: white;
            border: 2px solid #4CAF50;
            border-radius: 8px;
            gridline-color: #3d3d5c;
        }
        
        QTableWidget::item {
            padding: 8px;
        }
        
        QHeaderView::section {
            background-color: #1f1f38;
            color: white;
            padding: 10px;
            border: 1px solid #4CAF50;
            font-weight: bold;
        }
        
        QProgressBar {
            border: 2px solid #4CAF50;
            border-radius: 8px;
            text-align: center;
            background-color: #2d2d44;
            color: white;
        }
        
        QProgressBar::chunk {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #4CAF50, stop:1 #45a049);
        }
        
        QComboBox {
            background-color: #2d2d44;
            color: white;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            padding: 5px;
            min-height: 30px;
        }
    """

def get_status_style(status_type='success'):
    """Returns style for status labels"""
    colors = {
        'success': '#4CAF50',
        'error': '#f44336',
        'warning': '#ff9800',
        'info': '#2196F3'
    }
    color = colors.get(status_type, '#ffffff')
    return f'color: {color}; font-size: 14px;'

def get_stats_style():
    """Returns style for statistics display"""
    return """
        color: #ffffff; 
        padding: 10px; 
        background-color: #2d2d44; 
        border-radius: 5px;
    """

def get_image_label_style():
    """Returns style for image display label"""
    return """
        border: 3px solid #4CAF50; 
        border-radius: 10px; 
        background-color: #1a1a2e; 
        min-height: 400px;
    """