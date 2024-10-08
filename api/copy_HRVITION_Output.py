import os
import shutil

def copy_folder_files(source, destination):
    # Iterate over all items in the source directory
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isdir(source_path):
            # If the item is a directory, recursively copy its contents
            shutil.copytree(source_path, destination_path, dirs_exist_ok=True)
        else:
            # If the item is a file, copy it to the destination directory
            shutil.copy2(source_path, destination_path)
        
        print(f"Copied: _Data -> HR-VITON/data/test")

# Source directory
source_directory = r'C:\Users\ASUS\HR-VITON\output'

# Destination directory
destination_directory = r'C:\Users\ASUS\Desktop\FashionAppBackend-main\static\media\media\model_photo'

# Copy the folder/files from source to destination
copy_folder_files(source_directory, destination_directory)

