import os
import shutil
import subprocess

def find_matching_mov(root, heic_file):
    base_name = os.path.splitext(heic_file)[0]
    for file in os.listdir(root):
        if file.lower().startswith(base_name.lower()) and file.lower().endswith('.mov'):
            return file
    return None

def find_matching_heic(root, base_name):
    for file in os.listdir(root):
        if file.lower().startswith(base_name.lower()) and file.lower().endswith('.heic'):
            return True
    return False

def process_directory(source_dir, output_dir):
    total_files = 0
    processed_live_photos = 0
    copied_files = 0
    skipped_files = 0
    heic_count = 0
    mov_count = 0
    other_count = 0

    script_path = os.path.abspath("MotionPhoto2.ps1")

    for root, dirs, files in os.walk(source_dir):
        print(f"Processing directory: {root}")
        
        for file in files:
            total_files += 1
            if file.lower().endswith('.heic'):
                heic_count += 1
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
                    
                    # Construct the command as a list
                    cmd = [
                        'powershell.exe',
                        '-ExecutionPolicy', 'Bypass',
                        '-NoLogo',
                        '-File', script_path,
                        '-imageFile', heic_path,
                        '-videoFile', mov_path,
                        '-outputFile', output_path
                    ]

                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                        print(f"Processed Live Photo: {os.path.join(root, file)}")
                        processed_live_photos += 1
                    except subprocess.CalledProcessError as e:
                        print(f"Error processing Live Photo: {os.path.join(root, file)}")
                        print(f"Error message: {e}")
                        print(f"PowerShell output: {e.output}")
                        print(f"PowerShell error: {e.stderr}")
                        # 如果處理失敗，仍然複製原始檔案
                        copy_file(root, file, source_dir, output_dir)
                        copied_files += 1
                else:
                    print(f"No matching MOV file found for: {file}")
                    copy_file(root, file, source_dir, output_dir)
                    copied_files += 1
            elif file.lower().endswith('.mov'):
                mov_count += 1
                # 檢查是否有對應的 HEIC 檔案
                if not find_matching_heic(root, os.path.splitext(file)[0]):
                    copy_file(root, file, source_dir, output_dir)
                    copied_files += 1
                else:
                    # 如果有對應的 HEIC 檔案，跳過這個 MOV 檔案，因為它會在處理 HEIC 時一起處理
                    skipped_files += 1
                    print(f"Skipped MOV file (part of Live Photo): {os.path.join(root, file)}")
            else:
                # 複製所有其他類型的檔案
                other_count += 1
                copy_file(root, file, source_dir, output_dir)
                copied_files += 1

    print(f"\nProcessing completed! Summary:")
    print(f"Total files processed: {total_files}")
    print(f"Live Photos processed: {processed_live_photos}")
    print(f"Regular files copied: {copied_files}")
    print(f"Skipped files (MOV parts of Live Photos): {skipped_files}")
    print(f"Total handled (Live Photos + Copied + Skipped): {processed_live_photos + copied_files + skipped_files}")
    print(f"\nDetailed file type breakdown:")
    print(f"HEIC files: {heic_count}")
    print(f"MOV files: {mov_count}")
    print(f"Other files: {other_count}")

def copy_file(root, file, source_dir, output_dir):
    source_path = os.path.join(root, file)
    rel_path = os.path.relpath(root, source_dir)
    dest_path = os.path.join(output_dir, rel_path, file)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    shutil.copy2(source_path, dest_path)
    print(f"Copied file: {source_path}")

if __name__ == "__main__":
    source_directory = input("Enter the source directory path: ").strip('"')
    output_directory = input("Enter the output directory path: ").strip('"')

    process_directory(source_directory, output_directory)
