import sys
from utils.image_finder import ImageFinder
from utils.sequence_sorter import SequenceSorter
from utils.video_creator import VideoCreator

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
    else:
        folder_path = sys.argv[1]
    #folder_path = '/home/nailsrumford/Dev/Bloodhound_references/test'
    images = ImageFinder(folder_path).find_images()
    sorted_sequences = SequenceSorter.sort_sequences(images)
    output_folder = folder_path
    VideoCreator.create_videos(sorted_sequences, output_folder)
