import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
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
        all_data = []
        colors = ['blue', 'red', 'green', 'black']

        for i in range(4):
            # Activate current relay
            for j, pin in enumerate(self.relay_pins):
                GPIO.output(pin, GPIO.HIGH if i == j else GPIO.LOW)

            # Run sweep and collect data
            voltages, currents = SCPIVS.perform_iv_sweep(str(self.test_results_dir), i+1)
            all_data.append((voltages, currents))

        # Turn off all relays
        for pin in self.relay_pins:
            GPIO.output(pin, GPIO.LOW)

        # Plot all data on a single graph
        plt.figure(figsize=(8, 6))
        for idx, (voltages, currents) in enumerate(all_data):
            plt.plot(voltages, currents, label=f'Test {idx+1}', color=colors[idx], marker="o", linestyle="-", markersize=2)

        plt.xlabel("Voltage (V)")
        plt.ylabel("Current (A)")
        plt.title("I-V Curves - Combined")
        plt.legend()
        plt.grid(True)

        combined_image_path = self.test_results_dir / "Combined_Test_Result.png"
        plt.savefig(combined_image_path)
        plt.close()

        # Display the combined image in all GUI slots
        img = Image.open(combined_image_path)
        img = img.resize((400, 400), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        for label in self.image_labels:
            label.configure(image=img_tk)
            label.image = img_tk


    def on_closing(self):
        GPIO.cleanup()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
