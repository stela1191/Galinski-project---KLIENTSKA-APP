import tkinter as tk

h=720
w=1280

root = tk.Tk()
can = tk.Canvas(root,width=w,height=h)
can.pack()



def round_rectangle(x1, y1, x2, y2, radius=50, **kwargs):

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

    return can.create_polygon(points, **kwargs, smooth=True,fill='#c4ffef')

def frame2():
    global prihlasit_btn, ID_entry, ucty_list
    can.delete('all')
    prihlasit_btn.destroy()
    ID_entry.destroy()
    
    ucty_list = tk.Listbox(root, width=43, height = 8, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    ucty_list.insert(1, "BEZNY UCET, SK68 0651 0000 0000 0000 0000")
    ucty_list.insert(2, "FIREMNY UCET, SK68 0651 0000 0000 0000 0000")
    ucty_list.place(x=20,y=70)
    
    karty_list = tk.Listbox(root, width=43, height = 8, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    karty_list.insert(1, "KREDITNA KARTA, dlh = 120$")
    karty_list.insert(2, "DEBETNA KARTA")
    karty_list.place(x=(w//3)*2+20,y=70)
    
    transakcia_btn=tk.Button(root,text='TRANSAKCIA',command=frame2)
    transakcia_btn.place(width=200,height=25,x=w//6-100,y=430)
    
    platprik_btn=tk.Button(root,text='PLATOBNY PRIKAZ',command=frame2)
    platprik_btn.place(width=200,height=25,x=w//6-100,y=480)
    
    prijmy_btn=tk.Button(root,text='PRIJMY',command=frame2)
    prijmy_btn.place(width=200,height=25,x=w//6-100,y=530)
    
    potvrdplatbu_btn=tk.Button(root,text='potvrdit platbu',command=frame2)
    potvrdplatbu_btn.place(width=200,height=25,x=w//2-100,y=210)
    
    splatdlh_btn=tk.Button(root,text='splatit dlh',command=frame2)
    splatdlh_btn.place(width=200,height=25,x=(w//6)*5-100,y=240)
    
    prijemca_entry = tk.Entry(root)
    prijemca_entry.place(width=200,height=25,x=w//2-100,y=100)
    
    suma_entry = tk.Entry(root)
    suma_entry.place(width=200,height=25,x=w//2-100,y=170)
    
    can.create_text(w//2,80,text='Prijemca')
    can.create_text(w//2,150,text='Suma')
    can.create_text(w//6,40,text='ÚČTY',font='Arial 25')
    can.create_text(w//2,40,text='PLATOBNY PRIKAZ',font='Arial 25')
    can.create_text((w//6)*5,40,text='KARTY',font='Arial 25')
    can.create_text(w//6,300,text='zostatok na ucte: 1234$6',font='Arial 20')

##    round_rectangle(400, 200, w-400, h-200, radius=50)
##    round_rectangle(400, 200, w-400, h-200, radius=50)
##    round_rectangle(400, 200, w-400, h-200, radius=50)
    
def login():
    global prihlasit_btn, ID_entry
    prihlasit_btn=tk.Button(root,text='BUTONIK',command=frame2)
    prihlasit_btn.place(width=200,x=w//2-100,y=h//2+50)
    
    ID_entry=tk.Entry(root,width=200)
    ID_entry.place(width=60,x=w//2-30,y=h//2+20)
    
    round_rectangle(400, 200, w-400, h-200, radius=50)
    can.create_text(w//2,h//2-20,text='LOGIN',font='Arial 30')
login()

#bez frame, vandak style riesenie na widgety :D menej prace, menej errorov...
#
