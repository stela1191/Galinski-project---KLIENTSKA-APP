import tkinter as tk
import datetime
import os
import math

w=590
h=145
root = tk.Tk()
can = tk.Canvas(root,width=w,height=h, bg='#beefff')
can.pack()
labelMenuImg=0

def karty_lock_create():
    subor = open('KARTY_LOCK.txt','w')
    subor.close()
def karty_lock_delete():
    os.remove('KARTY_LOCK.txt')


def ucty_lock_create():
    subor = open('UCTY_LOCK.txt','w')
    subor.close()
def ucty_lock_delete():
    os.remove('UCTY_LOCK.txt')


def klienti_lock_create():
    subor = open('KLIENTI_LOCK.txt','w')
    subor.close()
def klienti_lock_delete():
    os.remove('KLIENTI_LOCK.txt')


def trans_ucty_lock_create():
    subor = open('TRANSAKCIE_UCTY_LOCK.txt','w')
    subor.close()
def trans_ucty_lock_delete():
    os.remove('TRANSAKCIE_UCTY_LOCK.txt')


def trans_pay_lock_create():
    subor = open('TRANSAKCIE_PAYWALL_LOCK.txt','w')
    subor.close()
def trans_pay_lock_delete():
    os.remove('TRANSAKCIE_PAYWALL_LOCK.txt')


def zamestnanci_lock_create():
    subor = open('ZAMESTNANCI_LOCK.txt','w')
    subor.close()
def zamestnanci_lock_delete():
    os.remove('ZAMESTNANCI_LOCK.txt')

lock_karty_btn =tk.Button(root,text='KARTY LOCK'+'\n'+'CREATE',command=karty_lock_create, state='active')
lock_karty_btn.place(width=100,height=75,x=0,y=0)
lock_karty_d_btn =tk.Button(root,text='KARTY LOCK'+'\n'+'DELETE',command=karty_lock_delete, state='active')
lock_karty_d_btn.place(width=100,height=75,x=0,y=75)

lock_ucty_btn =tk.Button(root,text='UCTY LOCK'+'\n'+'CREATE',command=ucty_lock_create, state='active')
lock_ucty_btn.place(width=100,height=75,x=100,y=0)
lock_ucty_d_btn =tk.Button(root,text='UCTY LOCK'+'\n'+'DELETE',command=ucty_lock_delete, state='active')
lock_ucty_d_btn.place(width=100,height=75,x=100,y=75)

lock_klienti_btn =tk.Button(root,text='KLIENTI LOCK'+'\n'+'CREATE',command=klienti_lock_create, state='active')
lock_klienti_btn.place(width=100,height=75,x=200,y=0)
lock_klienti_d_btn =tk.Button(root,text='KLIENTI LOCK'+'\n'+'DELETE',command=klienti_lock_delete, state='active')
lock_klienti_d_btn.place(width=100,height=75,x=200,y=75)

lock_trans_ucty_btn =tk.Button(root,text='TRANS. UCTY'+'\n'+'LOCK'+'\n'+'CREATE',command=trans_ucty_lock_create, state='active')
lock_trans_ucty_btn.place(width=100,height=75,x=300,y=0)
lock_trans_ucty_d_btn =tk.Button(root,text='TRANS. UCTY'+'\n'+'LOCK'+'\n'+'DELETE',command=trans_ucty_lock_delete, state='active')
lock_trans_ucty_d_btn.place(width=100,height=75,x=300,y=75)

lock_trans_pay_btn =tk.Button(root,text='TRANS. PAYW'+'\n'+'LOCK'+'\n'+'CREATE',command=trans_pay_lock_create, state='active')
lock_trans_pay_btn.place(width=100,height=75,x=400,y=0)
lock_trans_pay_d_btn =tk.Button(root,text='TRANS. PAYW'+'\n'+'LOCK'+'\n'+'DELETE',command=trans_pay_lock_delete, state='active')
lock_trans_pay_d_btn.place(width=100,height=75,x=400,y=75)

lock_zamestnanci_btn =tk.Button(root,text='ZAMESTNANCI'+'\n'+'LOCK'+'\n'+'CREATE',command=zamestnanci_lock_create, state='active')
lock_zamestnanci_btn.place(width=100,height=75,x=500,y=0)
lock_zamestnanci_d_btn =tk.Button(root,text='ZAMESTNANCI'+'\n'+'LOCK'+'\n'+'DELETE',command=zamestnanci_lock_delete, state='active')
lock_zamestnanci_d_btn.place(width=100,height=75,x=500,y=75)

