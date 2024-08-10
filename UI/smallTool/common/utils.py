import os
from ..common.config import cfg

class FileInfo:
    def __init__(self, name, path=None):
        self.full_path = path
        self.file_name = name
        self.file_suffix = os.path.splitext(self.file_name)[1]
def get_file_from_folders(directorys, suffixes=None):
    files_with_suffix = []
    for directory in directorys:
        files_with_suffix += get_file_from_folder(directory, suffixes)

    return files_with_suffix

def get_file_from_folder(directory, suffixes=None):
    if suffixes is None and  cfg.get(cfg.file_suffix):
        suffixes = cfg.file_suffix

    # 获取指定目录下所有文件和目录的列表
    file_list = os.listdir(directory)
            
    # 过滤出所有以指定后缀结尾的文件名
    files_with_suffix = [FileInfo(file, directory + "/" + file) for file in file_list if any(file.endswith(suffix) for suffix in suffixes)]
    
    return files_with_suffix


class Utils:
    def __init__(self):
        
        pass
    
    class FolderUtils:
        pass