"""
Traffic Sign Recognition System
Main application entry point
"""

import sys
from PyQt5.QtWidgets import QApplication
from main_window import TrafficSignRecognition


def main():
    """Main application entry point"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application metadata
    app.setApplicationName("Traffic Sign Recognition System")
    app.setOrganizationName("Zoey Ding")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = TrafficSignRecognition()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()