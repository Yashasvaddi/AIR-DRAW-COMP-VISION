import tkinter as tk
window=tk.Tk()
i=-1
def close():
    window.destroy()

def own_camera():
    global i
    i=0
    window.after(1000,close)

def seperate_camera():
    global i
    i=3
    window.after(1000,close)

def camera_selector():
    window.title("AIR CANVAS")
    label=tk.Label(window,text="DO YOU WANT TO DISPLAY ON YOUR DEVICE \nOR\nDO YOU WANT TO RUN ON A EXTERNAL CAMERA?\n",font=("Times New Roman",14))
    label.grid(row=0,column=0,columnspan=10,pady=10)
    button1=tk.Button(window,text="Own Camera",command=own_camera)
    button1.grid(row=2,column=0,padx=90,pady=10)
    button2=tk.Button(window,text="Other Camera",command=seperate_camera)
    button2.grid(row=2,column=2,padx=25,pady=10)
    window.geometry("470x200")
    window.mainloop()
    return i

if __name__=="__main__":
    camera_selector()