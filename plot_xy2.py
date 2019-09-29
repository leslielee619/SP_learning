# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:09:03 2019

@author: leslielee

我用第一种方法画图
此程序实现了，动态图，但是只是一张张图片
"""

import matplotlib.pyplot as plt

file_url="D:\GUI_interface\generate_xy.txt"

update_num=1 #初始时，随便给其一个值(不为0)，使程序进入while循环
xy_list=[]

plt.ion() #打开交互形式
plt.figure(1)

while  update_num != 0:
    #每次循环需要将列表清空
    x_list=[] 
    y_list=[]
    last_length=len(xy_list) #前一次读取的数据长度
    
    with open(file_url) as file_obj:
        xy_list=file_obj.readlines()
        now_length=len(xy_list) #现在的数据长度
        update_num=now_length-last_length
    file_obj.close()
    
    for i in xy_list:
        i=i.strip('\n')
        i=eval(i)  #将[x,y]从字符串转化为列表
        x_list.append(i[0])
        y_list.append(i[1])
    
    plt.clf()    
    plt.plot(x_list,y_list,'b')
    plt.grid(True)    
    plt.pause(1)
    
    