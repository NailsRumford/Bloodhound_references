import sys
import os
import logging
from utils.image_finder import ImageFinder
from utils.sequence_sorter import SequenceSorter
from utils.video_creator import VideoCreator

def main():
    if len(sys.argv) != 2:
        logging.error("Usage: python main.py <folder_path>")
        return

    folder_path = sys.argv[1]

    if not os.path.isdir(folder_path):
        logging.error(f"Invalid folder path: {folder_path}")
        return

    image_finder = ImageFinder(folder_path)
    images = image_finder.find_images()

    if not images:
        logging.error("No images found in the specified folder.")
        return

    sorted_sequences = SequenceSorter.sort_sequences(images)

    if not sorted_sequences:
        logging.error("No image sequences found.")
        return

    output_folder = folder_path

    VideoCreator.create_videos(sorted_sequences, output_folder)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()