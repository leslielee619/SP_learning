# -*- coding:UTF-8  -*-
"""
Created on Sat Oct  5 15:17:19 2019

@author: leslie
"""
import tkinter as tk
from tkinter import Menu
from tkinter import messagebox as msg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from tkinter import ttk
from scipy.fftpack import fft
import numpy as np
import tkinter.filedialog as filedialog
#============================================================
#创建主面板，创建菜单
#============================================================
#创建主面板
main_panel=tk.Tk()
main_panel.withdraw()
main_panel.title('绘制幅频图')  #创建标题
icon_url='image/madonna.ico'   #加上icon
main_panel.iconbitmap(icon_url)
main_panel.geometry('600x400')
main_panel.resizable(0,0)

#给主面板上添加菜单栏
menu_bar=Menu(main_panel)
main_panel.config(menu=menu_bar)

#添加File与Help
file_menu=Menu(menu_bar,tearoff=0)
help_menu=Menu(menu_bar,tearoff=0)
menu_bar.add_cascade(label='文件',menu=file_menu)
menu_bar.add_cascade(label='帮助',menu=help_menu)


#_save与保存绑定
def _save(*args):
    pic_url = filedialog.asksaveasfilename(title='保存文件', 
                                           filetypes=[("PNG", ".png")])
    if pic_url != '':
        fig.savefig(pic_url+'.PNG')
    
# _quit与×，退出,以及退出的快捷键关联。该函数可传入任意个参数
#因为bind_all会返回一个event，所以目前只好这样改
def _quit(*args):
    var=msg.askyesno('','你真的要退出吗？')
    if var == True :
        main_panel.quit()
        main_panel.destroy()      
        
#给File添加Save与Quit,并且给Quit添加快捷键
file_menu.add_command(label='保存',command=_save,accelerator='Ctrl+S')
file_menu.add_separator()
file_menu.add_command(label='退出',command=_quit,accelerator='Ctrl+E')
file_menu.bind_all('<Control-e>',_quit)  
file_menu.bind_all('<Control-s>',_save)  

#将叉与_quit函数绑定
main_panel.protocol('WM_DELETE_WINDOW',_quit)

#_about与 关于 绑定
def _about():
    msg.showinfo('','这是由leslie lee用Tkinter创建的GUI。\n创建时间：2019-10-05')

#_help与 如何使用 绑定
def _help():
    help_panel=tk.Tk()
    help_panel.geometry('300x200')
    help_panel.iconbitmap(icon_url)
    help_panel.title('如何使用')
    help_text=tk.Text(help_panel)
    help_text.pack()
    text1='用户需输入的复合简谐函数,然后点击显示会显示其波形图及幅频图.\n'
    text2='输入的顺序为DC(直流部分),A,f,phi.然后会得到一个复合函数:\n'
    text3='DC+A*sin(2*pi*f+phi).\n'
    text4='四个参数都是列向量且元素个数相同,输入方式为[[],[],[],[]].\n'
    text5='点击保存,可以将屏幕截屏保存.\n'
    text6='如输入[[10,20],[5,10],[100,20],[np.pi/2,np.pi/3]]\n' 
    text7='np.pi表示圆周率3.1415...'
    text=text1+text2+text3+text4+text5+text6+text7
    help_text.insert('insert',text)
    help_text.config(state='disabled')
    
#给Help添加About
help_menu.add_command(label='关于',command=_about)
help_menu.add_command(label='如何使用',command=_help)

#====================================================================
#在面板里添加控件.  
#entery 输入[DC,A,f,phi] DC+A*sin(2*pi*f+phi)
#只需添加三个label，一个按钮，一个entry，两个canvas
#====================================================================
#用2个labelframe瓜分容器,一个放entry，一个放画布
frame1=ttk.LabelFrame(main_panel,text='原始波形与幅频图')
frame1.place(width=600,height=300)
frame2=ttk.LabelFrame(main_panel,text='输入参数')
frame2.place(x=0,y=310,width=400,height=60)

#初始化fig
#fig = Figure(figsize=(12,8), facecolor='white') 
fig=plt.figure(1)
plot1=fig.add_subplot(121)
plot2=fig.add_subplot(122)
canvas = FigureCanvasTkAgg(fig, master=frame1)
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

#entry
para=tk.StringVar()
para_entered=ttk.Entry(frame2,width=55,textvariable=para)
para_entered.grid(sticky='W')

def _fft():
    #[[10,20],[5,10],[100,20],[np.pi/2,np.pi/3]]
    paras=para.get()
    print(paras)
    if '[' in paras:
        paras=eval(paras)
        if len(paras) == 4 and type(paras)==list :
            DC=np.array(paras[0])
            A=np.array(paras[1])
            f=np.array(paras[2])
            phi=np.array(paras[3])
            Fs=max(f)*2.56
            L=round(Fs)
            t=np.linspace(0,1,int(L))       
            y=list()
            for i in t:
                y.append(sum(A*np.sin(2*np.pi*f*i+phi))+sum(DC))
            ym=fft(y)
            ym_abs=np.abs(ym)
            
            #作图
            plot1.clear()
            plot2.clear()
            plot1.plot(t,y)
            x=np.arange(L)
            x1=x[range(int(L/2))]
            ym_abs1=ym_abs[range(int(L/2))]/L
            plot2.plot(x1,ym_abs1)
            fig.canvas.draw()


  
#button
action=ttk.Button(main_panel,text='显示! ',command=_fft)
action.place(x=500,y=330)
#--------------------------------------------------------------------
main_panel.update()
main_panel.deiconify()
main_panel.mainloop()
