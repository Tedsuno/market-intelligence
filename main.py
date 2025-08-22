import os
import sys

if __name__ == "__main__":
    cmd = [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"]
    os.execvp(cmd[0], cmd)
