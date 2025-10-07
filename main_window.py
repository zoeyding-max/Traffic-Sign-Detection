"""
Main Application Window
Contains the main UI and application logic
"""

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QLabel, QVBoxLayout, 
                             QHBoxLayout, QWidget, QFileDialog, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QProgressBar)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from config import (WINDOW_TITLE, WINDOW_WIDTH, WINDOW_HEIGHT, 
                   VIDEO_EXTENSIONS, DEFAULT_CAMERA_INDEX)
from styles import (get_main_stylesheet, get_status_style, get_stats_style, 
                   get_image_label_style)
from model_handler import ModelHandler
from video_thread import VideoThread
from image_processor import ImageProcessor
from results_analyzer import ResultsAnalyzer
from batch_processor import BatchProcessor


class TrafficSignRecognition(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.model_handler = ModelHandler()
        self.batch_processor = BatchProcessor(self.model_handler)
        
        # State variables
        self.current_image = None
        self.video_thread = None
        self.camera_active = False
        
        # Initialize UI
        self.init_ui()
        
        # Load YOLO model
        self.load_model()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Apply stylesheet
        self.setStyleSheet(get_main_stylesheet())
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        
        # Create panels
        left_panel = self.create_left_panel()
        right_panel = self.create_right_panel()
        
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
    def create_left_panel(self):
        """Create left control panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Title
        title = QLabel('🚦 Traffic Sign Detection')
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Status label
        self.status_label = QLabel('Status: Ready')
        self.status_label.setStyleSheet(get_status_style('success'))
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        layout.addSpacing(20)
        
        # Control buttons
        self.create_control_buttons(layout)
        
        layout.addSpacing(20)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Statistics display
        stats_label = QLabel('📊 Detection Statistics')
        stats_label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(stats_label)
        
        self.stats_display = QLabel('No detections yet')
        self.stats_display.setStyleSheet(get_stats_style())
        self.stats_display.setWordWrap(True)
        layout.addWidget(self.stats_display)
        
        layout.addStretch()
        
        return panel
    
    def create_control_buttons(self, layout):
        """Create control buttons"""
        # Upload buttons
        btn_upload_image = QPushButton('📷 Upload Image')
        btn_upload_image.clicked.connect(self.upload_image)
        layout.addWidget(btn_upload_image)
        
        btn_upload_video = QPushButton('🎥 Upload Video')
        btn_upload_video.clicked.connect(self.upload_video)
        layout.addWidget(btn_upload_video)
        
        self.btn_camera = QPushButton('📹 Start Live Camera')
        self.btn_camera.clicked.connect(self.toggle_camera)
        layout.addWidget(self.btn_camera)
        
        btn_batch = QPushButton('📁 Batch Process Folder')
        btn_batch.clicked.connect(self.batch_process)
        layout.addWidget(btn_batch)
        
        layout.addSpacing(20)
        
        # Save buttons
        btn_save_image = QPushButton('💾 Save Annotated Image')
        btn_save_image.clicked.connect(self.save_image)
        layout.addWidget(btn_save_image)
        
        btn_stop = QPushButton('⏹️ Stop Processing')
        btn_stop.clicked.connect(self.stop_processing)
        layout.addWidget(btn_stop)
        
    def create_right_panel(self):
        """Create right display panel"""
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)
        
        # Image display
        self.image_label = QLabel('No image loaded')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(get_image_label_style())
        layout.addWidget(self.image_label, 3)
        
        # Results table
        results_label = QLabel('📋 Detection Results')
        results_label.setFont(QFont('Arial', 12, QFont.Bold))
        layout.addWidget(results_label)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(
            ['Class', 'Confidence', 'Box Coordinates', 'Count']
        )
        self.results_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.results_table, 2)
        
        return panel
    
    def load_model(self):
        """Load YOLO model"""
        self.update_status('Loading YOLO model...', 'info')
        
        success, message = self.model_handler.load_model()
        
        if success:
            self.update_status('Model loaded ✓', 'success')
        else:
            self.update_status('Model loading failed ✗', 'error')
            QMessageBox.critical(self, 'Error', message)
    
    def upload_image(self):
        """Upload and process a single image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select Image', '', 
            'Images (*.png *.jpg *.jpeg *.bmp)'
        )
        
        if file_path:
            self.process_image(file_path)
    
    def process_image(self, image_path):
        """Process image with YOLO detection"""
        try:
            self.update_status('Processing image...', 'info')
            
            # Read image
            image = ImageProcessor.read_image(image_path)
            if image is None:
                raise ValueError('Failed to load image')
            
            # Run detection
            results = self.model_handler.predict(image)
            annotated_image = self.model_handler.get_annotated_image(results)
            self.current_image = annotated_image
            
            # Display and analyze results
            self.display_image(annotated_image)
            self.analyze_and_display_results(results)
            
            self.update_status('Detection complete ✓', 'success')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Processing failed: {str(e)}')
            self.update_status('Processing failed ✗', 'error')
    
    def display_image(self, image):
        """Display image in label"""
        pixmap = ImageProcessor.numpy_to_pixmap(image)
        scaled_pixmap = ImageProcessor.scale_pixmap(
            pixmap, self.image_label.size()
        )
        self.image_label.setPixmap(scaled_pixmap)
    
    def analyze_and_display_results(self, results):
        """Analyze detection results and update displays"""
        # Extract detections
        detections = ResultsAnalyzer.extract_detections(results)
        
        if not detections:
            self.results_table.setRowCount(0)
            self.stats_display.setText('No objects detected')
            return
        
        # Group by class and update table
        class_groups = ResultsAnalyzer.group_by_class(detections)
        self.update_results_table(class_groups)
        
        # Calculate and display statistics
        stats = ResultsAnalyzer.calculate_statistics(detections)
        stats_text = ResultsAnalyzer.format_statistics(stats)
        self.stats_display.setText(stats_text)
    
    def update_results_table(self, class_groups):
        """Update detection results table"""
        self.results_table.setRowCount(0)
        
        row = 0
        for class_name, data in class_groups.items():
            self.results_table.insertRow(row)
            
            # Class name
            self.results_table.setItem(row, 0, QTableWidgetItem(class_name))
            
            # Confidence
            conf_text = f"{data['max_confidence']:.2%}"
            self.results_table.setItem(row, 1, QTableWidgetItem(conf_text))
            
            # Box coordinates
            box_text = ResultsAnalyzer.format_box_coordinates(
                data['representative_box']
            )
            self.results_table.setItem(row, 2, QTableWidgetItem(box_text))
            
            # Count
            self.results_table.setItem(row, 3, QTableWidgetItem(str(data['count'])))
            
            row += 1
    
    def upload_video(self):
        """Upload and process video file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select Video', '', 
            'Videos (*.mp4 *.avi *.mov *.mkv)'
        )
        
        if file_path:
            self.process_video(file_path)
    
    def process_video(self, video_path):
        """Process video with YOLO detection"""
        try:
            self.update_status('Processing video...', 'info')
            
            # Stop any existing thread
            self.stop_processing()
            
            # Create and start video thread
            self.video_thread = VideoThread(video_path, self.model_handler)
            self.video_thread.frame_ready.connect(self.display_image)
            self.video_thread.finished.connect(self.video_finished)
            self.video_thread.error_occurred.connect(self.handle_error)
            self.video_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Video processing failed: {str(e)}')
    
    def toggle_camera(self):
        """Toggle live camera detection"""
        if not self.camera_active:
            self.start_camera()
        else:
            self.stop_camera()
    
    def start_camera(self):
        """Start live camera detection"""
        try:
            self.update_status('Starting camera...', 'info')
            
            # Create and start camera thread
            self.video_thread = VideoThread(DEFAULT_CAMERA_INDEX, self.model_handler)
            self.video_thread.frame_ready.connect(self.display_image)
            self.video_thread.finished.connect(self.video_finished)
            self.video_thread.error_occurred.connect(self.handle_error)
            self.video_thread.start()
            
            self.camera_active = True
            self.btn_camera.setText('⏸️ Stop Camera')
            self.update_status('Camera running', 'success')
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Camera failed: {str(e)}')
    
    def stop_camera(self):
        """Stop live camera detection"""
        if self.video_thread and self.video_thread.isRunning():
            self.video_thread.stop()
            self.video_thread.wait()
        
        self.camera_active = False
        self.btn_camera.setText('📹 Start Live Camera')
        self.update_status('Camera stopped', 'info')
    
    def video_finished(self):
        """Handle video processing completion"""
        self.update_status('Video processing complete ✓', 'success')
        if self.camera_active:
            self.stop_camera()
    
    def stop_processing(self):
        """Stop all processing"""
        if self.video_thread and self.video_thread.isRunning():
            self.video_thread.stop()
            self.video_thread.wait()
        
        if self.camera_active:
            self.stop_camera()
        
        self.update_status('Processing stopped', 'info')
    
    def batch_process(self):
        """Batch process folder of images"""
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        
        if not folder_path:
            return
        
        try:
            self.update_status('Batch processing...', 'info')
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            
            # Progress callback
            def update_progress(current, total):
                progress = int((current / total) * 100)
                self.progress_bar.setValue(progress)
                from PyQt5.QtWidgets import QApplication
                QApplication.processEvents()
            
            # Process folder
            success_count, total_count, output_folder = self.batch_processor.process_folder(
                folder_path, progress_callback=update_progress
            )
            
            self.progress_bar.setVisible(False)
            
            if total_count == 0:
                QMessageBox.information(self, 'Info', 'No images found in folder')
                self.update_status('No images found', 'warning')
            else:
                self.update_status(f'Processed {success_count}/{total_count} images ✓', 'success')
                QMessageBox.information(
                    self, 'Success', 
                    f'Successfully processed {success_count} out of {total_count} images.\n'
                    f'Results saved to: {output_folder}'
                )
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, 'Error', f'Batch processing failed: {str(e)}')
            self.update_status('Batch processing failed ✗', 'error')
    
    def save_image(self):
        """Save current annotated image"""
        if self.current_image is None:
            QMessageBox.warning(self, 'Warning', 'No image to save')
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 'Save Image', 'detected_image.jpg',
            'Images (*.jpg *.png)'
        )
        
        if file_path:
            if ImageProcessor.save_image(self.current_image, file_path):
                QMessageBox.information(self, 'Success', 'Image saved successfully')
                self.update_status('Image saved ✓', 'success')
            else:
                QMessageBox.critical(self, 'Error', 'Failed to save image')
                self.update_status('Save failed ✗', 'error')
    
    def update_status(self, message, status_type='info'):
        """Update status label"""
        self.status_label.setText(f'Status: {message}')
        self.status_label.setStyleSheet(get_status_style(status_type))
    
    def handle_error(self, error_message):
        """Handle errors from threads"""
        QMessageBox.critical(self, 'Error', error_message)
        self.update_status('Error occurred ✗', 'error')
    
    def closeEvent(self, event):
        """Handle window close event"""
        self.stop_processing()
        event.accept()