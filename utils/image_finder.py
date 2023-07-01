import os
from typing import List

class ImageFinder:
    """
    Class for finding images in a given root folder.
    """

    def __init__(self, root_folder: str):
        """
        Initialize ImageFinder object.

        Args:
            root_folder (str): The root folder where images will be searched.
        """
        self.root_folder = root_folder

    def find_images(self) -> List[str]:
        """
        Find images in the root folder and its subdirectories.

        Returns:
            List[str]: A list of paths to the found images.
        """
        images = []

        try:
            for root, dirs, files in os.walk(self.root_folder):
                for file in files:
                    if file.lower().endswith('.jpg'):
                        images.append(os.path.join(root, file))
        except (OSError, IOError) as e:
            print(f"Error occurred while searching for images: {e}")

        return images