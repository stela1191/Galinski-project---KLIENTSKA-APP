import tkinter as tk

h=720
w=1280

root = tk.Tk()
can = tk.Canvas(root,width=w,height=h)
can.pack()
frame = tk.Frame(root, bg='white',width=w,height=h)
frame.place(x=0,y=0)
can = tk.Canvas(frame,width=w,height=h)
can.pack()
button=tk.Button(frame,text='BUTONIK',command=frame.destroy)
button.place(width=200,x=w//2-100,y=h//2+50)
entry=tk.Entry(frame,width=200)
entry.place(width=60,x=w//2-30,y=h//2+20)
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

round_rectangle(400, 200, w-400, h-200, radius=50)
can.create_text(w//2,h//2-20,text='LOGIN',font='Arial 30')
root.mainloop()
