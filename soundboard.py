from __future__ import unicode_literals
from ast import With
import audioop
from glob import glob
from msilib.schema import Billboard
from re import L
from turtle import bgcolor, width
from matplotlib import image
from matplotlib.pyplot import bar, fill, grid, pause, text
from pygame import mixer #Playing sound

import subprocess

import tkinter as tk 
#from tkinter import *
from tkinter import Y, Button, ttk
from os import walk
import pygame
import youtube_dl
import keyboard

import threading

#pygame test 
mixer.init()
#[get_audio_device_name(x, 0).decode() for x in range(get_num_audio_devices(0))] 
mixer.quit() #Quit the mixer as it's initialized on your main playback device
mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)') #Initialize it with the correct device

PrimaryCol = '#ebebeb'
secondaryCol = '#dbdbdb'

root = tk.Tk()
root.configure(bg=PrimaryCol)
root.title('Skitbox')
root.geometry("610x440")




def my_hook(d):
    if d['status'] == 'downloading':
        print ("downloading "+ str(round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1))+"%")
        bar['value'] = round(float(d['downloaded_bytes'])/float(d['total_bytes'])*100,1)
        root.update()       
    if d['status'] == 'finished':
        filename=d['filename']
        print(filename)
        win.destroy()

ydl_opts = {
 'outtmpl': 'sounds/%(title)s.%(ext)s',
 'quiet': True,
 'no_warnings': True,
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
    'keepvideo': False,
    'progress_hooks': [my_hook]
}










root.wm_iconbitmap('imgs\skitbox-logo.ico')

device_num = tk.IntVar()

variable = tk.StringVar(root)
variable.set("one") # default value


keyboard.on_press_key("f7", lambda _:play(lbox.get(tk.ACTIVE)))  

f = []

onOff = tk.IntVar()




def play(sound):
   global filename 
   filename = 'sounds/' + sound
   mixer.music.load(filename) #Load the mp3
   mixer.music.play() #Play it

   global slider_pos
   song = pygame.mixer.Sound(filename)
   slider_pos = int(song.get_length())
  # AudioProgress.config(to=slider_pos, value=0) 
   #play_Time()



def play_Time():
    current_time = pygame.mixer.music.get_pos() / 1000
    newtime = current_time
    newtime += 1
   
    
   # if int(AudioProgress.get()) == int(current_time):
     #   print(AudioProgress.get(), current_time)
        #AudioProgress.config(to=slider_pos, value=int(newtime))
       
  #  else:
     #   AudioProgress.config(to=slider_pos, value=int(AudioProgress.get()))
        #mixer.music.play(loops=0, start=int(AudioProgress.get())) 
        
    if current_time > 0.01:
        root.after(1000, play_Time)

def stop():
    mixer.music.stop()

pauze = 0
def TogglePlay():
    global pauze
    if mixer.music.get_busy():
        if pauze == 0:
            mixer.music.pause()
            pauze = 1
    else:
        mixer.music.unpause()
        pauze = 0


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
                lbox.insert(tk.END, x)
                #tk.Button(myCanvas, text=truncated_text, width=25,height=5 , bg='#1f62cf', border=0, command=lambda m=x :  play(m) ).grid(row=o, column=colm, pady=5, padx=5, sticky=N+S+E+W)
                btn = tk.Button(myCanvas, text=truncated_text, width=25,height=5 , bg='#1f62cf', border=0 , command=lambda m=x :  play(m) )
                tk.Grid.columnconfigure(myCanvas, colm, weight=1)
                tk.Grid.rowconfigure(myCanvas, o, weight=1)
                btn.grid(column=colm, row=o,pady=1, padx=1, sticky="news")
                f.append(x)
   
    

       


listboxSet = tk.Canvas(root,bg=PrimaryCol,highlightthickness=0, height=190, width=20)
listboxSet.pack(side="top", fill="both")




scrollbar = tk.Scrollbar(root, orient="vertical")
lbox = tk.Listbox(root,bg=PrimaryCol, highlightthickness=0,  borderwidth=0 , width=30, height=20, yscrollcommand=scrollbar.set)
scrollbar.config(command=lbox.yview)


scrollbar.pack(side="right", fill="y")
lbox.pack(padx=10, pady=10, side="right",fill="both")

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


my_menu = tk.Menu(root)
root.config(menu=my_menu)



def new():
    global win
    win = tk.Toplevel()
    win.wm_title("Window")
    win.geometry("220x130")
    win.configure(bg=secondaryCol)

    global bar
    bar = ttk.Progressbar(win, orient=tk.HORIZONTAL, length=300)
    bar.pack()

    text = tk.Text(win, width=40, height=2)
    text.pack(fill=tk.Y)
    text.insert(tk.END, "put youtube link URL here")

    
   


    l = tk.Entry(win, width=40)
    l.pack(fill=tk.Y)

    b = tk.Button(win, text="Okay", width=40, height=2, command= lambda: [threading.Thread(target=GetYoutubeVid(l)).start(), UpdateSounds(), win.destroy])
    b.pack(fill=tk.Y)

    text = tk.Text(win, width=40, height=2)
    text.pack(fill=tk.Y)
    text.insert(tk.END, "**warning** app might stop \n responding just wait ")
    UpdateSounds()






def folder():
    subprocess.Popen('explorer ".\sounds"')
    #subprocess.Popen('explorer', __file__)

def setVolume(val):
    mixer.music.set_volume(float(val))

file_icon = tk.PhotoImage(file = r"imgs\newFile.png") 
open_folder = tk.PhotoImage(file = r"imgs\open-folder.png") 
mic = tk.PhotoImage(file = r"imgs\mic.png") 
play_icon = tk.PhotoImage(file = r"imgs\play.png") 
stop_icon = tk.PhotoImage(file = r"imgs\stop.png")
info_icon = tk.PhotoImage(file = r"imgs\information.png")

newFile = tk.Button(listboxSet , width=25,height=25,command=new)
open_file = tk.Button(listboxSet , width=25,height=25, command=folder)
micc = tk.Button(listboxSet , width=25,height=25)
playy = tk.Button(listboxSet , width=25,height=25, command=TogglePlay)
stopp = tk.Button(listboxSet , width=25,height=25, command=stop)
info = tk.Button(listboxSet , width=25,height=25)

newFile.config(image=file_icon)
newFile.image = file_icon

micc.config(image=mic)
micc.image = mic

playy.config(image=play_icon)
playy.image = play_icon

stopp.config(image=stop_icon)
stopp.image = stop_icon

open_file.config(image=open_folder)
open_file.image = open_folder

info.config(image=info_icon)
info.image = info_icon

newFile.pack(side="left")
open_file.pack(side="left")
info.pack(side="left")
playy.pack(side="left")
stopp.pack(side="left")


style = ttk.Style()
style.configure("TScale", background=PrimaryCol)
#slider = tk.Scale(listboxSet,from_=0, to=1, digits = 3, resolution = 0.01 ,orient=tk.HORIZONTAL, bg=PrimaryCol, command=setVolume, bd=0, highlightthickness=0, relief='ridge')
slider = ttk.Scale(listboxSet,from_=0, to=1,orient=tk.HORIZONTAL, command=setVolume, style="TScale")
slider.set(1)
micc.pack(side="left")
slider.pack(side="left")

#AudioProgress = ttk.Scale(listboxSet,from_=0, to=1, length=200,orient=tk.HORIZONTAL,command=slide ,style="TScale")
#AudioProgress.pack(side="right")
#AudioProgress.pack()
 
 

def GetYoutubeVid(l):
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        root.update()
        ydl.download([l.get()])





#my_menu.add_cascade(label="File", menu=file_menu)
#my_menu.add_command(label="stop", command=stop)
#my_menu.add_checkbutton(label="pause/resume", variable=onOff, command=TogglePlay)


#file_menu.add_command(label="New", command=new)
#file_menu.add_command(label="Open file", command=new)

root.mainloop()


