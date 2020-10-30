# Importing Required Modules & libraries
import tkinter
from tkinter import *
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter.filedialog import askdirectory
import pygame
import os
import datetime
import mutagen
from mutagen.mp3 import MP3

# Defining MusicPlayer Class
class MusicPlayer:
    def __init__(self, root):
        self.root = root
        # Title of the window
        self.root.title("Music Player")
        self.root.configure(bg="lightskyblue3")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        #initiating pygame Mixer
        pygame.init()
        pygame.mixer.init()
        #------------------------------------------------------------------------------------
        #IMAGE REGISTER --------> IMAGE SIZING
        #global volupimg, voldownimg, playimg, pauseimg, unpauseimg, stopimg#, gifimg, gifimgdark
        self.playimg = PhotoImage(file='play-button (1).png')
        self.playimg = self.playimg.subsample(10,10)

        self.pauseimg = PhotoImage(file='pause-button1.png')
        self.pauseimg = self.pauseimg.subsample(8,8)

        self.volupimg = PhotoImage(file='volume-up.png')
        self.volupimg = self.volupimg.subsample(25,25)

        self.voldownimg = PhotoImage(file='low-volume1.png')
        self.voldownimg = self.voldownimg.subsample(20,20)

        self.unpauseimg = PhotoImage(file='resume-button-1.png')
        self.unpauseimg = self.unpauseimg.subsample(15,15)

        self.stopimg = PhotoImage(file='stopbutton.png')
        self.stopimg = self.stopimg.subsample(20,20)

        self.gifimg = PhotoImage(file= "music.gif")
        self.gifimg = self.gifimg.subsample(1,1)

        self.rootimg = Label(self.root, image=self.gifimg, compound=CENTER)
        self.rootimg.place(x=315, y=10, width=675, height=490)

        self.imgdark = PhotoImage(file="cat.gif")
        self.imgdark = self.imgdark.subsample(1, 1)

        self.imglight = PhotoImage(file="house-music.png")
        self.imglight = self.imglight.subsample(1, 1)

        #Declaring Track variable
        self.track = StringVar()
        # Declaring Status Variable
        self.status = StringVar()


        # Creating Button Frame
        self.buttonframe = LabelFrame(self.root, font=("times new roman", 15, "bold"), bg="ivory2", fg="white", bd=5, relief=FLAT)
        self.buttonframe.place(x=10, y=510, width=980, height=185)

        # Inserting Status Label
        self.trackstatus = Label(self.buttonframe, textvariable=self.status, font=("times new roman", 12, "bold"), bg="ivory2",fg="black")
        self.trackstatus.place(x=10, y=160, height=15)

        # Inserting Play Button
        self.playbtn = Button(self.buttonframe, command=self.playsong, font=("times new roman", 16, "bold"), bg="ivory2", relief=FLAT,image=self.playimg, compound=CENTER)
        self.playbtn.place(x=450, y=50)

        # Inserting Pause Button
        self.pausebtn = Button(self.buttonframe, command=self.pausesong, bg="ivory2", relief=FLAT, activebackground="ivory2",image=self.pauseimg, compound=CENTER)
        self.pausebtn.place(x=390, y=60)

        # Inserting Unpause Button
        self.unpausebtn = Button(self.buttonframe, command=self.unpausesong, bg="ivory2", relief=FLAT, activebackground="ivory2",image=self.unpauseimg, compound=CENTER)
        self.unpausebtn.place(x=390, y=60)
        self.unpausebtn.place_forget()

        # Inserting Stop Button
        self.stopbtn = Button(self.buttonframe, command=self.stopsong, bg="ivory2", relief=FLAT, activebackground="ivory2", image=self.stopimg, compound=CENTER)
        self.stopbtn.place(x=530, y=60)

        # Adding volume buttons
        self.vol_upbtn = Button(self.buttonframe, command=self.volumeup, bg="ivory2", activebackground='ivory2', fg="white", relief=FLAT, image=self.volupimg, compound=CENTER)
        self.vol_upbtn.place(x=870, y=73, width=20, height=20)

        self.vol_downbtn = Button(self.buttonframe, command=self.volumedown, bg="ivory2", activebackground='ivory2',fg="white", relief=FLAT, image=self.voldownimg, compound=CENTER)
        self.vol_downbtn.place(x=700, y=73, width=20, height=20)

        # Creating Playlist Frame
        self.songsframe = LabelFrame(self.root, font=("times new roman", 15, "bold"), bg="lightgrey",fg="white", bd=5, relief=FLAT)
        self.songsframe.place(x=10, y=10, width=300, height=480)

        # Inserting scrollbar
        scroly = Scrollbar(self.songsframe, orient=VERTICAL)

        # Inserting Playlist listbox
        self.playlist = Listbox(self.songsframe, yscrollcommand=scroly.set, selectbackground="khaki", selectmode=SINGLE,font=("times new roman", 12, "bold"), bg="ghost white", fg="black", relief=FLAT)

        # Applying Scrollbar to listbox
        scroly.pack(side=RIGHT, fill=Y)
        scroly.config(command=self.playlist.yview)
        self.playlist.place(x=1, y=1, width=268, height=475)
        self.totalsonglength = 0
        #self.count = 0
        #self.text = ''

        # adding song label in trackframe
        self.songlabel = Label(self.buttonframe, textvariable=self.track, bg="lightsteelblue2", fg="black",font=('arial', 10, 'bold'), anchor=W)
        self.songlabel.place(x=1, y=2, height=15)

        self.ProgressbarLabel=Label(self.buttonframe, text='', bg='snow')
        self.ProgressbarLabel.place(x=700,y=50,height=20,width=190)

        self.ProgressbarVolume = Progressbar(self.ProgressbarLabel, orient=HORIZONTAL, mode='determinate', value=0, length=190)
        self.ProgressbarVolume.place(x=0, y=0,width=190, height=20)

        self.ProgressbarVolumeLabel = Label(self.ProgressbarLabel, text='0%',bg='ivory3')
        self.ProgressbarVolumeLabel.place(x=90, y=0, width=20,height=20)

        self.ProgressbarAudioTrack = Progressbar(self.root, orient=HORIZONTAL, mode='determinate', value=0, length=950)
        self.ProgressbarAudioTrack.place(x=40, y=500,height=10)

        self.ProgressbarAudioTrackLabel1 = Label(self.root, text='0:00:00', bg='ivory2', font=('arial', 7))
        self.ProgressbarAudioTrackLabel1.place(x=10, y=500, height=10, width=30)

        self.ProgressbarAudioTrackLabel2 = Label(self.root, text='0:00:00', bg='ivory2', font=('arial', 7))
        self.ProgressbarAudioTrackLabel2.place(x=960, y=500, height=10, width=30)

        self.menubuttons()
    #-------------------------------F U N C T I O N S----------------------------------

    def volumeup(self):
        vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(vol + 0.05)
        self.ProgressbarVolumeLabel.configure(text='{}%'.format(int(pygame.mixer.music.get_volume()*100)))
        self.ProgressbarVolume['value'] = pygame.mixer.music.get_volume()*100

    def volumedown(self):
        vol = pygame.mixer.music.get_volume()
        pygame.mixer.music.set_volume(vol - 0.05)
        self.ProgressbarVolumeLabel.configure(text='{}%'.format(int(pygame.mixer.music.get_volume() * 100)))
        self.ProgressbarVolume['value'] = pygame.mixer.music.get_volume() * 100

    def playsong(self):
        # Displaying Selected Song title
        ad = self.playlist.get(ACTIVE)
        self.track.set(ad)
        self.status.set("-Playing")
        # Loading Selected Song
        pygame.mixer.music.load(ad)
        # Playing Selected Song
        pygame.mixer.music.set_volume(0.4)
        self.ProgressbarVolume['value'] = 40
        self.ProgressbarVolumeLabel['text']= '40%'
        pygame.mixer.music.play()
        # Getting total song length of song which is being played
        self.song = MP3(ad)
        self.totalsonglength = int(self.song.info.length)
        self.ProgressbarAudioTrack['maximum'] = self.totalsonglength
        self.ProgressbarAudioTrackLabel2.configure(text='{}'.format(str(datetime.timedelta(seconds=self.totalsonglength))))

        self.Progressbarmusictick()

    def Progressbarmusictick(self):
        self.currentsonglength = pygame.mixer.music.get_pos() // 1000
        self.ProgressbarAudioTrack['value'] = self.currentsonglength
        self.ProgressbarAudioTrackLabel1.configure(text='{}'.format(str(datetime.timedelta(seconds=self.currentsonglength))))
        self.ProgressbarAudioTrack.after(2, self.Progressbarmusictick)

    def stopsong(self):
        self.status.set("-Stopped")
        pygame.mixer.music.stop()

    def pausesong(self):
        pygame.mixer.music.pause()
        self.pausebtn.place_forget()
        self.status.set("-Paused")
        self.unpausebtn.place(x=390, y=60)

    def unpausesong(self):
        self.unpausebtn.place_forget()
        self.pausebtn.place(x=390, y=60)
        self.status.set("-Playing")
        pygame.mixer.music.unpause()

    def directorychooser(self):
        self.realnames = []
        try:
            directory = askdirectory()  # ask user to select a folder
            os.chdir(directory)
            for track in os.listdir(directory):
               if track.endswith(".mp3"):
                    self.playlist.insert(END, track)
        except OSError:
            messagebox.showerror("File Not Found","Please select the File")

    def default(self):
        self.root.configure(bg="lightskyblue3")
        self.buttonframe.configure(bg="ivory2")
        self.songsframe.configure(bg="lightgrey")
        self.rootimg = Label(self.root, image=self.gifimg, compound=CENTER)
        self.rootimg.place(x=315, y=10, width=675, height=490)
        self.stopbtn.configure(bg="ivory2")
        self.playbtn.configure(bg="ivory2")
        self.pausebtn.configure(bg="ivory2")
        self.unpausebtn.configure(bg="ivory2")
        self.vol_downbtn.configure(bg="ivory2")
        self.vol_upbtn.configure(bg="ivory2")
        self.songlabel.configure(bg="lightsteelblue2")
        self.trackstatus.configure(bg="ivory2")
        self.playlist.configure(bg="ghost white",fg="black")

    def theme1(self):
        self.root.configure(bg="purple4")
        self.buttonframe.configure(bg="medium purple4")
        self.songsframe.configure(bg="black")
        rootgif1 = Label(self.root, image=self.imgdark, compound=CENTER)
        rootgif1.place(x=315, y=10, width=675, height=490)
        self.stopbtn.configure(bg="medium purple4")
        self.playbtn.configure(bg="medium purple4")
        self.pausebtn.configure(bg="medium purple4")
        self.unpausebtn.configure(bg="medium purple4")
        self.vol_downbtn.configure(bg="medium purple4")
        self.vol_upbtn.configure(bg="medium purple4")
        self.songlabel.configure(bg="medium purple4")
        self.trackstatus.configure(bg="medium purple4")
        self.playlist.configure(bg="snow", fg="black")

    def theme2(self):
        self.root.configure(bg="snow")
        self.buttonframe.configure(bg="lavender blush")
        self.songsframe.configure(bg="antique white")
        rootgif2 = Label(self.root, image=self.imglight, compound=CENTER)
        rootgif2.place(x=315, y=10, width=675, height=490)
        self.stopbtn.configure(bg="lavender blush")
        self.playbtn.configure(bg="lavender blush")
        self.pausebtn.configure(bg="lavender blush")
        self.unpausebtn.configure(bg="lavender blush")
        self.vol_downbtn.configure(bg="lavender blush")
        self.vol_upbtn.configure(bg="lavender blush")
        self.songlabel.configure(bg="lavender blush")
        self.trackstatus.configure(bg="lavender blush")
        self.playlist.configure(bg="lavender blush", fg="black")

    def menubuttons(self):
        menubar = Menu(self.root)
        menu_1 = Menu(self.root)
        menu_1.add_command(label="Open", command=self.directorychooser)
        menu_1.add_separator()
        menu_1.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=menu_1)

        menu_2 = Menu(self.root)
        menu_2.add_radiobutton(label="Dark theme", command=self.theme1)
        menu_2.add_radiobutton(label="Light theme", command=self.theme2)
        menu_2.add_radiobutton(label="Default theme", command=self.default)
        menubar.add_cascade(label="Theme", menu=menu_2)
        self.root.config(menu=menubar)


root = Tk()
obj = MusicPlayer(root)
obj.directorychooser()
root.mainloop()