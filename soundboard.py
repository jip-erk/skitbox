from __future__ import unicode_literals
from re import L
from turtle import bgcolor
from matplotlib.pyplot import fill, grid
from pygame import mixer #Playing sound

import tkinter as tk 
from tkinter import *
from tkinter import ttk
from os import walk
import youtube_dl
import keyboard

import threading

#pygame test 
mixer.init()
#[get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))] 
mixer.quit() #Quit the mixer as it's initialized on your main playback device
mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)') #Initialize it with the correct device






ydl_opts = {
 'outtmpl': 'sounds/%(title)s.%(ext)s',
 'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192'
    }],
    'postprocessor_args': [
        '-ar', '16000'
    ],
    'prefer_ffmpeg': True,
    'keepvideo': False
}



PrimaryCol = '#ebebeb'
secondaryCol = '#dbdbdb'

root = tk.Tk()
root.configure(bg=PrimaryCol)
root.title('Skitbox')
root.geometry("610x440")




root.wm_iconbitmap('skitbox-logo.ico')

device_num = tk.IntVar()

variable = StringVar(root)
variable.set("one") # default value





keyboard.on_press_key("f7", lambda _:play(lbox.get(ACTIVE)))  






f = []

onOff = IntVar()

def play(sound):
   filename = 'sounds/' + sound
   mixer.music.load(filename) #Load the mp3
   mixer.music.play() #Play it

def stop():
    mixer.music.stop()
    

def TogglePlay():
    if onOff.get() == 1:
        mixer.music.pause()
    else:
        mixer.music.unpause()
        
#selectorbg

colm = 0
o = 0
sid = 0
def UpdateSounds():
    for (dirpath, dirnames, filenames) in walk('sounds/'):
        
        for x in filenames:
            if not x in f:
                global o
                global colm
                global sid
                sid += 1
                if o > 4:
                    o = 0
                    colm += 1
                o += 1
                truncated_text = x[:18] + '...'
                lbox.insert(END, x)
                #tk.Button(myCanvas, text=truncated_text, width=25,height=5 , bg='#1f62cf', border=0, command=lambda m=x :  play(m) ).grid(row=o, column=colm, pady=5, padx=5, sticky=N+S+E+W)
                btn = Button(myCanvas, text=truncated_text, width=25,height=5 , bg='#1f62cf', border=0 , command=lambda m=x :  play(m) )
                Grid.columnconfigure(myCanvas, colm, weight=1)
                Grid.rowconfigure(myCanvas, o, weight=1)
                btn.grid(column=colm, row=o,pady=1, padx=1, sticky="news")
                f.append(x)

      
       




scrollbar = tk.Scrollbar(root, orient="vertical")
lbox = tk.Listbox(root,bg=PrimaryCol, highlightthickness=0,  borderwidth=0 , width=30, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=lbox.yview)

scrollbar.pack(side="right", fill="y")
lbox.pack(padx=10, pady=10, side="right",fill="both")

listboxSet = tk.Canvas(root,bg=PrimaryCol,highlightthickness=0, height=190, width=20)
listboxSet.pack(side="top", fill="both")
#botton bg 
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

myCanvas = tk.Canvas(root, bg=secondaryCol, highlightthickness=0)
myCanvas.pack(side="top", fill="both", expand=1) 






   # for i in range(len(f)):




#listbox with all sounds 

#on start get sounds    
UpdateSounds()

#keystroke hotkey shit


my_menu = Menu(root)
root.config(menu=my_menu)



def new():
    win = tk.Toplevel()
    win.wm_title("Window")
    win.geometry("220x130")
    win.configure(bg=secondaryCol)

    text = Text(win, width=40, height=2)
    text.pack(fill=Y)
    text.insert(tk.END, "put youtube link URL here")


    l = tk.Entry(win, width=40)
    l.pack(fill=Y)

    b = tk.Button(win, text="Okay", width=40, height=2, command= lambda: [threading.Thread(target=GetYoutubeVid(l)).start(), UpdateSounds(), win.destroy])
    b.pack(fill=Y)

    text = Text(win, width=40, height=2)
    text.pack(fill=Y)
    text.insert(tk.END, "**warning** app might stop \n responding just wait ")
    UpdateSounds()


    



    

def setVolume(val):

    mixer.music.set_volume(float(val))

style = ttk.Style()
style.configure("TScale",  background=PrimaryCol)
#slider = tk.Scale(listboxSet,from_=0, to=1, digits = 3, resolution = 0.01 ,orient=tk.HORIZONTAL, bg=PrimaryCol, command=setVolume, bd=0, highlightthickness=0, relief='ridge')
slider = ttk.Scale(listboxSet,from_=0, to=1,orient=tk.HORIZONTAL, command=setVolume, style="TScale")
slider.set(1)
slider.pack(side="right")
 
def volume():
    win = tk.Toplevel()
    win.wm_title("Window")
    win.geometry("400x300")
    
 

def GetYoutubeVid(l):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        root.update()
        ydl.download([l.get()])



    

file_menu = Menu(my_menu, tearoff=False)
my_menu.add_cascade(label="File", menu=file_menu)
my_menu.add_command(label="stop", command=stop)
my_menu.add_checkbutton(label="pause/resume", variable=onOff, command=TogglePlay)




file_menu.add_command(label="New", command=new)
file_menu.add_command(label="Open file", command=new)

root.mainloop()


