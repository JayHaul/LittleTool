import dataset 
 
class SQLUtils:
    def __init__(self, db_path): 
        self.db_path = db_path
        # 连接到数据库（这里使用 SQLite）
        self.db = dataset.connect(r"sqlite:///E:\workspace\Python\Desktop\UI\smallTool\app\data\data.db")
    
    def save_to_file(self, table_name, df):
        table = self.db[table_name]
        table.insert_many(df.to_dict(orient='records'))
        # 提交事务并关闭数据库连接
        self.db.commit()
        
    def close_db(self):
        self.db.close() 