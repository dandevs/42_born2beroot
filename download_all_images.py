#!/usr/bin/env python3
"""
Consolidated image downloader for Born2beRoot guide.
Downloads all 65 images from web.archive.org with retry logic.
"""

import os
import time
import random
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: requests module not found. Install with: pip install requests")
    exit(1)


# All images with their URLs and alt text
IMAGES = [
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-16-58-15.png", "name": "01_virtualbox_home.png", "alt": "VirtualBox Home"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-03-05.png", "name": "02_create_vm.png", "alt": "Create VM Window"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-06-40.png", "name": "03_memory_size.png", "alt": "Memory Size"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-12-07.png", "name": "04_hard_disk.png", "alt": "Hard Disk Creation"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-13-01.png", "name": "05_hard_disk_type.png", "alt": "Hard Disk File Type"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-13-40.png", "name": "06_storage_allocation.png", "alt": "Storage Allocation"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-15-23.png", "name": "07_file_location_size.png", "alt": "File Location and Size"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-17-53.png", "name": "08_vm_created.png", "alt": "VM Created"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/Screenshot-from-2022-03-02-17-21-33.png", "name": "09_startup_disk.png", "alt": "Select Startup Disk"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_24_47.png", "name": "10_debian_install_menu.png", "alt": "Debian Install Menu"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_30_54.png", "name": "11_language_selection.png", "alt": "Language Selection"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_32_01.png", "name": "12_location_selection.png", "alt": "Location Selection"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_33_44.png", "name": "13_keyboard_layout.png", "alt": "Keyboard Layout"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_39_44.png", "name": "14_hostname.png", "alt": "Hostname Configuration"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_41_01.png", "name": "15_domain_name.png", "alt": "Domain Name Configuration"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_43_19.png", "name": "16_root_password.png", "alt": "Root Password"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_46_06.png", "name": "17_new_user_fullname.png", "alt": "New User Full Name"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_46_50.png", "name": "18_new_user_username.png", "alt": "New User Username"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_17_48_11.png", "name": "19_new_user_password.png", "alt": "New User Password"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_02_52.png", "name": "20_partitioning_method.png", "alt": "Partitioning Method"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_03_24.png", "name": "21_select_disk.png", "alt": "Select Disk to Partition"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_03_47.png", "name": "22_create_partition_table.png", "alt": "Create Partition Table"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_06_28.png", "name": "23_select_free_space.png", "alt": "Select Free Space"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_06_41.png", "name": "24_create_new_partition.png", "alt": "Create New Partition"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_33.png", "name": "25_boot_partition_size.png", "alt": "Boot Partition Size"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_42.png", "name": "26_boot_partition_type.png", "alt": "Boot Partition Type"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_49.png", "name": "27_boot_partition_location.png", "alt": "Boot Partition Location"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_10.png", "name": "28_boot_mount_point.png", "alt": "Boot Mount Point"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_17.png", "name": "29_boot_mount_point_selection.png", "alt": "Select Boot Mount Point"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_31.png", "name": "30_boot_partition_done.png", "alt": "Boot Partition Done"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_17.png", "name": "31_select_free_space_2.png", "alt": "Select Remaining Free Space"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_26.png", "name": "32_create_new_partition_2.png", "alt": "Create Second Partition"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_40.png", "name": "33_lvm_partition_size.png", "alt": "LVM Partition Size"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_47.png", "name": "34_lvm_partition_type.png", "alt": "LVM Partition Type"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_06.png", "name": "35_lvm_mount_point.png", "alt": "LVM Partition Mount Point"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_19.png", "name": "36_lvm_do_not_mount.png", "alt": "Do Not Mount LVM Partition"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_44.png", "name": "37_lvm_partition_done.png", "alt": "LVM Partition Done"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_49_39.png", "name": "38_configure_encrypted_volumes.png", "alt": "Configure Encrypted Volumes"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_50_09.png", "name": "39_write_changes_encryption.png", "alt": "Write Changes for Encryption"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_50_41.png", "name": "40_create_encrypted_volumes.png", "alt": "Create Encrypted Volumes"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_08.png", "name": "41_select_partition_to_encrypt.png", "alt": "Select Partition to Encrypt"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_29.png", "name": "42_encryption_params_done.png", "alt": "Encryption Parameters Done"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_43.png", "name": "43_finish_encryption_setup.png", "alt": "Finish Encryption Setup"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_52.png", "name": "44_erase_data.png", "alt": "Erase Data"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_13_45.png", "name": "45_encryption_passphrase.png", "alt": "Encryption Passphrase"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_14_49.png", "name": "46_configure_lvm.png", "alt": "Configure LVM"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_05.png", "name": "47_write_changes_lvm.png", "alt": "Write Changes LVM"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_24.png", "name": "48_create_volume_group.png", "alt": "Create Volume Group"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_45.png", "name": "49_name_volume_group.png", "alt": "Name Volume Group"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_05.png", "name": "50_select_encrypted_partition.png", "alt": "Select Encrypted Partition"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_26.png", "name": "51_create_logical_volume.png", "alt": "Create Logical Volume"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_44.png", "name": "52_select_volume_group.png", "alt": "Select Volume Group"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_56.png", "name": "53_name_logical_volume.png", "alt": "Name Logical Volume"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_17_27.png", "name": "54_logical_volume_size.png", "alt": "Logical Volume Size"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_28_18.png", "name": "55_lvm_config_details.png", "alt": "LVM Configuration Details"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_29_51.png", "name": "56_select_lv_to_format.png", "alt": "Select Logical Volume to Format"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_29_59.png", "name": "57_use_as.png", "alt": "Use As"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_12.png", "name": "58_select_ext4.png", "alt": "Select EXT4"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_36.png", "name": "59_mount_point.png", "alt": "Select Mount Point"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_45.png", "name": "60_select_home_mount.png", "alt": "Select Home Mount Point"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_01_18.png", "name": "61_software_selection.png", "alt": "Software Selection"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_14_05.png", "name": "62_install_grub.png", "alt": "Install GRUB"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_14_12-1.png", "name": "63_select_grub_device.png", "alt": "Select GRUB Device"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_16_42.png", "name": "64_finish_installation.png", "alt": "Finish Installation"},
    {"src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_18_33.png", "name": "65_partitions_result.png", "alt": "Partitions Result"},
]

# Configuration
DOWNLOAD_DIR = Path(__file__).parent / "images"
MAX_RETRIES = 3
TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"


def download_file(session: requests.Session, url: str, filepath: Path, filename: str) -> bool:
    """Download a single file with retry logic."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = session.get(url, stream=True, timeout=TIMEOUT)
            response.raise_for_status()

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            # Verify file has content
            if filepath.stat().st_size == 0:
                raise ValueError("Downloaded file is 0 bytes")

            print(f"  [OK] {filename}")
            return True

        except Exception as e:
            if attempt < MAX_RETRIES:
                wait_time = 2 * attempt
                print(f"  [RETRY {attempt}/{MAX_RETRIES}] {filename}: {e} (retrying in {wait_time}s...)")
                time.sleep(wait_time)
            else:
                print(f"  [FAILED] {filename}: {e}")
                return False


def main():
    # Create download directory
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Setup session with headers
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})

    # Track stats
    total = len(IMAGES)
    downloaded = 0
    skipped = 0
    failed = []

    print(f"Starting download of {total} images to: {DOWNLOAD_DIR}")
    print("-" * 60)

    for i, img in enumerate(IMAGES, 1):
        filename = img["name"]
        filepath = DOWNLOAD_DIR / filename
        url = img["src"]

        # Check if file already exists and has content
        if filepath.exists() and filepath.stat().st_size > 0:
            print(f"[{i}/{total}] [SKIP] {filename} (already exists)")
            skipped += 1
            continue

        # Check if file exists but is empty (redownload)
        if filepath.exists() and filepath.stat().st_size == 0:
            print(f"[{i}/{total}] [RE-DOWNLOAD] {filename} (file was empty)")
            filepath.unlink()

        print(f"[{i}/{total}] [DOWNLOADING] {filename}")

        if download_file(session, url, filepath, filename):
            downloaded += 1
        else:
            failed.append(filename)

        # Be nice to the server
        time.sleep(random.uniform(0.5, 1.5))

    # Summary
    print("-" * 60)
    print(f"Download complete!")
    print(f"  Total:     {total}")
    print(f"  Downloaded:{downloaded}")
    print(f"  Skipped:   {skipped}")
    print(f"  Failed:    {len(failed)}")

    if failed:
        print("\nFailed downloads:")
        for f in failed:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
