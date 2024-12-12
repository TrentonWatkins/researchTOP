import subprocess
import time
from ipcam import pub

def run_pub():
    """Run the pub.py script."""
    print("Running pub.py...")
    subprocess.run(["python", ".\\ipcam\\pub.py"], check=True)

def run_stored_data():
    """Run the Stored_Data.py script."""
    print("Running Stored_Data.py...")
    process = subprocess.Popen(["python", "Stored_Data.py"])
    # Allow it to run briefly, assuming it completes after initialization
    time.sleep(5)  # Adjust as needed for how long it takes to complete
    process.terminate()  # Stop the process if it isn't needed to run continuously
    print("Stored_Data.py has been terminated.")

def run_real_time_input():
    """Run the RealTimeInput.py script."""
    print("Running RealTimeInput.py...")
    subprocess.run(["python", "RealTimeInput.py"], check=True)

if __name__ == "__main__":
    try:
        # Run the scripts in the specified order
        run_pub()
        run_stored_data()
        run_real_time_input()
    except Exception as e:
        print(f"An error occurred while running the scripts: {e}")

