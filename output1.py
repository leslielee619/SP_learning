# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 10:15:32 2019

@author: leslielee
采样时间与采样点数，其实其中有一个是固定的。如你只采10min的数据，那么采样点数随之得出。
反之，若你只采1000个点，采样时间是几min也可得出。
"""
from math import sin,cos,pi
import time
import os
import numpy as np

class output1:
    
    def __init__(self,DC,a,phi,f,base_f,file_url='D:\GUI_interface\generate_xy.txt'):
        '''
        a,phi,f 是一个一维矩阵，array类型
        file_url是输出文件的位置
        T是采样的时间
        '''
        self.DC=DC  #直流分量
        self.a=a
        self.phi=phi
        self.f=f
        self.file_url=file_url        
#先确定采样时间是几分钟        
        self.T=1/base_f   
        self.Fs=base_f*2.56    #设置Fs为基频的2.56倍    
        self.dT=1/self.Fs
        self.n=self.Fs     #每个周期生成的点数
        self.N=10*self.n   #十个周期的点
#-------------------------------------------------------------------------------
##先确定频率分辨率,但采样时间是几分钟也随之确定
#        self.Fs=(base_f*3)*2.56
#        self.N=self.Fs
#        self.dT=1/self.Fs
#        self.T=self.N*self.dT 
#        self.M=self.N/2.56
#------------------------------------------------------------------------------
        
    def generate_xy(self):
        num=1
        t=0
        if(os.path.exists(self.file_url)):
            os.remove(self.file_url)
        while num <= self.n :
            x=sum(self.a*np.sin(2*np.pi*self.f*t+self.phi))+self.DC  
            coordinates=str([round(t,4),round(x,4)])     #将列表转为字符串，便于存储在txt中
            #将x与t写入文件
            with open(self.file_url,'a+') as file_obj:
                file_obj.write(coordinates+'\n')
            file_obj.close()
            print('已生成{}个离散时域点'.format(num))
            
#            time.sleep(0.1)  #实现0.1秒读入一个数字
            t=t+self.dT
            num=num+1        
        
if __name__ == '__main__':
    DC=80
    a=np.array([100,500,60])
    phi=np.array([np.pi/6,np.pi/4,np.pi/6])
    f=np.array([10,200,500])
    base_f=500
    output1(DC,a,phi,f,base_f).generate_xy()
    