import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Results GUI")
        self.save_location = tk.StringVar(value="Not Selected")

        self.image_labels = []
        self.load_placeholder_images()
        
        # Save Location Label
        self.save_label = tk.Label(root, text="Results saved to:")
        self.save_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.save_path_label = tk.Label(root, textvariable=self.save_location, fg="blue")
        self.save_path_label.grid(row=5, column=2, columnspan=2, pady=10)
        
        # Buttons
        self.change_location_btn = tk.Button(root, text="Change Save Location", command=self.change_save_location)
        self.change_location_btn.grid(row=6, column=0, columnspan=2, pady=10)
        
        self.start_test_btn = tk.Button(root, text="Start Tests", command=self.start_tests)
        self.start_test_btn.grid(row=6, column=2, columnspan=2, pady=10)
        
    def load_placeholder_images(self):
        placeholder = Image.new('RGB', (300, 300), color=(200, 200, 200))
        self.placeholder_img = ImageTk.PhotoImage(placeholder)
        
        for i in range(4):
            label_text = tk.Label(self.root, text=f"Test Result {i+1}")
            label_text.grid(row=0, column=i, pady=5)
            
            label_image = tk.Label(self.root, image=self.placeholder_img)
            label_image.grid(row=1, column=i, padx=10, pady=10)
            self.image_labels.append(label_image)

    def change_save_location(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.save_location.set(folder_selected)

    def start_tests(self):
        save_path = self.save_location.get()
        if save_path == "Not Selected":
            print("Please select a save location first.")
            return

        for i in range(4):
            image_path = os.path.join(save_path, f"Test_Result_{i+1}.png")
            if os.path.exists(image_path):
                img = Image.open(image_path)
                img = img.resize((300, 300), Image.LANCZOS)
                img_tk = ImageTk.PhotoImage(img)
                self.image_labels[i].configure(image=img_tk)
                self.image_labels[i].image = img_tk
            else:
                print(f"Image {image_path} not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()