import os

folder_path = 'E:/gameMusic'

try:
    files = os.listdir(folder_path)
    print("Files in the directory:")
    for file in files:
        print(file)
except Exception as e:
    print(f"An error occurred: {e}")
