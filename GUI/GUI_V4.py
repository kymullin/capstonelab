import time
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import SCPI_Voltage_Sweep as SCPIVS

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Results GUI")

        # Define the test results directory
        self.script_dir = Path(__file__).parent
        self.test_results_dir = self.script_dir / "Test Results"
        self.test_results_dir.mkdir(parents=True, exist_ok=True)

        # Setup GPIO
        self.relay_pins = [17, 27, 22, 23]  # GPIO pins for relays 1–4
        GPIO.setmode(GPIO.BCM)
        for pin in self.relay_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)  # Ensure all relays are off initially

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

        # Handle window close to cleanup GPIO
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

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
            # Activate current relay only
            for j, pin in enumerate(self.relay_pins):
                GPIO.output(pin, GPIO.HIGH if i == j else GPIO.LOW)

            image_path = self.test_results_dir / f"Test_Result_{i+1}.png"

            # Run the IV sweep test
            SCPIVS.perform_iv_sweep(self.test_results_dir, i+1)

            # Wait for the image to be created
            timeout = 10  # seconds
            start_time = time.time()
            while not image_path.exists():
                if time.time() - start_time > timeout:
                    print(f"Error: {image_path} not found after {timeout} seconds.")
                    return
                time.sleep(0.5)

            # Load and display the image
            img = Image.open(image_path)
            img = img.resize((400, 400), Image.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.image_labels[i].configure(image=img_tk)
            self.image_labels[i].image = img_tk

        # After all tests, turn off all relays
        for pin in self.relay_pins:
            GPIO.output(pin, GPIO.LOW)

    def on_closing(self):
        GPIO.cleanup()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
