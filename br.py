import os
import sys
import subprocess

def find_images(root_folder):
    images = []

    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.jpg'):
                images.append(os.path.join(root, file))

    return images

def sort_sequences(images):
    sequences = {}

    for image_path in images:
        filename = os.path.basename(image_path)
        name, frame, padding = parse_filename(filename)

        if name in sequences:
            sequences[name].append((frame, image_path, padding))
        else:
            sequences[name] = [(frame, image_path, padding)]

    sorted_sequences = []
    for name, frames in sequences.items():
        frames.sort(key=lambda x: x[0])
        padding = frames[0][2]
        output_filename = name + '.mov'
        first_frame_path = frames[0][1]
        folder_path = os.path.dirname(first_frame_path)
        sorted_sequences.append((name, padding, frames, output_filename, folder_path))

    return sorted_sequences

def parse_filename(filename):
    parts = filename.split('_')
    if len(parts) < 2:
        raise ValueError(f"Invalid filename format: {filename}")

    name = '_'.join(parts[:-1])
    last_part = parts[-1].split('.')[0]
    padding = len(last_part)
    frame = int(''.join(filter(str.isdigit, last_part)))

    return name, frame, padding

def create_videos(sequences, output_folder):
    for sequence in sequences:
        name, padding, frames, output_filename, folder_path = sequence
        output_path = os.path.join(output_folder, output_filename)
        start_number = frames[0][0]
        input_pattern = os.path.join(folder_path, f"{name}_%{padding}d.jpg")
        ffmpeg_command = f"ffmpeg -framerate 30 -start_number {start_number} -i /{input_pattern} -c:v mjpeg -q:v 2 -y {output_path}"
        #ffmpeg_command = f"ffmpeg -framerate 24 -i {input_pattern} -c:v mjpeg -q:v 2 -y {output_path}"

        try:
            subprocess.run(ffmpeg_command, shell=True, check=True)
            print(f"Created video: {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error creating video: {output_path}")
            print(f"Command: {e.cmd}")
            print(f"Return code: {e.returncode}")
            print(f"Output: {e.output}")

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <folder_path>")
    # else:
    #     folder_path = sys.argv[1]
    folder_path = '/home/nailsrumford/Dev/Bloodhound_references/test'
    images = find_images(folder_path)
    sorted_sequences = sort_sequences(images)
    output_folder = folder_path
    create_videos(sorted_sequences, output_folder)
