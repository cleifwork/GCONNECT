import os
import subprocess

# Get the script directory for relative file references
exe_dir = os.path.dirname(os.path.abspath(__file__))
python_exe = os.path.join(exe_dir, "python", "python311", "python.exe")
pythonw_exe = os.path.join(exe_dir, "python", "python311", "pythonw.exe")

FILE_PATHS = {
    "app": os.path.join(exe_dir, 'app'),
    "backup_folder": os.path.join(exe_dir, 'backup'),
    "csv_folder": os.path.join(exe_dir, 'raw_csv'),
    "macro_mod": os.path.join(exe_dir, 'macro_mod'),
    "service_account": os.path.join(exe_dir, 'service_account.json'),
    "api_key": os.path.join(exe_dir, 'put_api_key_here.txt'),
    "md_url": os.path.join(exe_dir, 'put_md_url_here.txt'),
    "voucher_amt": os.path.join(exe_dir, 'put_voucher_amt_here.txt'),
    "vcodlen": os.path.join(exe_dir, 'put_vcodlen_here.txt'),
    "voucher_log": os.path.join(exe_dir, 'voucher_logger.txt'),
    "expired_vouchers": os.path.join(exe_dir, 'expired_vouchers.txt'),
    "voucher_list": os.path.join(exe_dir, 'VoucherList.csv'),
    "macro_file": os.path.join(exe_dir, 'temp.macro'),
    "modified_macro": os.path.join(exe_dir, 'GConnect_-_GCash_-_Maya.macro'),
    "main_folder_name": os.path.join(exe_dir, 'main_folder_name.txt'),
    "main_folder_id": os.path.join(exe_dir, 'main_folder_id.txt'),
    "sub_folder_id": os.path.join(exe_dir, 'put_folder_id_here.txt'),
    "file_ids": os.path.join(exe_dir, 'put_file_ids_here.txt')
}

def check_file_exists(file_path, error_message=None):
    if not os.path.isfile(file_path):
        return error_message
    return None

def check_non_empty(file_path, error_message=None, additional_action=None, actions_to_take=None):    
    if not os.path.isfile(file_path):
        return None  # Return None if file is missing

    with open(file_path, "r") as file:
        content = file.read().strip()
        if not content:
            if additional_action and actions_to_take is not None:
                actions_to_take.append(additional_action)  # Queue the action
            return None  # Return None if file is empty
        return content  # Return the file content if non-empty

def open_in_notepad(file_path):
    subprocess.run(['notepad.exe', file_path], check=True)

def execute_actions(actions):
    for action in actions:
        try:
            action()
        except Exception as e:
            print(f"Error executing action: {e}")

