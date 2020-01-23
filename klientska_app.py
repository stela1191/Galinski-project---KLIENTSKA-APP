import tkinter as tk
import datetime
import os
import math


h=720
w=1280

# DOROBIT : - vytvorenie LOCKU ked s tym pracujem, vymazanie locku, close subor
#           - GRAF este nejde stopercentne kvoli tej premene sinusu na stupne, nevymaz tu dolnu podmienku, ak by si videl, ked budes mat cas mozes pozriet chybu//Christi
#           - Jednotne tlacidla
#           - Platobny prikaz este nekomunikuje so suborom tam ten zapis musime domysliet
#           - Skus vysvietit ten ucet spolu - neviem jak to spravit... grafiku riesme ked tak nakoniec 
#             Ono to nejde kvoli tomu ze je tam v tom idx len jedna pozicia ale ak ju zmeni tak to nejde takze neviem ako to vysvietime lebo aj ked tam dam to '\n' tak to nejde
# HOTOVE :  - Obrazok po prihlaseni 
#           - Splatenie dlhu na karte
#           - Nove okienko nejde otvorit ked je otvorene 
# OTAZKY :  - Nechceme zobrazovat tie prijmy uz hned pri nacitani frame2
#           - A ci chceme pri prijmoch zobrazovat aj kladne transakcie z kariet


root = tk.Tk()
can = tk.Canvas(root,width=w,height=h, bg='#beefff')
can.pack()
labelMenuImg=0


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
    global frame_3, login_tf, prihlasit_btn, ID_entry, pocet_uctov,ucty_list,karty_btn,transakcia_btn,menuImg,labelMenuImg,platprik_btn,potvrdplatbu_btn,prijmy_btn,splatdlh_btn,prijemca_entry,suma_entry,can, odhlasenie_btn, z_loginu, frame_2,id_uctov_frame2

    frame_2=True
    
    frame_3=False
    login_tf=False
    kon_ucty()

    if not lock_ucty:
        citaj_ucty()
        
    round_rectangle(100, 100, w-100, h-100, radius=50,color='#71CAE7', outline='black',width=3)
    
    can.create_text(w//2-255,150,text='ÚČTY',font='Arial 25')
    can.create_text(w//2-255,300,text='zostatok na ucte: 1234$6',font='Arial 20')
   
    ucty_list = tk.Listbox(root, width=43, height = 8, font='Arial 11', xscrollcommand=True)
  
    poradie = 0
    id_uctov_frame2 = []
    
    if not lock_ucty:
        for l in range((pocet_uctov)-1):#poradie uctov pridat
            if prihlaseny_ID == id_klienta_ucty[l]:
                poradie+=1
                if typ_uctu[l] == 'P':
                    typ_u = 'SÚKROMNÝ ÚČET '
                else:
                    typ_u = 'OBCHODNÝ ÚČET '
                ucty_list.insert(poradie*2, typ_u+ ' '*(40- len(stav_uctu[l])) + str(stav_uctu[l])+' €')
                ucty_list.insert(poradie*2, str(cislo_uctu[l]) )
                id_uctov_frame2.append(id_uctu[l])
       
    ucty_list.bind('<<ListboxSelect>>',vyber_ucet_def)
    ucty_list.place(x=w//2-425,y=200)

    if vybraty_ucet == '':
        transakcia_btn=tk.Button(root,text='TRANSAKCIA',command=frame3, state='disabled')
        transakcia_btn.place(width=200,height=35,x=w//2-355,y=375)
        
        platprik_btn=tk.Button(root,text='PLATOBNY PRIKAZ',command=platobny_prikaz_def, state='disabled')
        platprik_btn.place(width=200,height=35,x=w//2-355,y=420)
        
        prijmy_btn=tk.Button(root,text='PRIJMY',command=prijmy_def, state='disabled')
        prijmy_btn.place(width=200,height=35,x=w//2-355,y=465)
        
        karty_btn=tk.Button(root,text='KARTY',command=karty_def, state='disabled')
        karty_btn.place(width=200,height=35,x=w//2-355,y=510)
        
        menuImg = tk.PhotoImage(master=can,file='obrazky/menu.png')
        if not bol_lock_ucty:
            labelMenuImg = tk.Label(image = menuImg,borderwidth=0)
            labelMenuImgimage = menuImg
            labelMenuImg.pack()
            labelMenuImg.place(x=0.45*w,y=h-(0.50*h), anchor="w")
    else:
        labelMenuImg.destroy()
        transakcia_btn=tk.Button(root,text='TRANSAKCIA',command=frame3, state='active')
        transakcia_btn.place(width=200,height=35,x=w//2-355,y=375)
        
        platprik_btn=tk.Button(root,text='PLATOBNY PRIKAZ',command=platobny_prikaz_def, state='active')
        platprik_btn.place(width=200,height=35,x=w//2-355,y=420)
        
        prijmy_btn=tk.Button(root,text='PRIJMY',command=prijmy_def, state='active')
        prijmy_btn.place(width=200,height=35,x=w//2-355,y=465)
        
        karty_btn=tk.Button(root,text='KARTY',command=karty_def, state='active')
        karty_btn.place(width=200,height=35,x=w//2-355,y=510)
        
    if z_loginu:
        odhlasenie_btn=tk.Button(root,text='ODHLÁSIŤ SA',command=odhlas)
        odhlasenie_btn.place(width=100,height=25,x=w-200,y=20)
    z_loginu=False

##    prijmy_def()     TOTO NEJDE NECHAPEM PRECO... ked to pustim tak sa zacykluje shell
    if not bol_lock_ucty:
        ucty_lock_frame2()

def ucty_lock_frame2():
    global bol_lock_ucty, vybraty_ucet
    kon_ucty()
    if lock_ucty:
        vybraty_ucet == ''
        if frame_3:
            spat_def()
        print('nasiel som', lock_ucty, bol_lock_ucty)
        if frame_2:
            if not bol_lock_ucty:
                bol_lock_ucty = True
                vymaz_lavu_stranu()
                vymaz_pravu_stranu()
                frame2()
        bol_lock_ucty = True
    elif not lock_ucty:
        if bol_lock_ucty:
            bol_lock_ucty = False
            frame2()  
        bol_lock_ucty = False
    if not login_tf:
        print('kontrolujem')
        can.after(2000, ucty_lock_frame2)
    
def potvrd_ucet_def():
    global transakcia_btn, platprik_btn, prijmy_btn, karty_btn, vyber_ucet_btn
    if vybraty_ucet != '':
        transakcia_btn.destroy()
        transakcia_btn=tk.Button(root,text='TRANSAKCIA',command=frame3, state='active')
        transakcia_btn.place(width=200,height=35,x=w//2-355,y=375)
        
        platprik_btn.destroy()
        platprik_btn=tk.Button(root,text='PLATOBNY PRIKAZ',command=platobny_prikaz_def, state='active')
        platprik_btn.place(width=200,height=35,x=w//2-355,y=420)
        
        prijmy_btn.destroy()
        prijmy_btn=tk.Button(root,text='PRIJMY',command=prijmy_def, state='active')
        prijmy_btn.place(width=200,height=35,x=w//2-355,y=465)
        
        karty_btn.destroy()
        karty_btn=tk.Button(root,text='KARTY',command=karty_def, state='active')
        karty_btn.place(width=200,height=35,x=w//2-355,y=510)

        
def vyber_ucet_def(event):
    global vybraty_ucet, stav_vybrateho_uctu
    m = event.widget
    idx = int(m.curselection()[0])
    if idx < 2:
        idx=0
    else:
        if idx%2 == 1:
            idx = (idx-1)//2
        else:
            idx = idx//2
    vybraty_ucet=id_uctov_frame2[idx]
    potvrd_ucet_def()
    print(vybraty_ucet)
    stav_vybrateho_uctu=stav_uctu[int(vybraty_ucet)-1]

def frame3():
    global frame_3, scrollbar, trans_list, spat_btn, otvor_okienko,bol_f3, frame_2, id_uctu,vybraty_ucet,okno,id_uctu_transakcie,prihlaseny_ID, id_klienta_transakcie,pocet_transakcii,komu,cislo_uctu,krstne_meno,priezvisko,a,sucet_kladnych,sucet_zapornych,celkova_suma

    vymaz_pravu_stranu()
    
    frame_2 = False
    frame_3 = True
    
    bol_f3 = True
    
    vymaz_pravu_stranu()
    vymaz_lavu_stranu()

    kon_transakcie_ucty() #mensie zmeny v poradi kvoli LOCKU (najprv to skontroluje ci to moze pokracovat, ci nikde nie je lock)
    kon_ucty()
    kon_klienti()
    
    citaj_transakcie_ucty()
    citaj_ucty()
    citaj_klientov()
    
    round_rectangle(50, 50, w-50, h-50, radius=50,color='#71CAE7', outline='black',width=3)
    
    can.create_text(w//2,75,text='Transakcie', font= 'Arial 25')
    cislo=0
    a=[]
    sucet_kladnych=0
    sucet_zapornych=0
    celkova_suma=0
    scrollbar = tk.Scrollbar(root)
    scrollbar.place(x=w-120,y=100, height=h-200, width=20)
    trans_list = tk.Listbox(root, font='Arial 15')
    trans_list.place(x=100,y=100,width=w-220,height=h-200)
    for i in range(pocet_transakcii):
        if komu[i]==prihlaseny_ID or id_klienta_transakcie[i]==prihlaseny_ID and vybraty_ucet==id_uctu_transakcie[i]:
            a=int(id_klienta_transakcie[i])
            trans_list.insert(cislo, cislo_uctu[a]+(150-len(suma))*' '+suma[i]+' €')
            trans_list.insert(cislo+1, krstne_meno[a]+' '+priezvisko[a])
            trans_list.insert(cislo+2, '')
            celkova_suma+=int(suma[i])
            #print(celkova_suma)
            if (suma[i][0])=='-':
                sucet_zapornych+=int(suma[i])
                trans_list.itemconfig(cislo,{'fg': 'red'})
                trans_list.itemconfig(cislo+1,{'fg': 'red'})
            if (suma[i][0])=='+':
                sucet_kladnych+=int(suma[i])
                trans_list.itemconfig(cislo,{'fg': 'green'})
                trans_list.itemconfig(cislo+1,{'fg': 'green'})
            cislo+=3
            print(celkova_suma)
    trans_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=trans_list.yview)
        
    spat_btn = tk.Button(root,text='SPÄŤ',command=spat_def)
    spat_btn.place(width=200,height=25,x=100,y=60)
    okno=False
    if okno==False:
        otvor_okienko = tk.Button(root,text='ZOBRAZ GRAF',command=okienko,state='active')
        otvor_okienko.place(width=200,height=40,x=w-300,y=h-95)



def okienko():
    global sucet_kladnych,sucet_zapornych,celkova_suma,plusova,minusova,zaporne,kladne,okno
    okno=True
    newroot=tk.Tk()
    newroot.geometry('410x410')
    myCanvas = tk.Canvas(newroot, bg="white", height=400, width=400)
    coord = 10, 10, 390, 390
    arc = myCanvas.create_arc(coord, start=0, extent=(math.asin(celkova_suma//sucet_zapornych)), fill="red")
    arv2 = myCanvas.create_arc(coord, start=180, extent=(math.asin(celkova_suma//sucet_kladnych)), fill="green")
    if (sucet_zapornych*100)!=0 or celkova_suma!=0:
        minusova=(sucet_zapornych*100)/celkova_suma
        print('Minusova:'+str(minusova))
        zaporne=(360/100)*(-(int(minusova)))
        sinus1=math.sin(celkova_suma-zaporne)
        print(sinus1)
        sinus_stupne_z=math.degrees(sinus1)*(math.pi)
        print(sinus_stupne_z)
        arc = myCanvas.create_arc(coord, start=0, extent=360-(sinus_stupne_z), fill="red")
    if (sucet_kladnych)!=0 or celkova_suma!=0:
        plusova=(sucet_kladnych*100)//celkova_suma
        print('Plusova:'+str(plusova))
        kladne=(360/100)*(-(int(plusova)))
        sinus2=math.sin(celkova_suma-kladne)
        print(sinus2)
        sinus_stupne_k=math.degrees(sinus2)*(math.pi)
        print(sinus_stupne_k)
        arv2 = myCanvas.create_arc(coord, start=360-(sinus_stupne_z), extent=-sinus_stupne_k, fill="green")
        
    if (sucet_zapornych*100)==0:
        arc = myCanvas.create_arc(coord, start=0, extent=215, fill="green",outline='green')
        arc = myCanvas.create_arc(coord, start=100, extent=260, fill="green",outline='green')
    elif (sucet_kladnych*100)==0:
        arc = myCanvas.create_arc(coord, start=0, extent=215, fill="red",outline='red')
        arc = myCanvas.create_arc(coord, start=100, extent=260, fill="red",outline='red')
    otvor_okienko = tk.Button(root,text='ZOBRAZ GRAF',command=okienko,state='disabled')
    otvor_okienko.place(width=200,height=40,x=w-150,y=h-30)

    
    
    myCanvas.pack()
    root.mainloop()


def platobny_prikaz_def():
    global platobny_prikaz_tf, karty_tf, prijmy_tf, potvrdplatbu_btn, prijemca_entry, suma_entry, cislo_uctu,pocet_uctov, pocet_transakcii,stav_vybrateho_uctu, typy_karty,prihlaseny_ID,uctovnyDen
    vymaz_pravu_stranu()
    labelMenuImg.destroy()

    kon_ucty()
    citaj_ucty()

    can.create_text(w//2+255,150,text='PLATOBNY PRIKAZ',font='Arial 25')
    
    potvrdplatbu_btn=tk.Button(root,text='potvrdit platbu',command=frame2)
    potvrdplatbu_btn.place(width=200,height=25,x=w//2+155,y=340)
    
    prijemca_entry = tk.Entry(root)
    prijemca_entry.place(width=200,height=25,x=w//2+155,y=210)
    
    suma_entry = tk.Entry(root)
    suma_entry.place(width=200,height=25,x=w//2+155,y=280)
    
    can.create_text(w//2+255,190,text='Prijemca')
    can.create_text(w//2+255,260,text='Suma')
    subor_transakcie=open('TRANSAKCIE_UCTY.txt','r')
    subor_transakcie_NEW=open('TRANSAKCIE_UCTY_NEW.txt','w')

##    if str(stav_vybrateho_uctu)>=str(suma_entry.get()):
##        while riadok!='':
##            riadok = subor_transakcie.readline().strip()
##            riadok_NEW = riadok.split(';')
##            subor_transakcie_NEW.write(riadok+'\n')
##            for i in range():
##                subor_transakcie_NEW.write()+i)+(uctovnyDen))
##            
    subor_transakcie.close()
    subor_transakcie_NEW.close()
    karty_tf=False
    platobny_prikaz_tf=True
    prijmy_tf=False


def splatit():
    global splatene,suma2_entry,karty_list,kreditka,splatenie,dlh_vybratej_karty,stav_vybrateho_uctu
    subor = open('KARTY.txt','r')
    splatene=suma2_entry.get()
    print('stav uctu=' + stav_vybrateho_uctu)
    print('zadane=' + splatene)
    pocet_kariet = subor.readline().strip()
    if float(stav_vybrateho_uctu) >= float(splatene) and float(splatene) <= float(dlh_vybratej_karty):
        for a in range(int(pocet_kariet)):
            riadok_ = subor.readline().strip()
            riadok=riadok_.split(';')
            if riadok[0] == vybrata_karta:
                print('splatene')
        subor.close()
        subor_ = open('KARTY_.txt','w')
        subor = open('KARTY.txt','r+')
        for a in range(int(pocet_kariet)+1):
            riadok = subor.readline().strip()
            subor_.write(riadok+'\n')   
        subor.close()
        subor_.close()
        
        subor_ = open('KARTY_.txt','r')
        subor = open('KARTY.txt','w')
        for a in range(int(pocet_kariet)+1):
            riadok = subor_.readline().strip()
            if a == 0:
                subor.write(riadok+'\n')
            riadok_split=riadok.split(';')
            if a > 0:
                if riadok_split[0] == vybrata_karta:
                    r_ = riadok.split(';')
                    dlh = str(float(dlh_vybratej_karty) - float(splatene))
                    dlh_vybratej_karty = dlh
                    r_[7]=dlh
                    print(dlh)
                    riadok = ';'.join(r_)
                    subor.write(riadok+'\n')
                else:
                    subor.write(riadok+'\n')
        subor.close()
        subor_.close()
        
        subor = open('UCTY.txt','r')
        subor_ = open('UCTY_.txt','w')
        riadok = subor.readline().strip()
        subor_.write(riadok+'\n')
        print('PU:'+str(riadok))
        pocet = int(riadok) 
        for a in range(pocet):
            riadokk = subor.readline().strip()
            subor_.write(riadokk+'\n')
        subor.close()
        subor_.close()

        suboris = open('UCTY.txt','w')
        suboris_ = open('UCTY_.txt','r')

        for a in range(pocet_uctov+1):
            riadocek = suboris_.readline().strip()     
            if a == 0:
                suboris.write(riadok+'\n')
            
            if a > 0:
                riadocek_split = riadocek.split(';')
                if vybraty_ucet == riadocek_split[0]:
                    r_=riadocek.split(';')
                    r_[4] = str(float(stav_vybrateho_uctu) - float(splatene))
                    stav_vybrateho_uctu = r_[4]
                    print('nasiel sa ucet', 'stav noveho: ' + r_[4])
                    riadok = ';'.join(r_)
                    suboris.write(riadok+'\n')
                else:
                    suboris.write(riadocek+'\n')
        suboris.close()
        suboris_.close()

        os.remove("UCTY_.txt")
        os.remove("KARTY_.txt")
        
        frame2()
        karty_def()
    else:
        print('nesplatene')
    
    subor.close()
    splatka=True
    
def karty_def():
    global id_kariet_box, dlh_kariet_box, platobny_prikaz_tf,karty_tf, prijmy_tf, kreditka, splatka,splatdlh_btn, karty_list, id_uctu_karty,dlh_karty, splatene,suma2_entry,dlh,prihlasit_btn, ID_entry, ucty_list,karty_btn,transakcia_btn,platprik_btn,potvrdplatbu_btn,prijmy_btn,splatdlh_btn,prijemca_entry,suma_entry
    vymaz_pravu_stranu()

    id_kariet_box = []
    dlh_kariet_box = []
    kon_karty()
    citaj_karty()

    karty_list = tk.Listbox(root, width=43, height = 8, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    splatka=False
    poradie = 0
    for m in range(len(id_uctu_karty)):
        if vybraty_ucet == id_uctu_karty[m]:
            poradie+=1
            if typy_karty[m] == 'D':
                typ_k = 'DEBETNÁ KARTA '
                karty_list.insert(poradie, typ_k)
            else:
                typ_k = 'KREDITNÁ KARTA, '
                if splatka==False:
                    splatenie=karty_list.insert(poradie, typ_k + 'dlh na karte: ' + str(dlh_karty[m]))
                else:
                    splatenie=karty_list.insert(poradie, typ_k + 'dlh na karte: ' + str((dlh_karty[m])-splatene))
            id_kariet_box.append(id_karty[m])
            dlh_kariet_box.append(dlh_karty[m])
            
    karty_list.place(x=w//2+65,y=200)
    karty_list.bind('<<ListboxSelect>>',vyber_karty_def)
    
    can.create_text(w//2+255,150,text='KARTY',font='Arial 25')

    suma2_entry = tk.Entry(root)
    suma2_entry.place(width=200,height=25,x=w//2+155,y=h-300)

    can.create_text(w//2+255, h-330, text='Zadajte sumu', font='Arial 15')

    splatdlh_btn=tk.Button(root,text='SPLATIT DLH',command=splatit)
    splatdlh_btn.place(width=200,height=25,x=w//2+155,y=h-250)

    karty_tf=True
    platobny_prikaz_tf=False
    prijmy_tf=False

    print(id_kariet_box)
    print(dlh_kariet_box)
    
def vyber_karty_def(event):
    global vybrata_karta, dlh_vybratej_karty
    m = event.widget
    idx = int(m.curselection()[0])
    vybrata_karta=id_kariet_box[idx]
    dlh_vybratej_karty =dlh_kariet_box[idx]
    print(idx, vybrata_karta, dlh_vybratej_karty)
    
def prijmy_def():
    global platobny_prikaz_tf, karty_tf,prijmy, prijmy_tf, prijmy_list,prihlasit_btn, suma,ID_entry,pocet_transakcii,krstne_meno,priezvisko,cislo_uctu, ucty_list,karty_btn,transakcia_btn,platprik_btn,potvrdplatbu_btn,prijmy_btn,splatdlh_btn,prijemca_entry,suma_entry,can

    vymaz_pravu_stranu()

    kon_transakcie_ucty()
    citaj_transakcie_ucty()
    
    kon_ucty()
    citaj_ucty()
    
    kon_klienti()
    citaj_klientov()
    pocet=18
    
    prijmy=can.create_text(w//2+255,150,text='PRIJMY',font='Arial 25')
    prijmy_list = tk.Listbox(root, width=43, height = pocet, font='Arial 13',selectmode='SINGLE', xscrollcommand=True)
    
    for i in range(pocet_transakcii):
        a=int(id_klienta_transakcie[i])
        if  prihlaseny_ID==komu[i] and suma[i][0]=='+':
            prijmy_list.insert(i, cislo_uctu[a]+(50-len(suma))*' '+suma[i])
            prijmy_list.insert(i+1, krstne_meno[a]+priezvisko[a])
            prijmy_list.insert(i+2, '')
#Neviem ci tam chceme pridat aj transakcie kariet
    prijmy_list.place(x=w//2+65,y=200)
    
    karty_tf=False
    platobny_prikaz_tf=False
    prijmy_tf=True

def login_cez_enter(sur):
    prihlas()
    
def login():
    global frame_3, login_tf, w,h,entryID, buttonPrihlasit,menuImg,labelMenuImg,prihlasit_btn, ID_entry, PW_entry, labelMenuImg, odhlasenie_btn, z_loginu, prihlasene, frame_2, vybraty_ucet,uctovnyDen

    vybraty_ucet = ''

    frame_2 = False
    frame_3 = False
    login_tf = True
    
    can.create_rectangle(0,0,w,h,fill='#71CAE7')
    uctovnyDen = datetime.datetime.now()
    prihlasene = False
    z_loginu=True
        
    can.create_text((1/2)*w,h-(0.8*h),text="Klientská Aplikácia Prihlásenie" ,font="Arial 30", anchor="w")
    can.create_text((1/2*w,h-(0.72*h)),text="Aktuálny účtovný deň: " + uctovnyDen.strftime("%d. %b. %Y"),font="Arial 16", anchor="w")
    can.create_text((1/2*w,h-(0.60*h)),text="ID obchodníka: ",font="Arial 20", anchor="w")
    ID_entry = tk.Entry(width=33,font = "Helvetica 15 bold")
    ID_entry.pack()
    ID_entry.place(x=1/2*w + 240,y=h-(0.62*h),height=30)
    ID_entry.bind("<Return>", login_cez_enter) 
    
    can.create_text((1/2*w,h-(0.60*h)+35),text="Zadajte rodné číslo: ",font="Arial 20", anchor="w")
    
    PW_entry = tk.Entry(width=33,font = "Helvetica 15 bold")
    PW_entry.pack()
    PW_entry.place(x=1/2*w + 240,y=h-(0.62*h)+35,height=30)
    PW_entry.bind("<Return>", login_cez_enter)
    
    prihlasit_btn = tk.Button(text='PRIHLÁSIŤ', font="Helvetica 15",command=prihlas)
    prihlasit_btn.pack()
    prihlasit_btn.place(x=1/2*w,y=h-(0.4*h))
    
    menuImg = tk.PhotoImage(master=can,file='obrazky/menu.png')
    
    labelMenuImg = tk.Label(image = menuImg,borderwidth=0)
    labelMenuImgimage = menuImg
    labelMenuImg.pack()
    labelMenuImg.place(x=0.03*w,y=h-(0.55*h), anchor="w")


def odhlas():
    global  ucty_list, karty_btn, transakcia_btn, platprik_btn, prijmy_btn, scrollbar, trans_list, spat_btn,odhlasenie_btn,otvor_okienko
    can.delete('all')
    odhlasenie_btn.destroy()
    vymaz_pravu_stranu()
    vymaz_lavu_stranu()
    
    if bol_f3:
        scrollbar.destroy()
        trans_list.destroy()
        spat_btn.destroy()
        otvor_okienko.destroy()
    login()
    
def vymaz_pravu_stranu():
    global potvrdplatbu_btn, prijemca_entry, suma_entry, splatdlh_btn, karty_list, prijmy_list,menuImg,labelMenuImg
    labelMenuImg.destroy()
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
        suma2_entry.destroy()

    elif prijmy_tf:
        can.delete('all')
        frame2()
        prijmy_list.destroy()

def vymaz_lavu_stranu():
    global karty_btn, prijmy_btn, platprik_btn, transakcia_btn, ucty_list
    can.delete('all')
    karty_btn.destroy()
    prijmy_btn.destroy()
    platprik_btn.destroy()
    transakcia_btn.destroy()
    ucty_list.destroy()

def spat_def():
    global scrollbar, trans_list, spat_btn,otvor_okienko
    can.delete('all')
    scrollbar.destroy()
    trans_list.destroy()
    spat_btn.destroy()
    otvor_okienko.destroy()
    labelMenuImg.destroy()
    frame2()

def prihlas():
    global prihlasit_btn, ID_entry, PW_entry, prihlasene,ID_klientov, rodne_cisla, prihlaseny_ID
    kon_klienti()
    citaj_klientov()
    if lock_klienti:
        can.delete('lock_oznam')
        can.delete('nespravne_udaje_oznam')
        can.create_text(1/2*w + 425,h-(0.62*h)+85, text='Prebieha audit, počkajte prosim',fill='red',font='Arial 15', tags='lock_oznam')
    else:
        can.delete('lock_oznam')
        can.delete('nespravne_udaje_oznam')
        for p in range(pocet):
            if ID_entry.get() == ID_klientov[p] and  PW_entry.get() == rodne_cisla[p]:
                prihlaseny_ID = ID_entry.get()
                prihlasene=True
                can.delete('all')
                prihlasit_btn.destroy()
                ID_entry.destroy()
                PW_entry.destroy()
                labelMenuImg.destroy()
                frame2()
                return
            else:
                can.create_text(1/2*w + 425,h-(0.62*h)+85, text='Nesprávne zadané prihlasovacie údaje',fill='red',font='Arial 15', tags='nespravne_udaje_oznam')
                
def kon_klienti():
    global lock_klienti
    if not os.path.exists('KLIENTI_LOCK.txt'):
        lock_klienti = False
    else:
        lock_klienti = True
    if not prihlasene:
        can.after(1,kon_klienti)

def citaj_klientov():
    global ID_klientov, rodne_cisla, pocet,krstne_meno,priezvisko
    if not lock_klienti:
        lock_subor = open('KLIENTI_LOCK.txt','w')
        subor = open('KLIENTI.txt','r')
        pocet = int(subor.readline().strip())
        krstne_meno=[]
        priezvisko=[]
        for r in range(pocet): 
            riadok = subor.readline().strip()
            k=riadok.split(';')
            ID_klientov.append(k[0])
            rodne_cisla.append(k[3])
            krstne_meno.append(k[1])
            priezvisko.append(k[2])
        subor.close()
        lock_subor.close()
        os.remove("KLIENTI_LOCK.txt")
    else:
        pocet=0

def kon_karty():
    global lock_karty
    if not os.path.exists('KARTY_LOCK.txt'):
        lock_karty = False
    else:
        lock_karty = True

def citaj_karty():
    global cisla_karty, typy_karty, dlh_karty, id_uctu_karty, id_karty, pocet_kariet
    if not lock_karty:
        lock_subor = open('KARTY_LOCK.txt','w')
        subor = open('KARTY.txt','r')
        pocet_kariet = int(subor.readline().strip())
        id_uctu_karty = []
        cisla_karty = []
        typy_karty = []
        dlh_karty = []
        id_karty = []
        for r in range(pocet_kariet): 
            riadok = subor.readline().strip()
            k=riadok.split(';')
            id_uctu_karty.append(k[6])
            cisla_karty.append(k[3])
            typy_karty.append(k[2])
            dlh_karty.append(k[7])
            id_karty.append(k[0])
        subor.close()
        lock_subor.close()
        os.remove("KARTY_LOCK.txt")
        
def kon_ucty():
    global lock_ucty
    if not os.path.exists('UCTY_LOCK.txt'):
        lock_ucty = False
        mozes = True
    else:
        lock_ucty = True
    if frame_2:
        can.after(100, kon_ucty)

def citaj_ucty():   
    global id_klienta_ucty, cislo_uctu, typ_uctu, stav_uctu, pocet_uctov, id_uctu
    if not lock_ucty:
        lock_subor = open('UCTY_LOCK.txt','w')
        subor = open('UCTY.txt','r')
        pocet_uctov = int(subor.readline().strip())
        #print(pocet_uctov)
        id_klienta_ucty = []
        cislo_uctu = []
        typ_uctu = []
        stav_uctu = []
        id_uctu = []
        for r in range(pocet_uctov): 
            riadok = subor.readline().strip()
            k=riadok.split(';')
            id_uctu.append(k[0])
            id_klienta_ucty.append(k[1])
            cislo_uctu.append(k[2])
            typ_uctu.append(k[3])
            stav_uctu.append(k[4])
        subor.close()
        lock_subor.close()
        os.remove("UCTY_LOCK.txt")

def kon_transakcie_ucty():
    global lock_transakcie_ucty
    if not os.path.exists('TRANSAKCIE_UCTY_LOCK.txt'):
        lock_transakcie_ucty = False
    else:
        lock_transakcie_ucty = True


def citaj_transakcie_ucty():
    global id_uctu_transakcie, id_klienta_transakcie,suma,id_transakcie,pocet_transakcii,komu
    if not lock_transakcie_ucty:
##        can.delete('lock_tran_ucty_oznam')
        lock_subor = open('TRANSAKCIE_UCTY_LOCK.txt','w')
        subor = open('TRANSAKCIE_UCTY.txt','r')
        pocet_transakcii = int(subor.readline().strip())
        id_uctu_transakcie = []
        id_klienta_transakcie = []
        suma = []
        id_transakcie = []
        komu=[]
        for r in range(pocet_transakcii): 
            riadok = subor.readline().strip()
            k=riadok.split(';')
            id_uctu_transakcie.append(k[4])
            id_klienta_transakcie.append(k[3])
            suma.append(k[5])
            id_transakcie.append(k[0])
            komu.append(k[6])
        subor.close()
        lock_subor.close()
        os.remove("TRANSAKCIE_UCTY_LOCK.txt")
##    else:
##        can.create_text(1/2*w + 425,h-(0.62*h)+85, text='Prebieha audit, počkajte prosim',fill='red',font='Arial 15', tags='lock_tran_ucty_oznam')

        
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bol_lock_ucty = False
prihlaseny_ID = 1
lock_ucty=False
ID_klientov=[]
rodne_cisla=[]
bol_f3 = False # poistka kvoli blbnutiu odhlasenia f3 je frame 3
dlh = 0
karty_tf=False
platobny_prikaz_tf=False
prijmy_tf=False
z_loginu=True
login()


