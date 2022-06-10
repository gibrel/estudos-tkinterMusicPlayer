from tkinter import *
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk
from pygame import mixer, error
import os


class MPlayer:

    def __init__(self):

        mixer.init()

        self.window = ThemedTk(theme="black")
        self.configure_main_window()

        self.img_add = PhotoImage(file="assets/add.png")
        self.img_remove = PhotoImage(file="assets/remove.png")
        self.img_play = PhotoImage(file="assets/play.png")
        self.img_next = PhotoImage(file="assets/next.png")
        self.img_previous = PhotoImage(file="assets/previous.png")
        self.img_pause = PhotoImage(file="assets/pause.png")

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

        self.frame2 = ttk.Frame(self.window)
        self.frame2.pack(pady=10)

        self.previous = ttk.Button(self.frame2, image=self.img_previous, command=self.play_previous_music)
        self.previous.grid(row=0, column=0)

        self.play = ttk.Button(self.frame2, image=self.img_play, command=self.play_selected_music)
        self.play.grid(row=0, column=1, padx=5)

        self.next = ttk.Button(self.frame2, image=self.img_next, command=self.play_next_music)
        self.next.grid(row=0, column=2)

        self.volume = ttk.Scale(self.window)
        self.volume.pack(fill=X, pady=10, padx=10)

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
            self.send_message("ERROR", "Invalid folder provided.")

    @staticmethod
    def send_message(message_type, message_text):
        window = Toplevel()
        window.title(message_type)
        window.resizable(FALSE, FALSE)
        window.geometry("300x200+300+200")

        Label(window, text=message_text, pady=30, font="Comic 12").pack()

        Button(window, text="OK", command=window.destroy)

    def remove_music_file(self):
        self.list.delete(ACTIVE)

    def play_next_music(self):
        self.navigate_list(True)

    def play_previous_music(self):
        self.navigate_list(False)

    def navigate_list(self, forward):
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
        self.play_selected_music()

    def play_selected_music(self):
        try:
            file_path = str(self.folder) + "/" + str(self.list.get(ACTIVE))
            mixer.music.load(file_path)
            mixer.music.play()
        except error:
            self.send_message("ERROR", "Could not play file:\r\n" + file_path)


MPlayer()
