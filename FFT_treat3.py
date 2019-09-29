# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 21:08:39 2019

@author: leslie
此程序实现从文本中读取时域数据，然后进行实时变换为幅值与相位
实现只要有值就送过来进行复数计算，但是每次送过来的为了运行更快只计算最新的
分析的实际信号是一个周期内的，则不需要加窗。否则需要加窗，加窗函数的T怎么选择？我现在时域信号有好多频率选择哪个作为T呢？
应该整周期读取文件
"""
from scipy.fftpack import fft
import numpy as np
import time

class FFT_treat1:
    
    def __init__(self,file_url,work_speed,error=5):
        '''
        工作转速单位为r/min
        误差默认为5
        '''
        self.file_url=file_url
        self.work_speed=work_speed
        self.error=error
        self.T=1/self.work_speed   
        self.Fs=self.work_speed*2.56        
        self.dT=1/self.Fs
        self.n=self.Fs      #一个周期生成的数据点
        
    
    def line_num(self):
        #该函数统计文件中的行数
        count=0
        for index, line in enumerate(open(self.file_url,'r')):
            count += 1
        return count    
        
    def read_txt(self):
        #当文本不够一个周期时，不读取，而且每次读取整数个周期
        
        count=self.line_num()
        while count/self.n < 1 : 
            print('请稍等，读取的数据点不够一个周期...',round(count/self.n,2))
            time.sleep(5)   #如进入此循环先睡三秒钟
            
        with open(self.file_url) as file_obj:
            xy_list=file_obj.readlines()
        file_obj.close()
        count=len(xy_list)
        num=int((count-count%self.n))  #现在文本中有n个周期
        
        xy_list=np.array(xy_list)        #列表转数组
        xy_list=xy_list[0:num].tolist()  #数组转列表
        return xy_list,num
    
    def complex_trans(self):
        #将文本读取进行FFT变换,并且返回基频对应的幅值与相位角
        y_list=list()
        possible_abs=list()
        xy_list,N=self.read_txt()
        xy_list=np.array(xy_list)
#        NFFT=self.nextpow2(N)
        for i in xy_list:
            i=i.strip('\n')
            i=eval(i)            #将[x,y]从字符串转化为列表
            y_list.append(i[1])
#----------------------------------------------------------------------------
        Ym=fft(y_list)     #将y进行FFT变为Ym
        Ym_abs=np.abs(Ym).tolist()
        print(Ym_abs[200])
        Ym_phase=(np.angle(Ym)*180/np.pi).tolist()
        base_f=self.work_speed   #基频
#----------------------------------------------------------------------------
#这一段实现寻找基频左右的最大幅值，及其对应的相位，所以找出的相位应该不准确
        if len(Ym)>base_f+self.error:
            possible_f=np.arange(base_f-self.error,self.error+base_f)  #设置基频左右10，来寻找幅值与相位
            for f in possible_f:
                possible_abs.append(Ym_abs[int(f)])
                unbala_abs=max(possible_abs)
            where=possible_abs.index(unbala_abs)
            where=where+base_f-self.error
            unbala_phase=Ym_phase[int(where)]
            print('当前基频的幅值与相位是',[unbala_abs/N*2,unbala_phase+90])   #相位多加90度
            unbala=[unbala_abs/N*2,unbala_phase+90]
            return unbala,N
        else:
            return [],N


    def return_update(self):
        #保持一直读取文本直到文本不再更新为止
        time.sleep(3)  #每次读取间隔一秒
        unbala1,N1=self.complex_trans()
        last_num=N1
        unbala2,N2=self.complex_trans()
        now_num=N2            
        update=now_num-last_num
        if unbala1 == []:
            unbala=unbala2
            return unbala,update
        elif unbala1[0] <= unbala2[0]:
            unbala = unbala2
            return unbala,update
        else:
            unbala = unbala1
            return unbala,update
    
    def nextpow2(self,N):
        power=[2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072]
        power1=list()
        for i in power:
            if i>N:
                power1.append(i)
        pow2=min(power1)
        return pow2
    

    def choose_windows(self,N,name):
        #自己构造一个窗函数
        if name == 'Hamming':
            window = np.array([0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1)) for n in range(N)])
        elif name == 'Hanning':
            window = np.array([0.5 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) for n in range(N)])
        elif name == 'Rect':
            window = np.ones(N)
        return window

        
if __name__ == '__main__':
    file_url='D:\GUI_interface\generate_xy.txt'
    work_speed=500         #r/s
    error=10
    update=1
    while update != 0 :
        print('请稍后正在读入数据......')
        unbala,update=FFT_treat1(file_url,work_speed,error).return_update()

    print('文本不再更新')
    if unbala != []:
        print('该转速下的振幅与相位为',unbala)
    else :
        print('数据点不够未计算出振幅与相位')