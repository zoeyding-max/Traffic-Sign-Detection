"""
Batch Processor
Handles batch processing of multiple images
"""

from pathlib import Path
from config import IMAGE_EXTENSIONS, OUTPUT_FOLDER_NAME, OUTPUT_IMAGE_PREFIX
from image_processor import ImageProcessor


class BatchProcessor:
    """Handles batch processing of images"""
    
    def __init__(self, model_handler):
        """
        Initialize batch processor
        
        Args:
            model_handler: ModelHandler instance for inference
        """
        self.model_handler = model_handler
        
    def find_images(self, folder_path):
        """
        Find all image files in folder
        
        Args:
            folder_path: Path to folder
            
        Returns:
            List of image file paths
        """
        folder = Path(folder_path)
        image_files = []
        
        for ext in IMAGE_EXTENSIONS:
            image_files.extend(folder.glob(f'*{ext}'))
            image_files.extend(folder.glob(f'*{ext.upper()}'))
            
        return sorted(image_files)
    
    def create_output_folder(self, input_folder):
        """
        Create output folder for processed images
        
        Args:
            input_folder: Input folder path
            
        Returns:
            Path to output folder
        """
        output_folder = Path(input_folder) / OUTPUT_FOLDER_NAME
        output_folder.mkdir(exist_ok=True)
        return output_folder
    
    def process_folder(self, folder_path, progress_callback=None):
        """
        Process all images in folder
        
        Args:
            folder_path: Path to folder containing images
            progress_callback: Optional callback function(current, total)
            
        Returns:
            Tuple (success_count, total_count, output_folder)
        """
        # Find images
        image_files = self.find_images(folder_path)
        total = len(image_files)
        
        if total == 0:
            return 0, 0, None
        
        # Create output folder
        output_folder = self.create_output_folder(folder_path)
        
        # Process each image
        success_count = 0
        for i, img_path in enumerate(image_files):
            try:
                # Read image
                image = ImageProcessor.read_image(str(img_path))
                if image is None:
                    continue
                
                # Run detection
                results = self.model_handler.predict(image)
                annotated_image = self.model_handler.get_annotated_image(results)
                
                # Save result
                output_path = output_folder / f'{OUTPUT_IMAGE_PREFIX}{img_path.name}'
                if ImageProcessor.save_image(annotated_image, str(output_path)):
                    success_count += 1
                
            except Exception as e:
                print(f"Error processing {img_path.name}: {str(e)}")
                continue
            
            # Call progress callback
            if progress_callback:
                progress_callback(i + 1, total)
        
        return success_count, total, output_folder