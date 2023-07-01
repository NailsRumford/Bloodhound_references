import os
import subprocess
from typing import List, Tuple
import logging

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
            ffmpeg_command = VideoCreator._build_ffmpeg_command(input_pattern, output_path, start_number)

            try:
                subprocess.run(ffmpeg_command, shell=True, check=True)
                logging.info(f"Created video: {output_path}")
            except Exception as e:
                logging.error(f"Error creating video: {output_path}")
                logging.error(f"Command: {ffmpeg_command}")
                logging.error(f"Error message: {str(e)}")

    @staticmethod
    def _build_ffmpeg_command(input_pattern: str, output_path: str, start_number: int) -> str:
        """
        Build the FFmpeg command for creating a video.

        Args:
            input_pattern (str): The input image pattern.
            output_path (str): The output video path.
            start_number (int): The starting frame number.

        Returns:
            str: The FFmpeg command.
        """
        framerate = 30
        codec = "mjpeg"
        quality = 2

        return f"ffmpeg -framerate {framerate} -start_number {start_number} -i {input_pattern} -c:v {codec} -q:v {quality} -y {output_path}"