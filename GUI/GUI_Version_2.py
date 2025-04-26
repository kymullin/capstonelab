
import time
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
import SCPI_Voltage_Sweep as SCPIVS

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Results GUI")

        # Define the test results directory
        self.script_dir = Path(__file__).parent
        self.test_results_dir = self.script_dir / "Test Results"
        self.test_results_dir.mkdir(parents=True, exist_ok=True)

        self.image_labels = []
        self.load_placeholder_images()
        
        # Save Location Label
        self.save_label = tk.Label(root, text="Results saved to:")
        self.save_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.save_path_label = tk.Label(root, text=str(self.test_results_dir), fg="blue")
        self.save_path_label.grid(row=5, column=2, columnspan=2, pady=10)
        
        # Buttons
        self.start_test_btn = tk.Button(root, text="Start Tests", command=self.start_tests)
        self.start_test_btn.grid(row=6, column=1, columnspan=2, pady=10)
        
    def load_placeholder_images(self):
        placeholder = Image.new('RGB', (400, 400), color=(200, 200, 200))
        self.placeholder_img = ImageTk.PhotoImage(placeholder)
        
        for i in range(4):
            label_text = tk.Label(self.root, text=f"Test Result {i+1}")
            label_text.grid(row=0, column=i, pady=5)
            
            label_image = tk.Label(self.root, image=self.placeholder_img)
            label_image.grid(row=1, column=i, padx=10, pady=10)
            self.image_labels.append(label_image)

    def start_tests(self):       
        for i in range(4):
            image_path = self.test_results_dir / f"Test_Result_{i+1}.png"
            
            # Run the IV sweep test
            SCPIVS.perform_iv_sweep(self.test_results_dir, i+1)
            
            # Wait for the image to be created
            timeout = 10  # Maximum wait time in seconds
            start_time = time.time()
            
            while not image_path.exists():
                if time.time() - start_time > timeout:
                    print(f"Error: {image_path} not found after {timeout} seconds.")
                    return
                time.sleep(0.5)  # Check every 0.5 seconds
            
            # Load and display the generated image
            img = Image.open(image_path)
            img = img.resize((400, 400), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_labels[i].configure(image=img_tk)
            self.image_labels[i].image = img_tk

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
