import os

def read_file(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_file(file_path, data):
    with open(file_path, 'wb') as file:
        file.write(data)

def get_file_metadata(file_path):
    return os.stat(file_path)

def restore_file_metadata(original_metadata, file_path):
    os.utime(file_path, (original_metadata.st_atime, original_metadata.st_mtime))
    os.chmod(file_path, original_metadata.st_mode)
