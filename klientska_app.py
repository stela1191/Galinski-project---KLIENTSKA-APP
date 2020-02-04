import tkinter as tk
import datetime
import os
import math


h=720
w=1280

# DOROBIT : - vytvorenie LOCKU ked s tym pracujem, vymazanie locku, close subor
#           - vysvietit naraz
#           - Refreshovat ucty a hlavne pocet transakcii po platobnom prikaze inac nejdu transakcie ani prijmy
#           - Grafiku
#           - Dorobit Transakcie ucty pridat zplatenie kreditnej karty 

# HOTOVE :  - Platobny prikaz je pripraveny
#           - Dorobit citanie transakcii desatinne cisla
# OTAZKY :  - Neviem ako rozlisime pri zapisovani prijmu ci je to z kreditnej alebo debetnej karty



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

def kontrola_verzii():
    global klienti_verzia_var, ucty_verzia_var, karty_verzia_var, tran_ucty_verzia_var
    subor = open('KLIENTI_VERZIA.txt','r')
    verzia = subor.readline().strip()
    #if klienti_verzia_var == verzia:
    #    print('verzia_klienti:'+verzia)
    if not klienti_verzia_var == verzia:
        klienti_verzia_var = verzia
        print('zmena_v_klienta:', klienti_verzia_var)
        refresh_klienti()
    subor.close()
    
    subor = open('UCTY_VERZIA.txt','r')
    verzia = subor.readline().strip()
    #if ucty_verzia_var == verzia:
    #    print('verzia_ucty:'+verzia)
    if not ucty_verzia_var == verzia:
        ucty_verzia_var = verzia
        print('zmena_v_uctu:', ucty_verzia_var)
    subor.close()
    
    subor = open('KARTY_VERZIA.txt','r')
    verzia = subor.readline().strip()
    #if karty_verzia_var == verzia:
    #    print('verzia_karty:'+verzia)
    if not karty_verzia_var == verzia:
        karty_verzia_var = verzia
        print('zmena_v_karty:', karty_verzia_var)
        if karty_tf:
            vymaz_pravu_stranu()
            karty_def()
    subor.close()
    
    subor = open('TRANSAKCIE_UCTY_VERZIA.txt','r')
    verzia = subor.readline().strip()
    #if tran_ucty_verzia_var == verzia:
    #    print('verzia_tran_ucty:'+verzia)
    if not tran_ucty_verzia_var == verzia:
        if frame_3:
            spat_def()
            frame3()
        tran_ucty_verzia_var = verzia
        print('zmena_v_trans_uctov:', tran_ucty_verzia_var)
    subor.close()
    
    can.after(1000,kontrola_verzii)

def refresh_klienti():
    global refreshujem_klientov
    if not refreshujem_klientov:
        kon_klienti()
    if not lock_klienti:
        if prihlasene:
            subor_lock = open('KLIENTI_LOCK.txt','w')
            subor = open('KLIENTI.txt','r')
            pocet_klientov = subor.readline().strip()
            for a in range(int(pocet_klientov)):
                riadok = subor.readline().strip()
                riadok_split = riadok.split(';')
                if riadok_split[0] == prihlaseny_ID:
                    print('existuje furt')
                    if riadok_split[1] == krstne_prihlaseny:
                        if riadok_split[2] == priezvisko_prihlaseny:
                            if riadok_split[3] == rc_prihlaseny:
                                print('vsetko sedi')
                            else:
                                login()
            refreshujem_klientov = False
            subor.close()
            subor_lock.close()
            os.remove("KLIENTI_LOCK.txt")
    elif lock_klienti:
        can.after(1000,refresh_klienti)
        refreshujem_klientov = True
        
def frame2():
    global z_frame_3,frame_3, login_tf, prihlasit_btn, ID_entry, pocet_uctov,ucty_list,karty_btn,transakcia_btn,menuImg,labelMenuImg,platprik_btn,potvrdplatbu_btn,prijmy_btn,splatdlh_btn,prijemca_entry,suma_entry,can, odhlasenie_btn, z_loginu, frame_2,id_uctov_frame2

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
        for l in range((pocet_uctov)-1):
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
##        if not bol_lock_ucty:
##            labelMenuImg = tk.Label(image = menuImg,borderwidth=0)
##            labelMenuImgimage = menuImg
##            labelMenuImg.pack()
##            labelMenuImg.place(x=0.45*w,y=h-(0.50*h), anchor="w")
    else:
        if not z_loginu or not z_frame_3:
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
        odhlasenie_btn.place(width=100,height=35,x=w-200,y=10)
        labelMenuImg = tk.Label(image = menuImg,borderwidth=0)
        labelMenuImgimage = menuImg
        labelMenuImg.pack()
        labelMenuImg.place(x=0.45*w,y=h-(0.50*h), anchor="w")
        z_loginu=False
    if z_frame_3:
        labelMenuImg = tk.Label(image = menuImg,borderwidth=0)
        labelMenuImgimage = menuImg
        labelMenuImg.pack()
        labelMenuImg.place(x=0.45*w,y=h-(0.50*h), anchor="w")
        z_frame_3=False
##    if z_loginu:
##        odhlasenie_btn=tk.Button(root,text='ODHLÁSIŤ SA',command=odhlas)
##        odhlasenie_btn.place(width=100,height=35,x=w-200,y=10)
##        z_loginu=False

    
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
    global frame_3, scrollbar, trans_list, cislo,spat_btn, h_alebo_p ,otvor_okienko,bol_f3, frame_2, id_uctu,vybraty_ucet,okno,id_uctu_transakcie,prihlaseny_ID, id_klienta_transakcie,pocet_transakcii,komu,cislo_uctu,krstne_meno,priezvisko,a,sucet_kladnych,sucet_zapornych,celkova_suma

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
    if not lock_ucty and not lock_klienti and not lock_transakcie_ucty:
        for i in range(pocet_transakcii):
            if id_klienta_transakcie[i]==prihlaseny_ID and vybraty_ucet==id_uctu_transakcie[i] and h_alebo_p[i]=='P':
                a=int(komu[i])
                trans_list.insert(cislo, cislo_uctu[a]+(120-len(suma[i]))*' '+suma[i]+' €')
                trans_list.insert(cislo+1, krstne_meno[a]+' '+priezvisko[a])
                trans_list.insert(cislo+2, '')
                if int(float(suma[i]))>0:
                    celkova_suma+=int(float(suma[i]))
                elif int(float(suma[i]))<0:
                    celkova_suma-=int(float(suma[i]))
                if (suma[i][0])=='-':
                    sucet_zapornych-=int(float(suma[i]))
                    trans_list.itemconfig(cislo,{'fg': 'red'})
                    trans_list.itemconfig(cislo+1,{'fg': 'red'})
                if (suma[i][0])=='+':
                    sucet_kladnych+=int(float(suma[i]))
                    trans_list.itemconfig(cislo,{'fg': 'green'})
                    trans_list.itemconfig(cislo+1,{'fg': 'green'})
                cislo+=3
                print(celkova_suma)
        for i in range(pocet_transakcii):
            if id_klienta_transakcie[i]==prihlaseny_ID and vybraty_ucet==id_uctu_transakcie[i] and h_alebo_p[i]=='H':
                trans_list.insert(cislo, 'SK'+22*'*'+(130-len(suma[i]))*' '+suma[i]+' €')
                trans_list.insert(cislo+1, 'Prevod hotovostou')
                trans_list.insert(cislo+2, '')
                if int(float(suma[i]))>0:
                    celkova_suma+=int(float(suma[i]))
                elif int(float(suma[i]))<0:
                    celkova_suma-=int(float(suma[i]))
                if (suma[i][0])=='-':
                    sucet_zapornych-=int(float(suma[i]))
                    trans_list.itemconfig(cislo,{'fg': 'red'})
                    trans_list.itemconfig(cislo+1,{'fg': 'red'})
                if (suma[i][0])=='+':
                    sucet_kladnych+=int(float(suma[i]))
                    trans_list.itemconfig(cislo,{'fg': 'green'})
                    trans_list.itemconfig(cislo+1,{'fg': 'green'})
                cislo+=3
                print(celkova_suma)

    trans_list.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=trans_list.yview)
        
    spat_btn = tk.Button(root,text='SPÄŤ',command=spat_def)
    spat_btn.place(width=200,height=35,x=100,y=10)
    okno=False
    if okno==False:
        #otvor_okienko.destroy()
        otvor_okienko = tk.Button(root,text='ZOBRAZ GRAF',command=okienko,state='active')
        otvor_okienko.place(width=200,height=35,x=w-300,y=h-95)


def okienko():
    global sucet_kladnych,sucet_zapornych,celkova_suma,plusova,minusova,zaporne,kladne,okno, otvor_okienko
    okno=True
    newroot=tk.Tk()
    newroot.geometry('460x410')
    myCanvas = tk.Canvas(newroot, bg="white", height=410, width=460)
    coord = 10, 10, 390, 390
    percento_kladne=(sucet_kladnych*100)/celkova_suma
    print(percento_kladne)
    uhol_kladne=360*(percento_kladne)/100
    print(uhol_kladne)
    percento_zaporne=(sucet_zapornych*100)/celkova_suma
    print(percento_zaporne)
    uhol_zaporne=360*(percento_zaporne)/100
    print(uhol_zaporne)
    if (sucet_zapornych*100)!=0 or celkova_suma!=0:
        arc = myCanvas.create_arc(coord, start=0, extent=uhol_zaporne, fill="red")
        arv2 = myCanvas.create_arc(coord, start=uhol_zaporne, extent=uhol_kladne, fill="green")
        myCanvas.create_text(410,100,text=str(sucet_zapornych)+' €',fill='red',font='Arial 15')
        myCanvas.create_text(410,300,text=str(sucet_kladnych)+' €',fill='green',font='Arial 15')
    if (sucet_zapornych*100)==0:
        arc = myCanvas.create_arc(coord, start=0, extent=359, fill="green",outline='green')
        myCanvas.create_text(200,150,text=str(celkova_suma)+' €',fill='white',font='Arial 15')
        arc = myCanvas.create_arc(coord, start=359, extent=1, fill="green",outline='green')
    elif (sucet_kladnych*100)==0:
        arc = myCanvas.create_arc(coord, start=0, extent=359, fill="red",outline='red')
        myCanvas.create_text(200,150,text=str(celkova_suma)+' €',fill='white',font='Arial 15')
        arc = myCanvas.create_arc(coord, start=359, extent=1, fill="red",outline='red')
    otvor_okienko.destroy()
    otvor_okienko = tk.Button(root,text='ZOBRAZ GRAF',command=okienko,state='disabled')
    otvor_okienko.place(width=200,height=35,x=w-300,y=h-95)

    myCanvas.pack()
    root.mainloop()


def platobny_prikaz_def():
    global platobny_prikaz_tf, karty_tf, prijmy_tf, potvrdplatbu_btn, prijemca_entry, suma_entry, cislo_uctu,pocet_uctov, pocet_transakcii,stav_vybrateho_uctu, typy_karty,prihlaseny_ID,uctovnyDen
    vymaz_pravu_stranu()
    labelMenuImg.destroy()

    kon_ucty()
    citaj_ucty()

    can.create_text(w//2+255,150,text='PLATOBNY PRIKAZ',font='Arial 25')
    
    potvrdplatbu_btn=tk.Button(root,text='POTVRDIŤ PLATBU',command=sprav_platobny_prikaz,state='active')
    potvrdplatbu_btn.place(width=200,height=35,x=w//2+155,y=340)
    
    prijemca_entry = tk.Entry(root)
    prijemca_entry.place(width=200,height=35,x=w//2+155,y=210)
    
    suma_entry = tk.Entry(root)
    suma_entry.place(width=200,height=35,x=w//2+155,y=280)
    
    can.create_text(w//2+255,190,text='Prijemca')
    can.create_text(w//2+255,260,text='Suma')
    
    karty_tf=False
    platobny_prikaz_tf=True
    prijmy_tf=False

def sprav_platobny_prikaz():
    global stav_vybrateho_uctu, suma_entry, prijemca_entry, prihlaseny_ID, pocet_uctov, id_suvisiacej_transakcie,stav
    subor_transakcie=open('TRANSAKCIE_UCTY.txt','r')
    subor_transakcie_NEW=open('TRANSAKCIE_UCTY_NEW.txt','w')
    subor_ucty=open('UCTY.txt','r')
    datum = datetime.date.today().strftime('%d%m%Y')
    print(datum)
    print(stav_vybrateho_uctu)
    print(suma_entry.get())
    print(prijemca_entry.get())
    cislo_uctu= []
    id_klienta_ucty = []
    id_transakcie = []
    id_uctu = []
    stav_uctu = []
    pocet_transakcii=int(subor_transakcie.readline().strip())
    pocet_uctov=int(subor_ucty.readline().strip())
    subor_transakcie_NEW.write(str(pocet_transakcii))
    for v in range(pocet_transakcii):
        riadocek=subor_transakcie.readline().strip()
        subor_transakcie_NEW.write('\n'+riadocek)
        a=riadocek.split(';')
        id_transakcie.append(a[0])
        najvacsie_cislo=id_transakcie
    print(najvacsie_cislo)
    subor_transakcie_NEW.close()
    subor_transakcie_NEW=open('TRANSAKCIE_UCTY_NEW.txt','a')
    uspesna=0
    num_lines = sum(1 for line in open('TRANSAKCIE_UCTY.txt'))
    pocetriadkov = num_lines - (1)
    pocetriadkov_str = str(pocetriadkov)
    print(pocetriadkov_str)

    for u in range(pocet_uctov):
        riadok = subor_ucty.readline().strip()
        k=riadok.split(';')
        id_uctu.append(k[0])
        id_klienta_ucty.append(k[1])
        cislo_uctu.append(k[2])
        stav_uctu.append(k[4])
        if (stav_vybrateho_uctu)>=(suma_entry.get()) and prijemca_entry.get()==cislo_uctu[u]:
            can.create_rectangle(w//2+230,h-220,w//2+280,h-240,fill='#71CAE7', outline='#71CAE7')
            print(suma_entry.get())
            stav=(str(float(stav_vybrateho_uctu)-float(suma_entry.get())))
            print(stav)
            if (stav[0])=='-':
                can.create_rectangle(w//2+230,h-220,w//2+280,h-240,fill='#71CAE7', outline='#71CAE7')
                uspesna=0
                textik=can.create_text(w//2+255,h-230,text='Nedostatok penazi na ucte', fill='red', font='Arial 12',tags='no_money')
                stav=stav_vybrateho_uctu
                print('NIEEEEEEEEEE')
            else:
                textik=can.create_text(w//2+255,h-230,text='Transakcie bola uspesne uskutocnena', fill='green', font='Arial 12',tags='uskutocnena')
                subor_transakcie_NEW.write('\n'+(str(pocet_transakcii+1))+';'+'D'+';'+'P'+';'+vybraty_ucet+';'+prihlaseny_ID+';'+'-'+suma_entry.get()+';'+(str(pocet_transakcii+2))+';'+datum+';'+id_klienta_ucty[u])
                subor_transakcie_NEW.write('\n'+(str(pocet_transakcii+2))+';'+'D'+';'+'P'+';'+id_uctu[u]+';'+id_klienta_ucty[u]+';'+'+'+suma_entry.get()+';'+(str(pocet_transakcii+1))+';'+datum+';'+prihlaseny_ID)
                print('Moze prebehnut')
            uspesna=1
            if uspesna==1:
                uspesna=0
                p=str(pocet_transakcii+2)
                pocet_transakcii=p
                print(pocet_transakcii)
                potvrdplatbu_btn=tk.Button(root,text='POTVRDIŤ PLATBU',command=sprav_platobny_prikaz,state='disabled')
                potvrdplatbu_btn.place(width=200,height=35,x=w//2+155,y=340)
        
        else:
            uspesna=0
            print('NIEEEEEEEEEEE')
            #can.create_text(w//2+255,h-230,text='Neexistujuci ucet', fill='red', font='Arial 12',tags='neexistuje')
      
    subor_ucty.close()
    subor_transakcie_NEW.close()

    subor_transakcie=open('TRANSAKCIE_UCTY.txt','w')
    subor_transakcie_NEW=open('TRANSAKCIE_UCTY_NEW.txt','r')
    riadok=subor_transakcie_NEW.readline().strip()
    subor_transakcie.write(str(pocet_transakcii))
    while riadok!='':
        riadok=subor_transakcie_NEW.readline().strip()
        subor_transakcie.write('\n'+riadok)
    subor_transakcie.close()
    subor_transakcie_NEW.close()
    os.remove('TRANSAKCIE_UCTY_NEW.txt')
    
    subor_ucty=open('UCTY.txt','r')
    subor_ucty_NEW=open('UCTY_NEW.txt','w')
    for line in subor_ucty:
        subor_ucty_NEW.write(line.replace(stav_vybrateho_uctu,stav))

    subor_ucty.close()
    subor_ucty_NEW.close()

    subor_ucty=open('UCTY.txt','w')
    subor_ucty_NEW=open('UCTY_NEW.txt','r')
    riadok=subor_ucty_NEW.readline().strip()
    subor_ucty.write(str(pocet_uctov))
    while riadok!='':
        riadok=subor_ucty_NEW.readline().strip()
        subor_ucty.write('\n'+riadok)
    subor_ucty.close()
    subor_ucty_NEW.close()
    os.remove('UCTY_NEW.txt')
    
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
            if a==0:
                subor_.write(riadok) 
            else:
                subor_.write('\n'+riadok)   
        subor.close()
        subor_.close()
        
        subor_ = open('KARTY_.txt','r')
        subor = open('KARTY.txt','w')
        for a in range(int(pocet_kariet)+1):
            riadok = subor_.readline().strip()
            if a == 0:
                subor.write(riadok)
            riadok_split=riadok.split(';')
            if a > 0:
                if riadok_split[0] == vybrata_karta:
                    r_ = riadok.split(';')
                    dlh = str(float(dlh_vybratej_karty) - float(splatene))
                    dlh_vybratej_karty = dlh
                    r_[7]=dlh
                    print(dlh)
                    riadok = ';'.join(r_)
                    subor.write('\n'+riadok)
                else:
                    subor.write('\n'+riadok)
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
                suboris.write(riadok)
            
            if a > 0:
                riadocek_split = riadocek.split(';')
                if vybraty_ucet == riadocek_split[0]:
                    r_=riadocek.split(';')
                    r_[4] = str(float(stav_vybrateho_uctu) - float(splatene))
                    stav_vybrateho_uctu = r_[4]
                    print('nasiel sa ucet', 'stav noveho: ' + r_[4])
                    riadok = ';'.join(r_)
                    suboris.write('\n'+riadok)
                else:
                    suboris.write('\n'+riadocek)
        suboris.close()
        suboris_.close()

        os.remove("UCTY_.txt")
        os.remove("KARTY_.txt")

##        subor_t_NEW=open('TRANSAKCIE_UCTY_NEW.txt','w')
##        subor_t=open('TRANSAKCIE_UCTY.txt','r')
##        pocet_t=subor_t.readline().strip()
##        subor_t_NEW.write(str(int(pocet_t)+1))
##        for p in range(int(pocet_t)+1):
##            r=subor_t.readline().strip()
##            subor_t_NEW.write(r+'\n')
##        subor_t.close()
##        subor_t_NEW.close()
##
##        subor_t_NEW=open('TRANSAKCIE_UCTY_NEW.txt','r')
##        subor_t=open('TRANSAKCIE_UCTY.txt','w')
##        pocet_t=subor_t_NEW.readline().strip()
##        subor_t.write(pocet_t)
##        while riadok!='':
##            riadok=subor_t_NEW.readline().strip()
##            subor_t.write(riadok+'\n')
##        subor_t.write((str(pocet_t+1))+';'+'K'+';'+'P'+';'+vybraty_ucet+';'+prihlaseny_ID+';'+'-'+float(splatene)+';'+''+';'+datum+'\n')
##        subor_t.close()
##        subor_t_NEW.close()
##        subor_t_NEW.destroy()
##        frame2()
##        karty_def()
##    else:
##        print('nesplatene')
##    
##    subor.close()
    splatka=True
    karty_def()
    
def karty_def():
    global refreshujem_karty,id_kariet_box, dlh_kariet_box, platobny_prikaz_tf,karty_tf, prijmy_tf, kreditka, splatka,splatdlh_btn, karty_list, id_uctu_karty,dlh_karty, splatene,suma2_entry,dlh,prihlasit_btn, ID_entry, ucty_list,karty_btn,transakcia_btn,platprik_btn,potvrdplatbu_btn,prijmy_btn,splatdlh_btn,prijemca_entry,suma_entry
    vymaz_pravu_stranu()

    id_kariet_box = []
    dlh_kariet_box = []
    if not refreshujem_karty:
        kon_karty()

    if not lock_karty:
        refreshujem_karty = False
        print('vykreslujem karty')
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
    else:
        refreshujem_karty = True
        print('refreshujem_karty')
        can.after(2500, karty_def)
    
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
    cislo=0
    for i in range(pocet_transakcii):
        a=int(id_klienta_transakcie[i])
        if  prihlaseny_ID==komu[i] and suma[i][0]=='+':
            prijmy_list.insert(cislo, cislo_uctu[a]+(25-len(suma[i]))*' '+'+'+(suma[i])+' €')
            prijmy_list.insert(cislo+1, krstne_meno[a]+' '+priezvisko[a])
            prijmy_list.insert(cislo+2, '')
        cislo+=3

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
    global scrollbar, trans_list, spat_btn,otvor_okienko, z_frame_3
    z_frame_3 = True
    can.delete('all')
    scrollbar.destroy()
    trans_list.destroy()
    spat_btn.destroy()
    otvor_okienko.destroy()
    labelMenuImg.destroy()
    frame2()

def prihlas():
    global prihlasit_btn, ID_entry, PW_entry, prihlasene,ID_klientov, rodne_cisla, prihlaseny_ID, krstne_prihlaseny, priezvisko_prihlaseny, rc_prihlaseny
    kon_klienti()
    citaj_klientov()
    ID_prihlaseneho=ID_entry.get()
    print(ID_prihlaseneho)
    if lock_klienti:
        can.delete('lock_oznam')
        can.delete('nespravne_udaje_oznam')
        can.create_text(1/2*w + 425,h-(0.62*h)+85, text='Prebieha audit, počkajte prosim',fill='red',font='Arial 15', tags='lock_oznam')
    else:
        can.delete('lock_oznam')
        can.delete('nespravne_udaje_oznam')
        for p in range(pocet):
            if ID_entry.get() == ID_klientov[p] and  PW_entry.get() == rodne_cisla[p]:
                print('umiestnenie pod poctom: '+str(p))
                krstne_prihlaseny = krstne_meno[p]
                priezvisko_prihlaseny = priezvisko[p]
                rc_prihlaseny = rodne_cisla[p]
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
    if os.path.exists('KLIENTI_LOCK.txt'):
        lock_klienti = True
    else:
        lock_klienti = False
    if lock_klienti:
        print('**KLIENTI.txt LOCKED**')
        can.after(2000,kon_klienti)

def citaj_klientov():
    global ID_klientov, rodne_cisla, pocet,krstne_meno,priezvisko
    if not lock_klienti:
        lock_subor = open('KLIENTI_LOCK.txt','w')
        subor = open('KLIENTI.txt','r+')
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
        print('nic som nenacital')
        can.after(2000,citaj_klientov)
        
def kon_karty():
    global lock_karty
    if not os.path.exists('KARTY_LOCK.txt'):
        lock_karty = False
    else:
        lock_karty = True
        can.after(2000,kon_karty)
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
        if frame_2 and lock_ucty :
            lock_ucty = False
            vymaz_pravu_stranu()
            frame2()
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
        if frame_3 and lock_transakcie_ucty:
            lock_transakcie_ucty=False
            frame3()
        lock_transakcie_ucty = False
    else:
        lock_transakcie_ucty = True
    if lock_transakcie_ucty:
        can.after(2000, kon_transakcie_ucty)

def citaj_transakcie_ucty():
    global id_uctu_transakcie, id_klienta_transakcie,suma,id_transakcie,pocet_transakcii,komu, id_suvisiacej_transakcie,h_alebo_p,lock_transakcie_ucty
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
        h_alebo_p = []
        id_suvisiacej_transakcie=[]
        for r in range(pocet_transakcii): 
            riadok = subor.readline().strip()
            k=riadok.split(';')
            id_uctu_transakcie.append(k[4])
            id_klienta_transakcie.append(k[3])
            suma.append(k[5])
            id_transakcie.append(k[0])
            id_suvisiacej_transakcie.append(k[6])
            komu.append(k[8])
            h_alebo_p.append(k[2])
##            print('id_uctu_transakcie '+id_uctu_transakcie[r])
##            print('id_klienta_transakcie '+id_klienta_transakcie[r])
##            print('suma '+suma[r])
##            print('id_transakcie '+id_transakcie[r])
##            print('id_suvisiacej_transakcie '+id_suvisiacej_transakcie[r])
##            print('komu '+komu[r])
##            print('h_alebo_p '+h_alebo_p[r])
        subor.close()
        lock_subor.close()
        os.remove("TRANSAKCIE_UCTY_LOCK.txt")
##    else:
##        can.create_text(1/2*w + 425,h-(0.62*h)+85, text='Prebieha audit, počkajte prosim',fill='red',font='Arial 15', tags='lock_tran_ucty_oznam')

        
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
bol_lock_ucty = False
prihlaseny_ID = 1
lock_ucty=False
lock_transakcie_ucty=False
ID_klientov=[]
rodne_cisla=[]
bol_f3 = False # poistka kvoli blbnutiu odhlasenia f3 je frame 3
dlh = 0
karty_tf=False
platobny_prikaz_tf=False
prijmy_tf=False
z_loginu=True
klienti_verzia_var = ''
ucty_verzia_var = ''
karty_verzia_var = ''
tran_ucty_verzia_var = ''
refreshujem_klientov = False
refreshujem_karty = False
z_frame_3 = False
login()
kontrola_verzii()


