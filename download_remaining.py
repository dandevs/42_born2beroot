import requests
import json
import os
import time

images = [
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_02_52.png",
    "name": "20_partitioning_method.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_03_24.png",
    "name": "21_select_disk.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_03_47.png",
    "name": "22_create_partition_table.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_06_28.png",
    "name": "23_select_free_space.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_06_41.png",
    "name": "24_create_new_partition.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_33.png",
    "name": "25_boot_partition_size.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_42.png",
    "name": "26_boot_partition_type.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_45_49.png",
    "name": "27_boot_partition_location.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_10.png",
    "name": "28_boot_mount_point.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_17.png",
    "name": "29_boot_mount_point_selection.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_46_31.png",
    "name": "30_boot_partition_done.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_17.png",
    "name": "31_select_free_space_2.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_26.png",
    "name": "32_create_new_partition_2.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_40.png",
    "name": "33_lvm_partition_size.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_47_47.png",
    "name": "34_lvm_partition_type.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_06.png",
    "name": "35_lvm_mount_point.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_19.png",
    "name": "36_lvm_do_not_mount.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_48_44.png",
    "name": "37_lvm_partition_done.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_49_39.png",
    "name": "38_configure_encrypted_volumes.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_50_09.png",
    "name": "39_write_changes_encryption.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_50_41.png",
    "name": "40_create_encrypted_volumes.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_08.png",
    "name": "41_select_partition_to_encrypt.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_29.png",
    "name": "42_encryption_params_done.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_43.png",
    "name": "43_finish_encryption_setup.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_18_51_52.png",
    "name": "44_erase_data.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_13_45.png",
    "name": "45_encryption_passphrase.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_14_49.png",
    "name": "46_configure_lvm.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_05.png",
    "name": "47_write_changes_lvm.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_24.png",
    "name": "48_create_volume_group.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_15_45.png",
    "name": "49_name_volume_group.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_05.png",
    "name": "50_select_encrypted_partition.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_26.png",
    "name": "51_create_logical_volume.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_44.png",
    "name": "52_select_volume_group.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_16_56.png",
    "name": "53_name_logical_volume.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_17_27.png",
    "name": "54_logical_volume_size.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_28_18.png",
    "name": "55_lvm_config_details.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_29_51.png",
    "name": "56_select_lv_to_format.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_29_59.png",
    "name": "57_use_as.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_12.png",
    "name": "58_select_ext4.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_36.png",
    "name": "59_mount_point.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_20_30_45.png",
    "name": "60_select_home_mount.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_01_18.png",
    "name": "61_software_selection.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_14_05.png",
    "name": "62_install_grub.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_14_12-1.png",
    "name": "63_select_grub_device.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_16_42.png",
    "name": "64_finish_installation.png"
  },
  {
    "src": "https://web.archive.org/web/20220508112710im_/https://www.codequoi.com/wp-content/uploads/2022/03/VirtualBox_Born2beroot_02_03_2022_21_18_33.png",
    "name": "65_partitions_result.png"
  }
]

download_dir = "/home/danimend/Documents/Projects/Notes/Born2beRoot/images"
headers = {'User-Agent': 'Mozilla/5.0'}

for i, img in enumerate(images):
    try:
        if os.path.exists(os.path.join(download_dir, img["name"])):
            print(f"Skipping {img['name']}, already exists.")
            continue
            
        print(f"Downloading {img['name']}...")
        response = requests.get(img["src"], stream=True, headers=headers)
        response.raise_for_status()
        with open(os.path.join(download_dir, img["name"]), 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {img['name']}")
        time.sleep(1) # Be polite and avoid rate limits
    except Exception as e:
        print(f"Failed to download {img['name']}: {e}")
