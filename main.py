from tkinter import *
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from pygame import mixer, error
import os
from enum import Enum, auto


class PlayStatus(Enum):
    STOPPED = auto(),
    PLAYING = auto(),
    PAUSED = auto


class MPlayer:

    def __init__(self):

        mixer.init()

        self.window = ThemedTk(theme="black")
        self.configure_main_window()

        self.img_add = PhotoImage(file="assets/add.png")
        self.img_remove = PhotoImage(file="assets/remove.png")
        self.img_clear = PhotoImage(file="assets/clear.png")
        self.img_play = PhotoImage(file="assets/play.png")
        self.img_next = PhotoImage(file="assets/next.png")
        self.img_previous = PhotoImage(file="assets/previous.png")
        self.img_pause = PhotoImage(file="assets/pause.png")

        self.status = PlayStatus.STOPPED

        self.folder = ""

        self.list = Listbox(self.window, bg="#555555", height=16, fg="gray", font="Comic 12",
                            selectbackground="#6868e6")
        self.list.pack(fill=X, padx=10, pady=10)

        self.frame = ttk.Frame(self.window)
        self.frame.pack(pady=10)

        self.remove = ttk.Button(self.frame, image=self.img_remove, command=self.remove_music_file)
        self.remove.grid(row=0, column=0)

        self.add = ttk.Button(self.frame, image=self.img_add, command=self.import_music_folder)
        self.add.grid(row=0, column=1, padx=10)

        self.clear = ttk.Button(self.frame, image=self.img_clear, command=self.delete_music_list)
        self.clear.grid(row=0, column=3)

        self.frame2 = ttk.Frame(self.window)
        self.frame2.pack(pady=10)

        self.previous = ttk.Button(self.frame2, image=self.img_previous, command=self.play_previous_music)
        self.previous.grid(row=0, column=0)

        self.play = ttk.Button(self.frame2, image=self.img_play, command=self.play_selected_music)
        self.play.grid(row=0, column=1, padx=5)

        self.next = ttk.Button(self.frame2, image=self.img_next, command=self.play_next_music)
        self.next.grid(row=0, column=2)

        self.volume = ttk.Scale(self.window, from_=0, to=1, command=self.set_volume)
        self.volume.pack(fill=X, pady=10, padx=10)
        self.volume.set(0.5)

        self.window.mainloop()

    def configure_main_window(self):
        self.window.title("Music Player")
        window_width = 340
        window_height = 480
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
        try:
            self.folder = filedialog.askdirectory()
            if not self.folder or self.folder.strip() == "" or not os.path.exists(self.folder):
                raise TypeError("Invalid folder path.")
            files = os.listdir(self.folder)
            for file in files:
                self.list.insert(END, str(file))
            self.list.activate(0)
            self.list.select_set(0)
        except TypeError:
            self.send_message("ERROR", "Invalid folder provided.", "Oh Chesus!")

    def delete_music_list(self):
        self.list.delete(0, END)

    def send_message(self, message_type, message_text, message_button):
        window = Toplevel()
        window.title(message_type)
        window_width = 300
        window_height = 200
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window.resizable(FALSE, FALSE)
        window.geometry(self.number_to_string(window_width) + "x" +
                        self.number_to_string(window_height) + "+" +
                        self.number_to_string((screen_width - window_width) / 2) + "+" +
                        self.number_to_string((screen_height - window_height) / 2))

        Label(window, text=message_text, pady=30, font="Comic 12").pack(expand=YES)

        Button(window, text=message_button, command=window.destroy).pack(pady=30)

    def remove_music_file(self):
        current = self.list.curselection()[0]
        self.list.delete(ACTIVE)
        if self.list.size() > 0:
            if current >= self.list.size():
                current = 0
            self.list.select_clear(0, END)
            self.list.activate(current)
            self.list.select_set(current)

    def play_next_music(self):
        self.navigate_list(True)

    def play_previous_music(self):
        self.navigate_list(False)

    def navigate_list(self, forward):
        try:
            current = self.list.curselection()[0]
            if forward:
                if self.list.size() <= current + 1:
                    current = 0
                else:
                    current += 1
            else:
                if 0 > current - 1:
                    current = self.list.size() - 1
                else:
                    current -= 1
            self.list.select_clear(0, END)
            self.list.activate(current)
            self.list.select_set(current)
            self.list.yview(current)
            self.status = PlayStatus.STOPPED
            self.play_selected_music()
        except IndexError:
            self.send_message("ERROR", "Please add some music first.", "OOOOPS!")

    def play_selected_music(self):
        file_path = ""
        try:
            if self.status == PlayStatus.STOPPED:
                file_path = str(self.folder) + "/" + str(self.list.get(ACTIVE))
                # print("Playing: " + file_path)
                mixer.music.load(file_path)
                mixer.music.play()
                self.status = PlayStatus.PLAYING
                self.play.config(image=self.img_pause)
            elif self.status == PlayStatus.PLAYING:
                mixer.music.pause()
                self.status = PlayStatus.PAUSED
                self.play.config(image=self.img_play)
            elif self.status == PlayStatus.PAUSED:
                mixer.music.unpause()
                self.status = PlayStatus.PLAYING
                self.play.config(image=self.img_pause)
        except error:
            self.send_message("ERROR", "Could not play file:\r\n" + file_path, "OKAY...")

    def set_volume(self, var):
        mixer.music.set_volume(self.volume.get())


MPlayer()
