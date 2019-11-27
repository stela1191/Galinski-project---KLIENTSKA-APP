import tkinter as tk

h=720
w=1280

root = tk.Tk()
can = tk.Canvas(root,width=w,height=h)
can.pack()



def round_rectangle(x1, y1, x2, y2, radius=50, color='black', **kwargs):

    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]

    return can.create_polygon(points, **kwargs, smooth=True,fill=color)

def frame2():
    global prihlasit_btn, ID_entry, ucty_list
    can.delete('all')
    prihlasit_btn.destroy()
    ID_entry.destroy()

    round_rectangle(100, 100, w-100, h-100, radius=50,color='#71CAE7', outline='black',width=3)
    
    can.create_text(w//2-255,150,text='ÚČTY',font='Arial 25')
    can.create_text(w//2-255,300,text='zostatok na ucte: 1234$6',font='Arial 20')
    
    ucty_list = tk.Listbox(root, width=43, height = 8, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    ucty_list.insert(1, "BEZNY UCET, SK68 0651 0000 0000 0000 0000")
    ucty_list.insert(2, "FIREMNY UCET, SK68 0651 0000 0000 0000 0000")
    ucty_list.place(x=w//2-450,y=200)
    
    transakcia_btn=tk.Button(root,text='TRANSAKCIA',command=frame2)
    transakcia_btn.place(width=200,height=25,x=w//2-355,y=410)
    
    platprik_btn=tk.Button(root,text='PLATOBNY PRIKAZ',command=platobny_prikaz_def)
    platprik_btn.place(width=200,height=25,x=w//2-355,y=450)
    
    prijmy_btn=tk.Button(root,text='PRIJMY',command=prijmy_def)
    prijmy_btn.place(width=200,height=25,x=w//2-355,y=490)

    karty_btn=tk.Button(root,text='KARTY',command=karty_def)
    karty_btn.place(width=200,height=25,x=w//2-355,y=530)
    

def platobny_prikaz_def():
    global platobny_prikaz_tf, karty_tf, prijmy_tf, potvrdplatbu_btn, prijemca_entry, suma_entry
    vymaz_pravu_stranu()

    can.create_text(w//2+255,150,text='PLATOBNY PRIKAZ',font='Arial 25')
    
    potvrdplatbu_btn=tk.Button(root,text='potvrdit platbu',command=frame2)
    potvrdplatbu_btn.place(width=200,height=25,x=w//2+155,y=340)
    
    prijemca_entry = tk.Entry(root)
    prijemca_entry.place(width=200,height=25,x=w//2+155,y=210)
    
    suma_entry = tk.Entry(root)
    suma_entry.place(width=200,height=25,x=w//2+155,y=280)
    
    can.create_text(w//2+255,190,text='Prijemca')
    can.create_text(w//2+255,260,text='Suma')
    
    karty_tf=False
    platobny_prikaz_tf=True
    prijmy_tf=False

def karty_def():
    global platobny_prikaz_tf, karty_tf, prijmy_tf, splatdlh_btn, karty_list
    vymaz_pravu_stranu()
    
    can.create_text(w//2+255,150,text='KARTY',font='Arial 25')

    splatdlh_btn=tk.Button(root,text='splatit dlh',command=frame2)
    splatdlh_btn.place(width=200,height=25,x=w//2+155,y=410)

    karty_list = tk.Listbox(root, width=43, height = 8, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    karty_list.insert(1, "KREDITNA KARTA, dlh = 120$")
    karty_list.insert(2, "DEBETNA KARTA")
    karty_list.place(x=w//2+65,y=200)
    
    karty_tf=True
    platobny_prikaz_tf=False
    prijmy_tf=False
    
def prijmy_def():
    global platobny_prikaz_tf, karty_tf, prijmy_tf, prijmy_list
    vymaz_pravu_stranu()
    
    can.create_text(w//2+255,150,text='PRIJMY',font='Arial 25')
    
    prijmy_list = tk.Listbox(root, width=43, height = 8, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    prijmy_list.insert(1, "420 / SK83 0000 0000 0000 0000 0000")
    prijmy_list.insert(2, "1420 / SK83 0000 0000 0000 0000 0001")
    prijmy_list.insert(3, "4,20 / SK83 0000 0000 0000 0000 0002")
    prijmy_list.insert(4, "300 / SK83 0000 0000 0000 0000 0001")
    prijmy_list.insert(5, "400 / SK83 0000 0000 0000 0000 0000")
    prijmy_list.insert(6, "480 / SK83 0000 0000 0000 0000 0044")
    prijmy_list.place(x=w//2+65,y=200)

    karty_tf=False
    platobny_prikaz_tf=False
    prijmy_tf=True

    
def login():
    global prihlasit_btn, ID_entry

    prihlasit_btn=tk.Button(root,text='potvrdit',command=frame2, cursor='right_ptr')
    prihlasit_btn.place(width=200,x=w//2-100,y=h//2+75)
    
    ID_entry=tk.Entry(root,width=10, font='Arial 15', cursor='right_ptr')
    ID_entry.place(width=200,x=w//2-100,y=h//2+40)
    
    round_rectangle(400, 200, w-400, h-200, radius=50,color='#71CAE7', outline='black',width=3)
    can.create_text(w//2,h//2+20,text='Zadajte vase ID',font='Arial 15')
    can.create_text(w//2, h//2-40, text='LOGIN',font='Arial 30')
    
def vymaz_pravu_stranu():
    global potvrdplatbu_btn, prijemca_entry, suma_entry, splatdlh_btn, karty_list, prijmy_list
    if platobny_prikaz_tf:                                                
        can.delete('all')
        frame2()
        potvrdplatbu_btn.destroy()
        prijemca_entry.destroy()
        suma_entry.destroy()
        
    elif karty_tf:
        can.delete('all')
        frame2()
        splatdlh_btn.destroy()
        karty_list.destroy()
        
    elif prijmy_tf:
        can.delete('all')
        frame2()
        prijmy_list.destroy()


# VYSVETLIVKY: tf = true/false, btn = BUTTON

karty_tf=False
platobny_prikaz_tf=False
prijmy_tf=False
login()
