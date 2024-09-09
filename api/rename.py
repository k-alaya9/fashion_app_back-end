import os
import shutil

def rename_and_move_files(src_dir, dest_dir1, dest_dir2, file1_old_name, file1_new_name, file2_old_name, file2_new_name):
    # Ensure the destination directories exist
    if not os.path.exists(dest_dir1):
        os.makedirs(dest_dir1)
    
    if not os.path.exists(dest_dir2):
        os.makedirs(dest_dir2)

    # Rename the first file
    file1_old_path = os.path.join(src_dir, file1_old_name)
    file1_new_path = os.path.join(src_dir, file1_new_name)
    
    if os.path.exists(file1_old_path):
        os.rename(file1_old_path, file1_new_path)
        print(f"Renamed {file1_old_name} to {file1_new_name}")
    else:
        print(f"File {file1_old_name} does not exist")

    # Rename the second file
    file2_old_path = os.path.join(src_dir, file2_old_name)
    file2_new_path = os.path.join(src_dir, file2_new_name)
    
    if os.path.exists(file2_old_path):
        os.rename(file2_old_path, file2_new_path)
        print(f"Renamed {file2_old_name} to {file2_new_name}")
    else:
        print(f"File {file2_old_name} does not exist")

    # Move the renamed files to their respective destination directories
    file1_dest_path = os.path.join(dest_dir1, file1_new_name)
    file2_dest_path = os.path.join(dest_dir2, file2_new_name)
    
    if os.path.exists(file1_new_path):
        shutil.move(file1_new_path, file1_dest_path)
        print(f"Moved {file1_new_name} to {dest_dir1}")
    else:
        print(f"File {file1_new_name} does not exist in {src_dir}")

    if os.path.exists(file2_new_path):
        shutil.move(file2_new_path, file2_dest_path)
        print(f"Moved {file2_new_name} to {dest_dir2}")
    else:
        print(f"File {file2_new_name} does not exist in {src_dir}")

# Example usage:
src_directory = r"C:\Users\ASUS\Desktop\hd\test\image"
dest_directory1 = r"C:\Users\ASUS\Desktop\hd\test\openpose_json"  
dest_directory2 = r"C:\Users\ASUS\Desktop\hd\test\openpose_img"  
file1_old = "0.jpg.json"  
file1_new = "0_keypoints.json"  
file2_old = "0_keypoints.jpg"  
file2_new = "0_rendered.png"  

rename_and_move_files(src_directory, dest_directory1, dest_directory2, file1_old, file1_new, file2_old, file2_new)
