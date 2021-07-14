from tkinter import*
from tkinter import filedialog
import pygame
from pygame import mixer
from mutagen.mp3 import MP3
import time

root=Tk()

root.title("Mp3 Player")
root.iconbitmap(r'C:\Users\user\OneDrive\Desktop\Python Projects\music.ico')
root.geometry('500x350')



#initialize pygame mixer
pygame.mixer.init()

#length of song played
def play_time():
    current_time=pygame.mixer.music.get_pos()/1000
    
    #convert in time format
    conv_curr_time=time.strftime('%M:%S',time.gmtime(current_time))

    #Get the current song
    cur_song=song_box.curselection()
    song=song_box.get(cur_song)
    song=f'C:/Users/user/OneDrive/Desktop/Python Projects/music{song}'
    
    #get song length
    song_mut=MP3(song)
    song_len=song_mut.info.length

    conv_curr_len=time.strftime('%M:%S',time.gmtime(song_len))

    #Output time to status bar
    status_bar.config(text=f'Time Elapsed: {conv_curr_time} of {conv_curr_len}')
    status_bar.after(1000,play_time)

#Add song function
def add_song():
    song=filedialog.askopenfilename(initialdir='music',title="Choose a song",filetypes=(("mp3 Files","*.mp3"),))
    song=song.replace(r"C:/Users/user/OneDrive/Desktop/Python Projects/music","")
    song_box.insert(END,song)

#Add many song to Playlist
def add_many_song():
    songs=filedialog.askopenfilenames(initialdir='music',title="Choose a song",filetypes=(("mp3 Files","*.mp3"),))
    for song in songs:
        song=song.replace(r"C:/Users/user/OneDrive/Desktop/Python Projects/music","")
        song_box.insert(END,song)


#Create Playlist Box
song_box=Listbox(root,bg="black",fg="green",width=80,selectbackground="gray",selectforeground="black")
song_box.pack(pady=20)

#Define Player Control Buttons
back_btn_img=PhotoImage(file=r"C:\Users\user\OneDrive\Desktop\Python Projects\backward.png")
forward_btn_img=PhotoImage(file=r"C:\Users\user\OneDrive\Desktop\Python Projects\forward.png")
play_btn_img=PhotoImage(file=r"C:\Users\user\OneDrive\Desktop\Python Projects\play.png")
pause_btn_img=PhotoImage(file=r"C:\Users\user\OneDrive\Desktop\Python Projects\pause.png")
stop_btn_img=PhotoImage(file=r"C:\Users\user\OneDrive\Desktop\Python Projects\stop.png")

#Create Player control Frames
controls_frame=Frame(root)
controls_frame.pack()


# play Selected Song
def play():
    song=song_box.get(ACTIVE)
    song=f'C:/Users/user/OneDrive/Desktop/Python Projects/music{song}'
    mixer.music.load(song)
    mixer.music.play(loops=0)
    play_time()

#Stop playing current song
def stop():
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)

global Paused
Paused=False
#pause and unpause the current song
def pause(is_paused):
    global Paused
    Paused=is_paused
    if Paused:
        pygame.mixer.music.unpause()
        Paused=FALSE
    else:
        pygame.mixer.music.pause()
        Paused=TRUE

#Play next song in the playlist
def next_song():
    next_one=song_box.curselection()
    next_one=next_one[0]+1
    song=song_box.get(next_one)
    song=f'C:/Users/user/OneDrive/Desktop/Python Projects/music{song}'
    mixer.music.load(song)
    mixer.music.play(loops=0)
    
    #clear the active bar in playlist
    song_box.selection_clear(0,END)
    
    #Activate new song bar
    song_box.activate(next_one)

    #set active bar to next song
    song_box.selection_set(next_one,last=None)
    
#Play previous song in the playlist
def previous_song():
    next_one=song_box.curselection()
    next_one=next_one[0]-1
    song=song_box.get(next_one)
    song=f'C:/Users/user/OneDrive/Desktop/Python Projects/music{song}'
    mixer.music.load(song)
    mixer.music.play(loops=0)
    
    #clear the active bar in playlist
    song_box.selection_clear(0,END)
    
    #Activate new song bar
    song_box.activate(next_one)

    #set active bar to next song
    song_box.selection_set(next_one,last=None)

#delete a song from the playlist
def delete_song():
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

#Create Player control Buttons
back_button=Button(controls_frame,image=back_btn_img,borderwidth=0,command=previous_song)
forward_button=Button(controls_frame,image=forward_btn_img,borderwidth=0,command=next_song)
play_button=Button(controls_frame,image=play_btn_img,borderwidth=0,command=play)
pause_button=Button(controls_frame,image=pause_btn_img,borderwidth=0,command=lambda:pause(Paused))
stop_button=Button(controls_frame,image=stop_btn_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=10)
forward_button.grid(row=0,column=1,padx=10)
play_button.grid(row=0,column=2,padx=10)
pause_button.grid(row=0,column=3,padx=10)
stop_button.grid(row=0,column=4,padx=10)

# Create Menu
my_menu=Menu(root)
root.config(menu=my_menu)

# Add song Menu
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Add Songs",menu=add_song_menu)
add_song_menu.add_command(label="Add one Song to Playlist",command=add_song)

#Add many song to menu
add_song_menu.add_command(label="Add many Song to Playlist",command=add_many_song)

#Delete song menu
remove_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Remove song",menu=remove_song_menu)
remove_song_menu.add_command(label="Delete a song",command=delete_song)

#Create Status Bar
status_bar=Label(root,text='',bd=1,relief=GROOVE,anchor=E)
status_bar.pack(fill=X,side=BOTTOM,ipady=5)



root.mainloop()