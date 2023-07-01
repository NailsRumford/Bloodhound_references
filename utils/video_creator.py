import os
import subprocess
from typing import List, Tuple

class VideoCreator:
    """
    Class for creating videos from sorted sequences of images.
    """

    @staticmethod
    def create_videos(sequences: List[Tuple[str, int, List[Tuple[int, str, int]]]], output_folder: str) -> None:
        """
        Create videos from sorted sequences of images.

        Args:
            sequences (List[Tuple[str, int, List[Tuple[int, str, int]]]]): A list of sorted sequences.
                Each sequence is represented as a tuple containing name, padding, frames.
                Each frame is represented as a tuple containing frame number, image path, padding.
            output_folder (str): The folder path where the videos will be saved.
        """
        for sequence in sequences:
            name, padding, frames, output_filename, folder_path = sequence
            output_path = os.path.join(output_folder, output_filename)
            start_number = frames[0][0]
            input_pattern = os.path.join(folder_path, f"{name}_%{padding}d.jpg")
            ffmpeg_command = f"ffmpeg -framerate 30 -start_number {start_number} -i {input_pattern} -c:v mjpeg -q:v 2 -y {output_path}"

            try:
                subprocess.run(ffmpeg_command, shell=True, check=True)
                print(f"Created video: {output_path}")
            except subprocess.CalledProcessError as e:
                print(f"Error creating video: {output_path}")
                print(f"Command: {e.cmd}")
                print(f"Return code: {e.returncode}")
                print(f"Output: {e.output}")