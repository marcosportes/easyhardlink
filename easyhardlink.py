import os
import sys
import subprocess

def create_hardlink(source_dir, dest_dir):
    # Check if the destination directory exists, otherwise create it
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Iterate over all files and subdirectories in the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Create the full path for the source file
            source_path = os.path.join(root, file)

            # Create the full path for the destination file
            dest_path = os.path.join(dest_dir, os.path.relpath(source_path, source_dir))

            # Create the destination directory if it doesn't exist
            dest_dir_path = os.path.dirname(dest_path)
            if not os.path.exists(dest_dir_path):
                os.makedirs(dest_dir_path)

            # Check if the destination file already exists
            if os.path.exists(dest_path):
                # Ask for confirmation to replace the existing file
                answer = input(f"File '{dest_path}' already exists. Do you want to replace it? (y/n): ")
                if answer.lower() != "y":
                    continue

                # Replace the existing file by using the -f option with ln command
                subprocess.run(["ln", "-f", source_path, dest_path])
            else:
                # Create the hardlink from the source file to the destination using the ln command
                subprocess.run(["ln", source_path, dest_path])

            print(f"Created hardlink for: {dest_path}")

if __name__ == "__main__":
    # Check if the command-line arguments are passed correctly
    if len(sys.argv) != 3:
        print("Usage: python create_hardlink.py <source_directory> <destination_directory>")
        sys.exit(1)

    source_directory = sys.argv[1]
    destination_directory = sys.argv[2]

    create_hardlink(source_directory, destination_directory)

