import os
import shutil
import subprocess

def find_matching_mov(root, heic_file):
    base_name = os.path.splitext(heic_file)[0]
    for file in os.listdir(root):
        if file.lower().startswith(base_name.lower()) and file.lower().endswith('.mov'):
            return file
    return None

def process_directory(source_dir, output_dir):
    total_files = 0
    processed_live_photos = 0
    copied_files = 0

    # 獲取腳本的絕對路徑
    script_path = os.path.abspath("MotionPhoto2.ps1")

    for root, dirs, files in os.walk(source_dir):
        heic_files = [f for f in files if f.lower().endswith('.heic')]
        
        print(f"Found {len(heic_files)} HEIC files in directory {root}")

        # 處理所有檔案
        for file in files:
            total_files += 1
            if file.lower().endswith('.heic'):
                matching_mov = find_matching_mov(root, file)
                
                if matching_mov:
                    # Found a Live Photo pair
                    heic_path = os.path.join(root, file)
                    mov_path = os.path.join(root, matching_mov)
                    
                    # Create the corresponding output directory
                    rel_path = os.path.relpath(root, source_dir)
                    output_subdir = os.path.join(output_dir, rel_path)
                    os.makedirs(output_subdir, exist_ok=True)
                    
                    # Keep the .heic extension for the output file
                    output_path = os.path.join(output_subdir, file)
                    
                    # Execute the conversion script
                    cmd = f'powershell.exe -executionpolicy bypass -nologo -file "{script_path}" -imageFile "{heic_path}" -videoFile "{mov_path}" -outputFile "{output_path}"'
                    try:
                        subprocess.run(cmd, shell=True, check=True)
                        print(f"Processed Live Photo: {heic_path}")
                        processed_live_photos += 1
                    except subprocess.CalledProcessError as e:
                        print(f"Error processing Live Photo: {heic_path}")
                        print(f"Error message: {str(e)}")
                        # 如果處理失敗，仍然複製原始檔案
                        copy_file(root, file, source_dir, output_dir)
                        copied_files += 1
                else:
                    print(f"No matching MOV file found for: {file}")
                    copy_file(root, file, source_dir, output_dir)
                    copied_files += 1
            elif not file.lower().endswith('.mov') or not find_matching_mov(root, os.path.splitext(file)[0] + '.heic'):
                # 複製所有非 Live Photos 的檔案，包括沒有對應 HEIC 檔案的 MOV 檔案
                copy_file(root, file, source_dir, output_dir)
                copied_files += 1

    print(f"\nProcessing completed! Summary:")
    print(f"Total files processed: {total_files}")
    print(f"Live Photos processed: {processed_live_photos}")
    print(f"Regular files copied: {copied_files}")


def copy_file(root, file, source_dir, output_dir):
    source_path = os.path.join(root, file)
    rel_path = os.path.relpath(root, source_dir)
    dest_path = os.path.join(output_dir, rel_path, file)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(source_path, dest_path)
    print(f"Copied file: {source_path}")

if __name__ == "__main__":
    source_directory = input("Enter the source directory path: ")
    output_directory = input("Enter the output directory path: ")

    process_directory(source_directory, output_directory)
