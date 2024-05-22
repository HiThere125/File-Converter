import os
import glob
from PIL import Image
import moviepy.editor
from moviepy.editor import *
import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD

dropped_file = None
dropped_file_type = None
file_format = None

def get_dropped_file():
    return dropped_file

def get_dropped_file_type():
    return dropped_file_type

def get_file_format():
    return file_format

def take_input(event):
    global dropped_file
    global dropped_file_type
    global file_format
    window.insert("end", event.data.replace("{", "").replace("}", ""))
    dropped_file = event.data.replace("{", "").replace("}", "")
    dropped_file_type = dropped_file.split('.')[1]
    file_format = get_format(dropped_file_type)     
    l2.config(text = f"File Type: {dropped_file_type}")
    modify_options(dropped_file_type, file_format)

def get_format(file_type):
    if file_type == "mp4" or file_type == "mov":
        return "Video"
    elif file_type == "mp3" or file_type == "wav":
        return "Audio"
    elif file_type == "png" or file_type == "jpg" or file_type == "jpeg":
        return "Image"

def modify_options(dropped_file_type, file_format):
    new_list = []
    drop["menu"].delete(0, "end")    
    if file_format == "Video":
        if dropped_file_type == "mp4":
            new_list = ["Nothing", "MOV", "MP3", "FLAC", "WAV"]
        else:
            new_list = ["Nothing", "MP4", "MP3", "FLAC", "WAV"]
    elif file_format == "Audio":    
        if dropped_file_type == "mp3":
            new_list = ["Nothing", "FLAC", "WAV"]
        elif dropped_file_type == "flac":
            new_list = ["Nothing", "MP3", "WAV"]
        else:
            new_list = ["Nothing", "MP3", "FLAC"]
    elif file_format == "Image":
        if dropped_file_type == "png":
            new_list = ["Nothing", "JPG", "JPEG"]
        elif dropped_file_type == "jpg":
            new_list = ["Nothing", "PNG", "JPEG"]
        else:
            new_list = ["Nothing", "PNG", "JPG"]
    for item in new_list:
        drop["menu"].add_command(label=item, command=lambda value=item: clicked.set(value))
        
def convert_file():
    output_type = clicked.get().lower()
    output_format = get_format(output_type)
    print(f"File Format: {file_format}\nFile Path: {dropped_file}\nFile Type: {dropped_file_type}\nOutput Type: {output_type}\nOutput Format: {output_format}")
    if file_format == None or output_type == "Nothing":
        print("Either no file dropped or Nothing was selected")
    elif file_format == "Video":
        print(f"Changing video to .{output_type}")
        if output_format == "Video":
            change_video_formats(dropped_file, dropped_file_type, output_type)                
        else:
            convert_video_to_audio(dropped_file, dropped_file_type, output_type)
    elif file_format == "Audio":
        print(f"Changing audio to .{output_type}")
        change_audio_formats(dropped_file, dropped_file_type, output_type)
    else:
        print(f"Changing image to .{output_type}")
        change_image_formats(dropped_file, dropped_file_type, output_type)
    window.delete(0, 'end')

''' Checks the number of files of a specific type using os.listdir()
    @Params:    path            |   String  |   Path to the folder to be searched
                file_type       |   String  |   Type of file to search for
    @Returns:   number_of_type  |   Int     |   Number of files of specific type
                number_of_files |   Int     |   Number of files total in the folder'''
def check_file_extensions(path):
    number_of_files = [0]*18
    total_files = 0
    files = ["exe", "ini", "png", "jpg", "jpeg", "mp4", "mp3", "mov", "ppt", "csv", "pdf", "twbx", "cfg", "bat", "py", "sln", "pyproj", "misc"]   
    file_list = os.listdir(path)
    for fil in file_list:
        print(fil)
        split_fil = fil.split(".")     
        extension = split_fil[len(split_fil)-1]
        number_of_files[files.index(extension)] = number_of_files[files.index(extension)] + 1
        total_files = total_files + 1
    print(f"There are {total_files} files in this folder")         
    for ext in files:
        num_of_ext = number_of_files[files.index(ext)]       
        if num_of_ext > 0:
            print(f"{num_of_ext} .{ext} files")

''' Changes a single Video file's format using Moviepy
    @Params:    file_location   |   String  |   Path to the Video file
                input_type      |   String  |   Video file's type
                output_type     |   String  |   File type to convert to
    @Returns:   None'''
def change_video_formats(file_location, input_type, output_type):
    video = moviepy.editor.VideoFileClip(file_location)
    new_file_name = file_location.replace(input_type, output_type)
    video.write_videofile(new_file_name, codec = "libx264")

''' Converts a single Video file to an Audio file using Moviepy
    @Params:    file_location   |   String  |   Path to the Video file
                input_type      |   String  |   Video file's type
                output_type     |   String  |   File type to convert to
    @Returns:   None'''
def convert_video_to_audio(file_location, input_type, output_type):
    video = moviepy.editor.VideoFileClip(file_location)
    audio = video.audio
    new_file_name = file_location.replace(input_type, output_type)
    audio.write_audiofile(new_file_name, bitrate = '320k')

''' Changes a single Audio file's format using Moviepy
    @Params:    file_location   |   String  |   Path to the Audio file
                input_type      |   String  |   Audio file's type
                output_type     |   String  |   File type to convert to
    @Returns:   None'''
def change_audio_formats(file_location, input_type, output_type):
    audio = AudioFileClip(file_location)
    new_file_name = file_location.replace(input_type, output_type)
    audio.write_audiofile(new_file_name, bitrate = '320k')

''' Changes a single Image file's format using Pillow
    @Params:    file_location   |   String  |   Path to the Image file
                input_type      |   String  |   Image file's type
                output_type     |   String  |   File type to convert to
    @Returns:   None'''
def change_image_formats(file_location, input_type, output_type):
    img = Image.open(file_location)
    new_file_name = file_location.replace(input_type, output_type)
    img.save(new_file_name)

def mass_convert_images(path, file_type):
    print(f"Converting Images at {path} to {file_type}")
    filenames_list = []
    if file_type == "png":
        filenames_list = filenames_list + glob.glob(os.path.join(path, "*.jpeg"))
        filenames_list = filenames_list + glob.glob(os.path.join(path, "*.jpg"))
    elif file_type == "jpeg":
        filenames_list = filenames_list + glob.glob(os.path.join(path, "*.jpg"))
        filenames_list = filenames_list + glob.glob(os.path.join(path, "*.png"))
    elif file_type == "jpg":
        filenames_list = filenames_list + glob.glob(os.path.join(path, "*.jpeg"))
        filenames_list = filenames_list + glob.glob(os.path.join(path, "*.png"))
    print("Compiled File List")  
    if filenames_list != 0:
        for fil in range(0,len(filenames_list)):
            img = Image.open(filenames_list[fil])
            new_image = filenames_list[fil].split(".")[0]
            img.save(f"{new_image}.{file_type}")
            print(f"Finished Converting Image {fil} / {len(filenames_list)}")
    print(f"Finished Converting all Images to {file_type}")            


''' Removes the files of a specific type using os.remove()
    @Params:    path            |   String  |   Path to the folder to be searched
                file_type       |   String  |   Type of file to search for
    @Returns:   None'''
def remove_files_with_extension(path, file_type):
    file_list = glob.glob(os.path.join(path, file_type))
    for fil in file_list:
        os.remove(fil)
    

root = TkinterDnD.Tk()  # notice - use this instead of tk.Tk()
root.geometry("500x300")
window = tk.Listbox(root)
l1 = tk.Label(text = "Drag Files Below")
l2 = tk.Label(text = "File Type:")
button1 = tk.Button( root , text = "Convert" , command = lambda: convert_file())
options = ["Nothing", "MP4", "MOV", "MP3", "FLAC", "WAV", "PNG", "JPG", "JPEG"]
clicked = tk.StringVar()       # datatype of menu text
clicked.set("Nothing")      # initial menu text
drop = tk.OptionMenu( root , clicked , *options )
window.drop_target_register(DND_FILES)
window.dnd_bind('<<Drop>>', take_input)


l1.pack()
window.pack()
l2.pack()
drop.pack()
button1.pack()
root.mainloop()