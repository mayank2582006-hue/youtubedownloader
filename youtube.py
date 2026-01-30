import tkinter as tk
from tkinter import filedialog, messagebox
from pytube import YouTube
import threading

def start_download():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube video link.")
        return

    folder = filedialog.askdirectory()
    if not folder:
        messagebox.showerror("Error", "Please select a folder to save the video.")
        return

    threading.Thread(target=download_video, args=(url, folder)).start()

def download_video(url, folder):
    try:
        status_label.config(text="Downloading... Please wait ⏳")
        yt = YouTube(url, on_progress_callback=update_progress)
        stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
        stream.download(output_path=folder)
        status_label.config(text="Download completed successfully!")
        messagebox.showinfo("Success", f"Video saved in:\n{folder}")
    except Exception as e:
        status_label.config(text="Download failed.")
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

def update_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    downloaded = total_size - bytes_remaining
    percent = int(downloaded / total_size * 100)
    progress_var.set(percent)
    progress_bar.update()

root = tk.Tk()
root.title("YouTube Video Downloader")
root.geometry("500x250")
root.resizable(False, False)

tk.Label(root, text="Enter YouTube URL:", font=("Arial", 12)).pack(pady=10)
url_entry = tk.Entry(root, width=50, font=("Arial", 12))
url_entry.pack(pady=5)

download_button = tk.Button(root, text="Download Video", font=("Arial", 12, "bold"),
                            bg="green", fg="white", command=start_download)
download_button.pack(pady=15)

progress_var = tk.IntVar()
progress_bar = tk.Scale(root, variable=progress_var, orient="horizontal",
                        length=400, from_=0, to=100)
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
status_label.pack(pady=5)

root.mainloop()