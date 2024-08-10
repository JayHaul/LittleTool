import math
from  UI. smallTool.service.dataService.base import DealDataBase
import numpy as np



class Zero(DealDataBase):
    def __init__(self, file_path, batch_id):
        super().__init__(file_path, batch_id)
        
    def deal(self):
        self.df['pos_x'] = self.df['距离D（m)'] * np.cos((self.df['方位角AA（°）'] - 35) * math.pi / 180) * np.cos(self.df['俯仰角EA（°）'] * np.pi / 180) + 2
        self.df['pos_y'] = self.df['距离D（m)'] * np.sin((self.df['方位角AA（°）'] - 35) * math.pi / 180) * np.cos(self.df['俯仰角EA（°）'] * np.pi / 180) - 0.9
      

    
        


if __name__ == '__main__':
    a = Zero(r"E:\workspace\Python\Desktop\0_points.csv", 1)
    a.execute() 
    
    
    