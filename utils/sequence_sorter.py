import os
from typing import Dict, List, Tuple
import logging

class SequenceSorter:
    """
    Class for sorting sequences of images.
    """

    @staticmethod
    def sort_sequences(images: List[str]) -> List[Tuple[str, int, List[Tuple[int, str, int]]]]:
        """
        Sort sequences of images based on their names.

        Args:
            images (List[str]): A list of paths to the images.

        Returns:
            List[Tuple[str, int, List[Tuple[int, str, int]]]]: A list of sorted sequences.
                Each sequence is represented as a tuple containing name, padding, frames.
                Each frame is represented as a tuple containing frame number, image path, padding.
        """
        if not images:
            logging.warning("No images found. Empty list provided.")
            return []

        sequences: Dict[str, List[Tuple[int, str, int]]] = {}

        for image_path in images:
            filename = os.path.basename(image_path)
            name, frame, padding = SequenceSorter._parse_filename(filename)

            if name in sequences:
                sequences[name].append((frame, image_path, padding))
            else:
                sequences[name] = [(frame, image_path, padding)]

        sorted_sequences = []
        for name, frames_list in sequences.items():
            frames_list.sort(key=lambda x: x[0])
            padding = frames_list[0][2]
            output_filename = name + '.mov'
            first_frame_path = frames_list[0][1]
            folder_path = os.path.dirname(first_frame_path)
            sorted_sequences.append((name, padding, frames_list, output_filename, folder_path))

        return sorted_sequences

    @staticmethod
    def _parse_filename(filename: str) -> Tuple[str, int, int]:
        """
        Parse the filename and extract sequence information.

        Args:
            filename (str): The filename to parse.

        Returns:
            Tuple[str, int, int]: A tuple containing name, frame number, and padding.
        """
        parts = filename.split('_')
        if len(parts) < 2:
            raise ValueError(f"Invalid filename format: {filename}")

        name = '_'.join(parts[:-1])
        last_part = parts[-1].split('.')[0]
        padding = len(last_part)
        frame = int(''.join(filter(str.isdigit, last_part)))

        return name, frame, padding