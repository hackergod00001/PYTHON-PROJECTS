# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 15:39:49 2020

@author: UPMANYU JHA
"""
# Note Befor using this code for audio player plz check and change the directory of the pictures and song as instructed
from tkinter import *
import pygame
from tkinter import filedialog
from PIL import ImageTk, Image
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title("UJ MP3 Player-V6")
root.iconbitmap("C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/UJ MP3 Player-v6.ico") #where ever any saves this folder plz make a not to change its addres accordingly
root.geometry("800x500")

# initialize pygame
pygame.mixer.init()


#Get song length and time info
def play_time():
    # Check for fast moving
    if stopped:
        return
    # current song time elasped
    current_time = pygame.mixer.music.get_pos() / 1000
    
    # throw up temp label to abstract data
    #slider_label.config(text=f"Slider: {int(my_slider.get())} and Song pos: {int(current_time)}")
    
    # convert time format
    converted_current_time = time.strftime("%H:%M:%S",time.gmtime(current_time))
    
    # get current playing song
    #current_song = playlist_box.curselection()
    #Grab song title from playlist
    song = playlist_box.get(ACTIVE)
    #add directory structure and mp3 to song title
    song = f"C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/{song}.mp3"
    # load song length with mutagen
    song_mut = MP3(song)
    #obtain song total length
    global song_length
    song_length=song_mut.info.length
    # convert to time format
    converted_song_length = time.strftime("%H:%M:%S",time.gmtime(song_length))
    
    #Increase the present time by 1 sec.
    current_time +=1
    
    if int(my_slider.get())  == int(song_length):
        status_bar.config(text=f"Time Elasped: {converted_song_length}  ")
    
    elif int(my_slider.get())  == int(current_time):
        #Slider hasn't been moverd
        #update slider to postion
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
        
    elif paused:
        pass
    
    
    else:
        #Slider has been mover
        #update slider to postion
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        
        # convert time format
        converted_current_time = time.strftime("%H:%M:%S",time.gmtime(int(my_slider.get())))
        
        # output time to status bar
        status_bar.config(text=f"Time Elasped: {converted_current_time}  of  {converted_song_length}  ")
        
        
        #Move this along by one sec.
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
    
    
    # output time to status bar
    #status_bar.config(text=f"Time Elasped: {converted_current_time}  of  {converted_song_length}  ")
    # Update sliders postion value to current song postion...
    #my_slider.config(value=int(current_time))
    
    
    
    # update timer
    status_bar.after(1000, play_time)
    
    

#Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir="my hite songs/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))# Hear we can other types of audio files also after comma
    
    #strip out the directory info and .mp3 extension from the playlist_box
    song= song.replace("C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/", "")
    song= song.replace(".mp3", "")
    
    # Add song to list_box
    playlist_box.insert(END, song)

# Add Many Songs to playlist
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="my hite songs/", title="Choose the songs", filetypes=(("mp3 Files", "*.mp3"), ))# Hear we can other types of audio files also after comma
    
    #loop through song list and replace directory info and mp3
    for song in songs:
        #strip out the directory info and .mp3 extension from the playlist_box
        song= song.replace("C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/", "")
        song= song.replace(".mp3", "")
    
        # Insert into playlist_box
        playlist_box.insert(END, song)

#Play selected song
def play():
    
    # Set Stopped variable to false so song can play
    global stopped
    stopped = False
    song = playlist_box.get(ACTIVE)
    song = f"C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    # call play_time fun. to gain song length
    play_time()
    
    #update slider to postion
    #slider_position = int(song_length)
    #my_slider.config(to=slider_position, value=0)
    
     #Get current volume
    #current_volume = pygame.mixer.music.set_volume()
    #slider_label.config(text=current_volume * 100)
    
     #Get current volume
    current_volume = pygame.mixer.music.get_volume()
    # Times by 100 to make it easier to work with
    current_volume = current_volume * 100
    #slider_label.config(text=current_volume * 100)
    
    # Change volume Meter picture
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)
    
    
# Stop playing current song
global stopped
stopped = False
def stop():
    #Reset Slider and Status bar
    status_bar.config(text="")
    my_slider.config(value=0)
    #Stop Song Frm Playing
    pygame.mixer.music.stop()
    playlist_box.selection_clear(ACTIVE)
    
    # clear the status bar
    status_bar.config(text="")
    
    #Set Stop Variable to true
    global stopped
    stopped = True
    
    
# play The next_songin the playlist_box
def next_song():
    #Reset Slider and Status bar
    status_bar.config(text="")
    my_slider.config(value=0)
    
    # get the current song tuple number
    next_one = playlist_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    #Grab song title from playlist
    song = playlist_box.get(next_one)
    #add directory structure and mp3 to song title
    song = f"C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/{song}.mp3"
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #Clear active bar in playlist listbox
    playlist_box.selection_clear(0, END)
    
    #Active new song bar
    playlist_box.activate(next_one)
    
    #Set Active Bar to nextsong
    playlist_box.selection_set(next_one, last=None)
    
#Play previous_song from the play list
def previous_song():
    #Reset Slider and Status bar
    status_bar.config(text="")
    my_slider.config(value=0)
    
    # get the current song tuple number
    next_one = playlist_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]-1
    #Grab song title from playlist
    song = playlist_box.get(next_one)
    #add directory structure and mp3 to song title
    song = f"C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/{song}.mp3"
    #load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    
    #Clear active bar in playlist listbox
    playlist_box.selection_clear(0, END)
    
    #Active new song bar
    playlist_box.activate(next_one)
    
    #Set Active Bar to nextsong
    playlist_box.selection_set(next_one, last=None)


# Delete a song
def delete_song():
    stop()
    #delete selected song
    playlist_box.delete(ANCHOR)
    #stop music if it's playing music
    pygame.mixer.music.stop()

#delete all songs from playlist
def delete_all_songs():
    stop()
    #delete selected all song
    playlist_box.delete(0, END)
    #stop music if it's playing music
    pygame.mixer.music.stop()
    
    
#Creat Global Pause Variable 
global paused
paused = False

#Pause and Unpause The Current Song
def pause(is_paused):
    global paused
    paused = is_paused
    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        #Pause
        pygame.mixer.music.pause()
        paused = True
   
# slider to rewine and unrewine
def slide(x):
    #slider_label.config(text=f"{int(my_slider.get())} of {int(song_length)}")
    song = playlist_box.get(ACTIVE)
    song = f"C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/my hite songs/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))
    
    
# slider to increase and decrease volume
def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    
    #Get current volume
    current_volume = pygame.mixer.music.get_volume()
    # Times by 100 to make it easier to work with
    current_volume = current_volume * 100
    #slider_label.config(text=current_volume * 100)
    
    # Change volume Meter picture
    if int(current_volume) < 1:
        volume_meter.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) <= 25:
        volume_meter.config(image=vol1)
    elif int(current_volume) >= 25 and int(current_volume) <= 50:
        volume_meter.config(image=vol2)
    elif int(current_volume) >= 50 and int(current_volume) <= 75:
        volume_meter.config(image=vol3)
    elif int(current_volume) >= 75 and int(current_volume) <= 100:
        volume_meter.config(image=vol4)	

#Create a label
label = Label(root,text='Music Player',width=20,font=('arial',28,"bold"),background="#33ccff",fg="white") # set the heading
label.pack(pady=10)

# Create master frame
master_frame = Frame(root)
master_frame.pack(pady=20)


# Create playlist_box
playlist_box = Listbox(master_frame, bg="black", fg="white", width=100, selectbackground="#33ccff", selectforeground="black")
playlist_box.grid(row=0, column=0)


#create music positon slider
my_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.grid(row=1, column=0, pady=10)

#Create volume label frame
volume_frame = LabelFrame(master_frame, text="volume")
volume_frame.grid(row=0, column=1,padx=20)



#create music Volume slider
volume_slider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_slider.pack(pady=10)

#Create tempory slider label
#slider_label = Label(root, text="0")
#slider_label.pack(pady=10)

#Define Player ControlButton Images
back_btn_img = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/backward.png")
play_btn_img = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/play.png")
pause_btn_img = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/pause.png")
stop_btn_img = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/stop.png")
forward_btn_img = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/forward.png")

# Define Volume Control Images
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/volume 0.png")
vol1 = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/volume 1.png")
vol2 = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/volume 2.png")
vol3 = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/volume 3.png")
vol4 = PhotoImage(file="C:/Users/UPMANYU JHA/Desktop/PYTHON PROGRAMS/UJ MP3 Player v6/volume 4.png")

# Create Player Control frame
controls_frame = Frame(master_frame)
controls_frame.grid(row=2,column=0, pady=20)

# Create Volume Meter
volume_meter = Label(master_frame, image=vol0)
volume_meter.grid(row=1, column=1, padx=10)

#create player control buttons
back_button = Button(controls_frame, image=back_btn_img, borderwidth=0, command=previous_song)
play_button = Button(controls_frame, image=play_btn_img, borderwidth=0, command=play)
pause_button = Button(controls_frame, image=pause_btn_img, borderwidth=0, command=lambda: pause(paused))
stop_button = Button(controls_frame, image=stop_btn_img, borderwidth=0, command=stop)
forward_button = Button(controls_frame, image=forward_btn_img, borderwidth=0, command=next_song)

back_button.grid(row=0, column=0, padx=10)
play_button.grid(row=0, column=1, padx=10)
pause_button.grid(row=0, column=2, padx=10)
stop_button.grid(row=0, column=3, padx=10)
forward_button.grid(row=0, column=4, padx=10)

#Create Menu
my_menu = Menu(root)
root.config(menu=my_menu)

#Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu = add_song_menu)
add_song_menu.add_command(label="Add Song to Playlist", command=add_song)
#Add many songs to playlist_box
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_songs)

#Creat Delete song menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song from playlist", command=delete_song)
remove_song_menu.add_command(label="Delete all song from playlist", command=delete_all_songs)

# Create status bar
status_bar = Label(root, text="",  bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)














root.mainloop()
