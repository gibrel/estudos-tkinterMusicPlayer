from tkinter import *
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk


class MPlayer:

    def __init__(self):

        self.window = ThemedTk(theme="black")
        self.configure_main_window()

        self.img_add = PhotoImage(file="assets/add.png")
        self.img_remove = PhotoImage(file="assets/remove.png")
        self.img_play = PhotoImage(file="assets/play.png")
        self.img_next = PhotoImage(file="assets/next.png")
        self.img_previous = PhotoImage(file="assets/previous.png")
        self.img_pause = PhotoImage(file="assets/pause.png")

        self.list = Listbox(self.window, bg="#555555", height=16)
        self.list.pack(fill=X, padx=10, pady=10)

        self.frame = ttk.Frame(self.window)
        self.frame.pack(pady=10)

        self.remove = ttk.Button(self.frame, image=self.img_remove)
        self.remove.grid(row=0, column=0)

        self.add = ttk.Button(self.frame, image=self.img_add, command=self.import_music_folder)
        self.add.grid(row=0, column=1, padx=10)

        self.frame2 = ttk.Frame(self.window)
        self.frame2.pack(pady=10)

        self.previous = ttk.Button(self.frame2, image=self.img_previous)
        self.previous.grid(row=0, column=0)

        self.play = ttk.Button(self.frame2, image=self.img_play)
        self.play.grid(row=0, column=1, padx=5)

        self.next = ttk.Button(self.frame2, image=self.img_next)
        self.next.grid(row=0, column=2)

        self.volume = ttk.Scale(self.window)
        self.volume.pack(fill=X, pady=10, padx=10)

        self.window.mainloop()

    def configure_main_window(self):
        self.window.title("Music Player")
        window_width = 340
        window_height = 430
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.resizable(FALSE, FALSE)
        self.window.geometry(self.number_to_string(window_width) + "x" +
                             self.number_to_string(window_height) + "+" +
                             self.number_to_string((screen_width-window_width)/2) + "+" +
                             self.number_to_string((screen_height-window_height)/2))
        self.window.config(bg="#444444")

    @staticmethod
    def clear_trailing(number):
        return ('%f' % number).rstrip('0').rstrip('.')

    def number_to_string(self, number):
        return str(self.clear_trailing(number))

    def import_music_folder(self):
        folder = filedialog.askdirectory()
        print(folder)


MPlayer()
