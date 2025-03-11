import time
import tkinter as tk
from pathlib import Path
import SCPI_Voltage_Sweep as SCPIVS
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Results GUI")

        # Define the test results directory
        self.script_dir = Path(__file__).parent
        self.test_results_dir = self.script_dir / "Test Results"
        self.test_results_dir.mkdir(parents=True, exist_ok=True)

        # Save Location Label
        self.save_label = tk.Label(root, text="Results saved to:")
        self.save_label.grid(row=5, column=0, columnspan=2, pady=10)
        
        self.save_path_label = tk.Label(root, text=str(self.test_results_dir), fg="blue")
        self.save_path_label.grid(row=5, column=2, columnspan=2, pady=10)
        
        # Start Tests Button
        self.start_test_btn = tk.Button(root, text="Start Tests", command=self.start_tests)
        self.start_test_btn.grid(row=6, column=1, columnspan=2, pady=10)

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
            
            # Display the image using matplotlib
            self.display_image(image_path, i+1)

    def display_image(self, image_path, test_number):
        """Displays the image in a separate window using matplotlib."""
        img = mpimg.imread(image_path)
        plt.figure(figsize=(5, 5))
        plt.imshow(img)
        plt.axis("off")
        plt.title(f"Test Result {test_number}")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = TestApp(root)
    root.mainloop()
