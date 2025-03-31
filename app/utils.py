import os

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
    "sub_folder_name": os.path.join(exe_dir, 'put_folder_name_here.txt'),
    "sub_folder_id": os.path.join(exe_dir, 'put_folder_id_here.txt'),
    "file_ids": os.path.join(exe_dir, 'put_file_ids_here.txt'),
    "tokens": os.path.join(exe_dir, 'token.json'),
    "creds": os.path.join(exe_dir, 'creds.json')
}

def check_file_exists(file_path, error_message=None):
    if not os.path.isfile(file_path):
        return error_message
    return None


