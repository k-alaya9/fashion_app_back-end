#
# file1 = r"C:\Users\ASUS\Desktop\FashionAppBackend-main\static\media\media\user_photo\IMG_20240822_102636_765.jpg"
# dir1 = r'C:\Users\ASUS\Desktop\hd\test\image'
#
# file2 = r"C:\Users\ASUS\Desktop\FashionAppBackend-main\static\media\media\cloths_photo\IMG_20240822_102639_101.jpg"
# dir2=   r'C:\Users\ASUS\Desktop\hd\test\cloth'
import shutil
import os
import argparse

def move_files(file1, dir1, file2, dir2):
    # Ensure the destination directories exist
    os.makedirs(dir1, exist_ok=True)
    os.makedirs(dir2, exist_ok=True)

    # Move file1 to dir1
    shutil.move(file1, os.path.join(dir1, os.path.basename(file1)))

    # Move file2 to dir2
    shutil.move(file2, os.path.join(dir2, os.path.basename(file2)))

    print(f"{file1} has been moved to {dir1}")
    print(f"{file2} has been moved to {dir2}")

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Move two files to specified directories.")
    parser.add_argument("file1", help="The path to the first file to be moved.")
    parser.add_argument("dir1", help="The destination directory for the first file.")
    parser.add_argument("file2", help="The path to the second file to be moved.")
    parser.add_argument("dir2", help="The destination directory for the second file.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function with the parsed arguments
    move_files(args.file1, args.dir1, args.file2, args.dir2)
