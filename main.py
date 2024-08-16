import os
import shutil
import subprocess

def find_matching_mov(root, heic_file):
    base_name = os.path.splitext(heic_file)[0]
    for file in os.listdir(root):
        if file.lower().startswith(base_name.lower()) and file.lower().endswith('.mov'):
            return file
    return None

def process_directory(source_dir, output_dir, script_path):
    total_files = 0
    processed_live_photos = 0
    copied_files = 0

    for root, dirs, files in os.walk(source_dir):
        heic_files = [f for f in files if f.lower().endswith('.heic')]
        
        print(f"Found {len(heic_files)} HEIC files in directory {root}")

        for heic_file in heic_files:
            matching_mov = find_matching_mov(root, heic_file)
            
            if matching_mov:
                # Found a Live Photo pair
                heic_path = os.path.join(root, heic_file)
                mov_path = os.path.join(root, matching_mov)
                
                # Create the corresponding output directory
                rel_path = os.path.relpath(root, source_dir)
                output_subdir = os.path.join(output_dir, rel_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                # Keep the .heic extension for the output file
                output_path = os.path.join(output_subdir, heic_file)
                
                # Execute the conversion script
                cmd = f'powershell.exe -executionpolicy bypass -nologo -file "{script_path}" -imageFile "{heic_path}" -videoFile "{mov_path}" -outputFile "{output_path}"'
                try:
                    subprocess.run(cmd, shell=True, check=True)
                    print(f"Processed Live Photo: {heic_path}")
                    processed_live_photos += 1
                except subprocess.CalledProcessError as e:
                    print(f"Error processing Live Photo: {heic_path}")
                    print(f"Error message: {str(e)}")
            else:
                print(f"No matching MOV file found for: {heic_file}")
                copy_file(root, heic_file, source_dir, output_dir)
                copied_files += 1
            
            total_files += 1
        
        # Copy all files that are not part of Live Photos
        for file in files:
            if not file.lower().endswith('.heic') and not (file.lower().endswith('.mov') and find_matching_mov(root, os.path.splitext(file)[0] + '.heic')):
                copy_file(root, file, source_dir, output_dir)
                copied_files += 1
                total_files += 1

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
    script_path = input("Enter the full path of MotionPhoto2.ps1 script: ")

    process_directory(source_directory, output_directory, script_path)
