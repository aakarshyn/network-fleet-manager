
import os
import winreg
from datetime import datetime, timedelta

def get_downloads_path():
    
    return os.path.join(os.path.expanduser('~'), 'Downloads')

def convert_windows_timestamp(low_dw, high_dw):
    
    try:
        if low_dw == 0 and high_dw == 0:
            return "N/A"
        filetime = (high_dw << 32) + low_dw
        
        microseconds = filetime / 10
        sub_time = datetime(1601, 1, 1) + timedelta(microseconds=microseconds)
        return sub_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return "Unknown"

def mine_usb_history():
    
    downloads_dir = get_downloads_path()
    usb_telemetry = []
    
    try:
        
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Enum\USBSTOR")
        device_classes_count = winreg.QueryInfoKey(hkey)[0]
        
        for i in range(device_classes_count):
            try:
                device_class = winreg.EnumKey(hkey, i)
                
            
                vendor = "Unknown Vendor"
                product = "Unknown Product"
                if "Ven_" in device_class:
                    vendor = device_class.split("Ven_")[1].split("&")[0]
                if "Prod_" in device_class:
                    product = device_class.split("Prod_")[1].split("&")[0]

                sub_hkey = winreg.OpenKey(hkey, device_class)
                instances_count = winreg.QueryInfoKey(sub_hkey)[0]
                
                
                for j in range(instances_count):
                    serial_no = winreg.EnumKey(sub_hkey, j)
                    
                    
                    instance_path = f"SYSTEM\\CurrentControlSet\\Enum\\USBSTOR\\{device_class}\\{serial_no}"
                    inst_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, instance_path)
                    
                    
                    _, _, last_write_time = winreg.QueryInfoKey(inst_key)
                  
                    last_conn_str = datetime(1970, 1, 1) + timedelta(microseconds=last_write_time / 10)
                    last_conn_fmt = last_conn_str.strftime('%Y-%m-%d %H:%M:%S')

                    usb_entry = {
                        "vendor_name": vendor,
                        "product_id": product,
                        "serial_number": serial_no.split("&")[0], # Strip trailing port instance flags
                        "first_install_time": "N/A (Managed via Log API)",
                        "last_connected_time": last_conn_fmt
                    }
                    usb_telemetry.append(usb_entry)

                    
                    file_name = f"_USB{j}.txt"
                    usb_file_path = os.path.join(downloads_dir, file_name)
                    with open(usb_file_path, 'w', encoding='utf-8') as f:
                        f.write(f"Vendor: {vendor}\n")
                        f.write(f"Product ID: {product}\n")
                        f.write(f"Serial Number: {serial_no}\n")
                        f.write(f"First Install Time: N/A (Managed via Log API)\n")
                        f.write(f"Last Connected Time: {last_conn_fmt}\n")
                        
            except (KeyError, FileNotFoundError, PermissionError):
                continue
        winreg.CloseKey(hkey)
    except (FileNotFoundError, PermissionError):
        pass
        
    return usb_telemetry

def mine_user_sessions():
    
    session_logs = []
    
   
    try:
        url_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Internet Explorer\TypedURLs")
        val_count = winreg.QueryInfoKey(url_key)[1]
        for i in range(val_count):
            val_name, val_data, _ = winreg.EnumValue(url_key, i)
            session_logs.append(f"[TYPED_URL] {val_name}: {val_data}")
        winreg.CloseKey(url_key)
    except (FileNotFoundError, PermissionError):
        session_logs.append("[TYPED_URL] Status: Access Denied or No History Found")

  
    try:
        profile_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList")
        subkeys_count = winreg.QueryInfoKey(profile_key)[0]
        for i in range(subkeys_count):
            sub_name = winreg.EnumKey(profile_key, i)
            
            if sub_name.startswith("S-1-5-21"):
                session_logs.append(f"[PROFILE_FOUND] Identifier SID: {sub_name}")
        winreg.CloseKey(profile_key)
    except (FileNotFoundError, PermissionError):
        pass

    
    session_logs.append("[USER_SESSION_STATE] Status: [LOGOUT: CURRENTLY IN USE]")
    return session_logs

def run_forensic_harvest():
    """
    Master compiler loop. Gathers processed registry data feeds and structures
    them directly into the global tracking repository file _DeviceLogs.txt.
    """
    downloads_dir = get_downloads_path()
    
   
    usbs = mine_usb_history()
    sessions = mine_user_sessions()

    
    device_log_path = os.path.join(downloads_dir, "_DeviceLogs.txt")
    with open(device_log_path, 'w', encoding='utf-8') as f:
        f.write("=== COMPREHENSIVE FORENSIC DEVICE TELEMETRY LOG ===\n\n")
        f.write("--- HISTORICAL USB MASS STORAGE TELEMETRY ---\n")
        if usbs:
            for usb in usbs:
                f.write(f"Device: {usb['vendor_name']} {usb['product_id']} | "
                        f"Serial: {usb['serial_number']} | "
                        f"Last Contacted: {usb['last_connected_time']}\n")
        else:
            f.write("No Active/Historical USB Devices Found\n")
        
        f.write("\n--- USER SESSION FORENSIC FOOTPRINTS ---\n")
        for log in sessions:
            f.write(f"{log}\n")

if __name__ == "__main__":
    
    print("Initializing Core Python Kernel Registry Forensic Harvester...")
    run_forensic_harvest()
    print(f"Extraction sequence complete. Target assets generated inside: {get_downloads_path()}")