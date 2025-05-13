import os
import shutil

def copy_files_recursive(source_dir_path, dest_dir_path):
    # Add this check at the beginning
    if not os.path.exists(source_dir_path):
        print(f"Warning: Source directory {source_dir_path} not found")
        return

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)  # Use makedirs to create parent directories if needed

    for item_name in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, item_name)
        dest_path = os.path.join(dest_dir_path, item_name)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        elif os.path.isdir(from_path):
            copy_files_recursive(from_path, dest_path)