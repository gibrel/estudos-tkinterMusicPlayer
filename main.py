from tkinter import *


class MPlayer:

    def __init__(self):

        self.window = Tk()
        self.window.title("Music Player")
        self.window.resizable(FALSE, FALSE)
        self.window.geometry("300x400+800+300")
        self.window.mainloop()


MPlayer()
