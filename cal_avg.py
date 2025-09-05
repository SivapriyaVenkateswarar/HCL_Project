import os
from regipy.registry import RegistryHive

# Define the root path and list of user profiles
ntuser_root = r'D:\Digital forensics\Extracted_Files\Disk_Img_1\Registry_Hives (under process)\Documents and Settings'
user_profiles = ['Administrator', 'Default User', 'domex1', 'domex2', 'LocalService', 'NetworkService']

def dump_registry_tree(key, indent=0):
    """Recursively dump registry key names and values."""
    try:
        print('  ' * indent + f"[+] Key: {key.name}")

        # Get all values under this key
        try:
            values = key.get_values()  
            for value in values:
                value_name = value.name if value.name else "(default)"
                print('  ' * (indent + 1) + f"- {value_name}: {value.value}")
        except Exception as e:
            print('  ' * (indent + 1) + f"[!] Error reading values: {e}")

        # Recurse into subkeys
        for subkey in key.iter_subkeys():
            dump_registry_tree(subkey, indent + 1)

    except Exception as e:
        print('  ' * indent + f"[!] Error walking key {key.name}: {e}")

# Loop over each NTUSER.DAT file for the specified users
for profile in user_profiles:
    ntuser_path = os.path.join(ntuser_root, profile, 'NTUSER.DAT')

    if os.path.exists(ntuser_path):
        print(f"\n[✔] Processing: {ntuser_path}")

        try:
            hive = RegistryHive(ntuser_path)
            root_key = hive.root
            dump_registry_tree(root_key)

        except Exception as e:
            print(f"[!] Error opening registry for {profile}: {e}")

    else:
        print(f"NTUSER.DAT not found for {profile}")

