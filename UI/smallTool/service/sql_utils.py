import dataset
import logging

log = logging.getLogger(__name__)
class SQLUtils:
    def __init__(self, db_path): 
        self.db_path = db_path
        # 连接到数据库（这里使用 SQLite）
        self.db = dataset.connect(f"sqlite:///{db_path}\data.db")
        log.debug(f"连接到数据库 : {db_path}\data.db")

    def save_to_file(self, table_name, dataframe, override=False):
        if not self.db.has_table(table_name):
            self.db.create_table(table_name)
            log.debug(f"表{table_name}不存在,已经自动创建")
        table = self.db.load_table(table_name)
        if override:
            table.delete(file = dataframe['file'][0])
            table.insert_many(dataframe.to_dict(orient='records'))
            log.debug(f"数据保存完毕")
        else:
            table.insert_many(dataframe.to_dict(orient='records'))
            log.debug(f"数据保存完毕")
    
        # 提交事务并关闭数据库连接
        self.db.commit()
        log.debug(f"保存事务已提交")
        self.db.close()
        log.debug(f"数据库链接已断开")
        
        
        
