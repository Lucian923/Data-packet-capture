import tkinter
from tkinter import *
from tkinter import messagebox
from project_back_2 import *
import re

root = Tk()
root.iconbitmap("packets.ico")

root.title("Packets capture")


# function that enable "save" and "statistics" buttons
def enable():
    save_button["state"] = tkinter.NORMAL
    statistics_button["state"] = tkinter.NORMAL
    capture_done_label["text"] = "Capture done!"


# function that enable/disable entries of check buttons
def check_entries():
    if var1.get() == 1:
        count_entry["state"] = tkinter.NORMAL
        time_entry.delete(0, "end")
        time_entry["state"] = tkinter.DISABLED

    if var1.get() == 2:
        time_entry["state"] = tkinter.NORMAL
        count_entry.delete(0, "end")
        count_entry["state"] = tkinter.DISABLED

    if var1.get() == 0:
        count_entry.delete(0, "end")
        count_entry["state"] = tkinter.DISABLED
        time_entry.delete(0, "end")
        time_entry["state"] = tkinter.DISABLED


# function for calling the capture method with ending argument
def ending_filter():
    pattern = r'[1-9]'
    if count_entry.get() != "":
        if re.match(pattern, count_entry.get()):
            arg1 = int(count_entry.get())
            arg2 = None
            Capture.get_instance()
            Capture._instance.get_capture(capture_filter.get(), arg1, arg2)
            enable()
        else:
            messagebox.showinfo("Info", "Please enter a valid packets number")
    elif time_entry.get() != "":
        if re.match(pattern, time_entry.get()):
            arg1 = 0
            arg2 = int(time_entry.get())
            Capture.get_instance()
            Capture._instance.get_capture(capture_filter.get(), arg1, arg2)
            enable()
        else:
            messagebox.showinfo("Info", "Please enter a valid seconds number")
    else:
        messagebox.showinfo("Info", "One capture ending mode should be selected and filled")


# function that calls the method for saving the json file
def save_function():
    Capture.json_file(save_path_entry.get())
    if Capture.json_file(save_path_entry.get()):
        saved_label["text"] = "File saved"
    else:
        messagebox.showinfo("Info", "Invalid path or filename")

# creating and packing the frames
frame1 = LabelFrame(root)
frame1.pack(padx=10, pady=10)
frame2 = LabelFrame(root)
frame2.pack(padx=10, pady=10)
frame3 = LabelFrame(root)
frame3.pack(padx=10, pady=10)

# creating labels
#   frame 1
filter_label = Label(frame1, text="Enter filter (optional)")
filter_label.grid(row=0, column=0)

capture_end = Label(frame1, text="Choose capture ending mode:")
capture_end.grid(row=1, column=0)

capture_done_label = Label(frame1, text="")
capture_done_label.grid(row=4, column=1, columnspan=2)

#   frame 2
save_path_label = Label(frame2, text="Enter file path:")
save_path_label.grid(row=0, column=0)

saved_label = Label(frame2, text="")
saved_label.grid(row=2, column=1, columnspan=2)

# creating entries
#    frame 1
capture_filter = Entry(frame1, width=10)
capture_filter.grid(row=0, column=1)

count_entry = Entry(frame1, width=10, state=tkinter.DISABLED)
count_entry.grid(row=2, column=1)

time_entry = Entry(frame1, width=10, state=tkinter.DISABLED)
time_entry.grid(row=2, column=2)

#   frame 2
save_path_entry = Entry(frame2, width=50)
save_path_entry.grid(row=0, column=1, columnspan=2, sticky="E")

# creating buttons
#   frame 1
capture_button = Button(frame1, command=lambda: ending_filter(), text="Capture", height=2, width=7)
capture_button.grid(row=3, column=1, columnspan=2)

var1 = IntVar()
checkbox1 = Checkbutton(frame1, text="By packets number", variable=var1, onvalue=1, command=check_entries)
checkbox1.grid(row=1, column=1)

checkbox2 = Checkbutton(frame1, text="By seconds", variable=var1, onvalue=2, command=check_entries)
checkbox2.grid(row=1, column=2)
#   frame 2
save_button = Button(frame2, command=save_function, text="Save as JSON", state=tkinter.DISABLED)
save_button.grid(row=1, column=1, columnspan=2)

#   frame 3
statistics_button = Button(frame3, command=Capture.plot, text="Show statistics", state=tkinter.DISABLED)
statistics_button.grid(row=0, column=1)

root.mainloop()
