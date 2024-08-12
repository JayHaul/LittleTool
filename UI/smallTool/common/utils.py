import asyncio
import os

from PyQt6.QtCore import QThread,pyqtSignal

from UI.smallTool.common.config import cfg

import logging

log = logging.getLogger(__name__)
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

class AsyncWorker(QThread):

    def __init__(self, loop=None):
        super().__init__()
        if loop is None:
            self.loop = asyncio.new_event_loop()
        else:
            self.loop = loop
        self.future = None

    def run(self):
        asyncio.set_event_loop(self.loop)
        log.debug("开始执行")
        if self.future:
            try:
                self.loop.run_until_complete(self.future)
                log.debug("执行完成")
            except Exception as e:
                log.exception("执行过程中发生异常：")
            finally:
                pass
                # self.finished.emit()
        else:
            log.warning("没有 future 可执行")
        

    def execute_async(self, coro):
        if not self.isRunning():
            self.future = asyncio.wrap_future(asyncio.run_coroutine_threadsafe(coro, self.loop))
            self.start()
        else:
            print("Thread is already running.")

class Utils:
    def __init__(self):
        
        pass
    
    class FolderUtils:
        pass