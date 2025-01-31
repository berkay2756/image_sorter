import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS

# Supported file formats
IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png')
VIDEO_EXTENSIONS = ('.mp4', '.mov')
OTHER_EXTENSIONS = ('.aae',)  # Add more if needed
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS + VIDEO_EXTENSIONS + OTHER_EXTENSIONS

# Language Dictionary
LANGUAGES = {
    "English": {
        "title": "Photo Sorter",
        "source": "Source Folder:",
        "destination": "Destination Folder:",
        "browse": "Browse",
        "include_subfolders": "Include Subfolders",
        "sort_files": "Sort Files",
        "sorting_started": "Sorting started...",
        "sorting_completed": "Sorting completed!",
        "warning": "Warning",
        "select_folders": "Please select both source and destination folders!",
        "success": "Success",
    },
    "Türkçe": {
        "title": "Fotoğraf Düzenleyici",
        "source": "Kaynak Klasör:",
        "destination": "Hedef Klasör:",
        "browse": "Gözat",
        "include_subfolders": "Alt Klasörleri Dahil Et",
        "sort_files": "Dosyaları Sırala",
        "sorting_started": "Sıralama başladı...",
        "sorting_completed": "Sıralama tamamlandı!",
        "warning": "Uyarı",
        "select_folders": "Lütfen kaynak ve hedef klasörleri seçin!",
        "success": "Başarılı",
    }
}

# Default Language
current_lang = "English"

def get_translation(key):
    """
    Function for fetching the 
    translation for the given key.
    """

    return LANGUAGES[current_lang].get(key, key)

def change_language(selection):
    """
    Function for changing the language.
    """

    global current_lang
    current_lang = selection
    root.title(get_translation("title"))
    lbl_source.config(text=get_translation("source"))
    lbl_destination.config(text=get_translation("destination"))
    btn_source.config(text=get_translation("browse"))
    btn_dest.config(text=get_translation("browse"))
    chk_recursive.config(text=get_translation("include_subfolders"))
    btn_sort.config(text=get_translation("sort_files"))

def get_date_taken(image_path):
    """
    Get the date a photo was taken (from EXIF) 
    or fallback to file modified time.
    """

    if image_path.lower().endswith(IMAGE_EXTENSIONS):
        try:
            image = Image.open(image_path)
            exif_data = image._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == "DateTimeOriginal":
                        return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
        except Exception as e:
            log_message(f"EXIF data not found for {image_path}: {e}")

    mod_time = os.path.getmtime(image_path)
    return datetime.fromtimestamp(mod_time)

def get_unique_filename(target_folder, filename):
    """
    Ensure the filename is unique in the 
    target folder by appending a number if needed.
    """

    base_name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(target_folder, new_filename)):
        new_filename = f"{base_name}_{counter}{ext}"
        counter += 1

    return new_filename

def sort_files_by_date():
    """
    Sort files into year-month 
    folders based on user input.
    """

    source_folder = entry_source.get().strip()
    dest_folder = entry_dest.get().strip()
    include_subfolders = var_recursive.get()

    if not source_folder or not dest_folder:
        messagebox.showwarning(get_translation("warning"), get_translation("select_folders"))
        return

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    log_message(get_translation("sorting_started"))

    if include_subfolders:
        for root, _, files in os.walk(source_folder):
            for filename in files:
                process_file(root, filename, dest_folder)
    else:
        for filename in os.listdir(source_folder):
            file_path = os.path.join(source_folder, filename)
            if os.path.isfile(file_path):
                process_file(source_folder, filename, dest_folder)

    messagebox.showinfo(get_translation("success"), get_translation("sorting_completed"))
    log_message(get_translation("sorting_completed"))

def process_file(folder, filename, dest_folder):
    """
    Process and move a single file 
    based on its date.
    """

    file_path = os.path.join(folder, filename)

    if filename.lower().endswith(SUPPORTED_EXTENSIONS):
        date_taken = get_date_taken(file_path)
        folder_name = date_taken.strftime("%Y-%m")
        target_folder = os.path.join(dest_folder, folder_name)

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        unique_filename = get_unique_filename(target_folder, filename)
        shutil.move(file_path, os.path.join(target_folder, unique_filename))
        log_message(f"Moved {filename} → {unique_filename} in {target_folder}")

def select_source():
    """
    Function for open folder 
    selection dialog for source folder.
    """

    folder_selected = filedialog.askdirectory()
    entry_source.delete(0, tk.END)
    entry_source.insert(0, folder_selected)

def select_dest():
    """
    Function for open folder selection 
    dialog for destination folder.
    """

    folder_selected = filedialog.askdirectory()
    entry_dest.delete(0, tk.END)
    entry_dest.insert(0, folder_selected)

def log_message(message):
    """Function for displaying log 
    messages in the GUI.
    """

    text_log.insert(tk.END, message + "\n")
    text_log.see(tk.END)

# Create GUI window
root = tk.Tk()
root.title(get_translation("title"))
root.geometry("500x400")

# Language Selection
tk.Label(root, text="Language / Dil:").pack()
language_menu = tk.StringVar(root)
language_menu.set("English")  # Default language
dropdown = tk.OptionMenu(root, language_menu, *LANGUAGES.keys(), command=change_language)
dropdown.pack()

# Source Folder Selection
lbl_source = tk.Label(root, text=get_translation("source"))
lbl_source.pack(pady=5)
frame_source = tk.Frame(root)
frame_source.pack(pady=2)
entry_source = tk.Entry(frame_source, width=40)
entry_source.pack(side=tk.LEFT, padx=5)
btn_source = tk.Button(frame_source, text=get_translation("browse"), command=select_source)
btn_source.pack(side=tk.RIGHT)

# Destination Folder Selection
lbl_destination = tk.Label(root, text=get_translation("destination"))
lbl_destination.pack(pady=5)
frame_dest = tk.Frame(root)
frame_dest.pack(pady=2)
entry_dest = tk.Entry(frame_dest, width=40)
entry_dest.pack(side=tk.LEFT, padx=5)
btn_dest = tk.Button(frame_dest, text=get_translation("browse"), command=select_dest)
btn_dest.pack(side=tk.RIGHT)

# Recursive Checkbox
var_recursive = tk.BooleanVar()
chk_recursive = tk.Checkbutton(root, text=get_translation("include_subfolders"), variable=var_recursive)
chk_recursive.pack(pady=5)

# Sort Button
btn_sort = tk.Button(root, text=get_translation("sort_files"), command=sort_files_by_date, bg="green", fg="white")
btn_sort.pack(pady=10)

# Log Output
text_log = tk.Text(root, height=10, width=58)
text_log.pack(pady=5)

# Run GUI
root.mainloop()
