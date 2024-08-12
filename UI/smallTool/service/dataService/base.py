import math
import os
import numpy as np
import pandas as pd

from UI. smallTool.service.sql_utils import SQLUtils

cycle = 60


def judge_frame(Utc_time):
    return math.ceil( Utc_time / cycle )



class DealDataBase:
    def __init__ (self, file_path, batch_id):
        self._file_path = file_path
        self.file_name = '.'.join(os.path.basename(self._file_path).split('.')[:-1])
        self.batch_id = batch_id
        self.radar = pd.read_csv(file_path, encoding='gb18030')
        self.df = None 
        self.db = SQLUtils(r"E:\workspace\Python\Desktop\UI\smallTool\app\data")
        

    # 只获取需要用到的列
    def get_data(self):
        return self.radar[['Utc_msec', '距离D（m)', '方位角AA（°）', '俯仰角EA（°）']]

    
    # 根据周期数给每行数据增加帧数和文件名这俩列
    def add_extr(self):
        self.df = self.get_data()
        df_c = self.df.copy()
        df_c.loc[:, 'frame'] = np.ceil( self.df['Utc_msec'] / cycle )
        df_c.loc[:, 'file'] = self.file_name
        # 添加行号作为ID列
        df_c = df_c.reset_index().rename(columns={'index': 'ID'})
        self.df = df_c
        
    # 编写子类来重写该方法,这是用来处理数据的
    def deal(self, index):
        pass 
    
    # 这是整个处理流程
    # 比如处理类 Zero:
    # Zero(数据文件路径).execute()就可以了
    async def execute(self, index):
        self.add_extr()
        self.deal(index)
        await self.save_to_sqlLite(self.df)


    async def save_to_sqlLite(self, df):
        self.db.save_to_file(f'table_{self.batch_id}', df, True)


   