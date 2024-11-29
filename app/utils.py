import os
import subprocess

# Get the script directory for relative file references
exe_dir = os.path.dirname(os.path.abspath(__file__))
python_exe = os.path.join(exe_dir, "python", "python311", "python.exe")

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

def check_non_empty(file_path, error_message=None, additional_action=None):
    if not os.path.isfile(file_path):
        return None

    with open(file_path, "r") as file:
        content = file.read().strip()
        if not content:
            if additional_action:
                additional_action()
            return error_message
        return content

def execute_actions(actions):
    for action in actions:
        try:
            action()
        except Exception as e:
            print(f"Error executing action: {e}")

def open_in_notepad(file_path):
    subprocess.run(['notepad.exe', file_path], check=True)


# def get_path(filename):
#     """Helper to get absolute paths based on app_dir."""
#     return os.path.join(exe_dir, filename)

# # Directory or File check
# def check_dirfile_exists(file_path, error_message=None):
#     if not os.path.exists(file_path):
#         if error_message:
#             print(error_message)
#         return False
#     return True