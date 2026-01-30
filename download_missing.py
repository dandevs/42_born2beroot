import requests
import os
import time
import random

# List of files that were identified as missing or empty (0 bytes) in the previous step
missing_files = [
    "21_select_disk.png",
    "23_select_free_space.png",
    "24_create_new_partition.png",
    "27_boot_partition_location.png",
    "29_boot_mount_point_selection.png",
    "32_create_new_partition_2.png",
    "34_lvm_partition_type.png",
    "35_lvm_mount_point.png",
    "36_lvm_do_not_mount.png",
    "37_lvm_partition_done.png",
    "38_configure_encrypted_volumes.png",
    "39_write_changes_encryption.png",
    "40_create_encrypted_volumes.png",
    "44_erase_data.png",
    "46_configure_lvm.png",
    "47_write_changes_lvm.png",
    "48_create_volume_group.png",
    "51_create_logical_volume.png",
    "54_logical_volume_size.png",
    "55_lvm_config_details.png",
    "56_select_lv_to_format.png",
    "57_use_as.png",
    "58_select_ext4.png",
    "59_mount_point.png",
    "61_software_selection.png",
    "64_finish_installation.png"
]

# Mapping from filename to URL (re-declared for safety)
images_map = {
  "21_select_disk.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_03_24.png",
  "23_select_free_space.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_06_28.png",
  "24_create_new_partition.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_06_41.png",
  "27_boot_partition_location.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_49.png",
  "29_boot_mount_point_selection.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_17.png",
  "32_create_new_partition_2.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_26.png",
  "34_lvm_partition_type.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_47.png",
  "35_lvm_mount_point.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_06.png",
  "36_lvm_do_not_mount.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_19.png",
  "37_lvm_partition_done.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_44.png",
  "38_configure_encrypted_volumes.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_49_39.png",
  "39_write_changes_encryption.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_50_09.png",
  "40_create_encrypted_volumes.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_50_41.png",
  "44_erase_data.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_52.png",
  "46_configure_lvm.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_14_49.png",
  "47_write_changes_lvm.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_05.png",
  "48_create_volume_group.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_24.png",
  "51_create_logical_volume.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_26.png",
  "54_logical_volume_size.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_17_27.png",
  "55_lvm_config_details.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_28_18.png",
  "56_select_lv_to_format.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_29_51.png",
  "57_use_as.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_29_59.png",
  "58_select_ext4.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_12.png",
  "59_mount_point.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_36.png",
  "61_software_selection.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_01_18.png",
  "64_finish_installation.png": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_16_42.png"
}

download_dir = "/home/danimend/Documents/Projects/Notes/Born2beRoot/images"

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

print(f"Attempting to download {len(missing_files)} missing files...")

for filename in missing_files:
    url = images_map.get(filename)
    if not url:
        print(f"No URL found for {filename}")
        continue
        
    filepath = os.path.join(download_dir, filename)
    
    # Retry loop
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(f"Downloading {filename} (Attempt {attempt+1}/{max_retries})...")
            response = session.get(url, stream=True, timeout=10)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            if os.path.getsize(filepath) > 0:
                print(f"Success: {filename}")
                break
            else:
                print(f"Warning: {filename} is 0 bytes.")
                
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            time.sleep(2 * (attempt + 1)) # Exponential backoff
            
    # Delay between files
    time.sleep(random.uniform(1.0, 3.0))

print("Download process completed.")
