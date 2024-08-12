import math
from  UI. smallTool.service.dataService.base import DealDataBase
import numpy as np



class PlanA(DealDataBase):
    def __init__(self, file_path, batch_id):
        super().__init__(file_path, batch_id)
        
    def deal(self, index):
        if index == 0:
            self.df['pos_x'] = self.df['距离D（m)'] * np.cos((self.df['方位角AA（°）'] - 35) * math.pi / 180) * np.cos(self.df['俯仰角EA（°）'] * np.pi / 180) + 2
            self.df['pos_y'] = self.df['距离D（m)'] * np.sin((self.df['方位角AA（°）'] - 35) * math.pi / 180) * np.cos(self.df['俯仰角EA（°）'] * np.pi / 180) - 0.9
        elif index == 1:
            self.df['pos_x'] = self.df['距离D（m)'] * np.cos((self.df['方位角AA（°）'] + 35) * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) + 2
            self.df['pos_y'] = self.df['距离D（m)'] * np.sin((self.df['方位角AA（°）'] + 35) * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) + 0.9
        elif index == 2:
            self.df['pos_x'] = self.df['距离D（m)'] * np.cos((self.df['方位角AA（°）'] - 131) * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) - 2
            self.df['pos_y'] = self.df['距离D（m)'] * np.sin((self.df['方位角AA（°）'] - 131) * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) - 0.9
        elif index == 3:
            self.df['pos_x'] = self.df['距离D（m)'] * np.cos((self.df['方位角AA（°）'] + 132) * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) - 2
            self.df['pos_y'] = self.df['距离D（m)'] * np.sin((self.df['方位角AA（°）'] + 132) * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) + 0.9
        elif index == 4:
            self.df['pos_x'] = self.df['距离D（m)'] * np.cos(self.df['方位角AA（°）'] * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180) + 2
            self.df['pos_y'] = -(self.df['距离D（m)'] * np.sin(self.df['方位角AA（°）'] * math.pi / 180) * np.cos(
                self.df['俯仰角EA（°）'] * np.pi / 180))
    
    