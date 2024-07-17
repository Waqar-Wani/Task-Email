import schedule
import time
import subprocess

def run_batch_file():
    batch_file_path = r'C:\Users\Welcome\Desktop\vasista\Task Alert.bat'
    subprocess.run([batch_file_path], shell=True)

# Schedule the job to run every 15 minutes
schedule.every(15).minutes.do(run_batch_file)

# Function to display last and next runtime
def display_runtimes():
    last_runtime = schedule.jobs[-1].last_run
    next_runtime = schedule.jobs[-1].next_run
    print(f"Last Runtime: {last_runtime}, Next Runtime: {next_runtime}")

# Schedule the display_runtimes function to run every minute
schedule.every(10).minutes.do(display_runtimes)

# Run the scheduler continuously
while True:
    schedule.run_pending()
    time.sleep(1)
