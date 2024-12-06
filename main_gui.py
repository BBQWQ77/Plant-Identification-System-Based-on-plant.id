import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from plant_identification import identify_plant, parse_suggestions
import requests
from io import BytesIO


def display_image(uploaded_image_path):
    suggestions = identify_plant(uploaded_image_path)

    uploaded_image = Image.open(uploaded_image_path)
    uploaded_photo = ImageTk.PhotoImage(uploaded_image.resize((200, 200)))
    uploaded_canvas.config(image=uploaded_photo)
    uploaded_canvas.image = uploaded_photo

    for widget in result_frame.winfo_children():
        widget.destroy()

    tk.Label(result_frame, text="classification results：", font=("Arial", 14)).grid(row=0, column=0, columnspan=2,
                                                                                    sticky="w", padx=5,
                                                                                    pady=5)

    for i, suggestion in enumerate(suggestions):
        tk.Label(result_frame, text=f"{suggestion['name']} ({suggestion['probability'] * 100:.2f}%)",
                 font=("Arial", 12)).grid(row=i + 1, column=0, sticky="w", padx=5, pady=5)

        similar_image = download_image(suggestion["image_url"])
        similar_photo = ImageTk.PhotoImage(similar_image.resize((100, 100)))
        img_label = tk.Label(result_frame, image=similar_photo)
        img_label.image = similar_photo  # 保持引用
        img_label.grid(row=i + 1, column=1, padx=5, pady=5)


def download_image(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    return Image.open(image_data)


def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        display_image(file_path)


root = tk.Tk()
root.title("Plant recognition results")

uploaded_canvas = tk.Label(root)
uploaded_canvas.pack()

result_frame = tk.Frame(root)
result_frame.pack(pady=10)

upload_button = tk.Button(root, text="Upload plant images", command=upload_image)
upload_button.pack(pady=10)

root.mainloop()
