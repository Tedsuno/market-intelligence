import os
import sys
from database.connection import init_db, test_connection
init_db()
test_connection()

if __name__ == "__main__":
    cmd = [sys.executable, "-m", "streamlit", "run", "dashboard/app.py"]
    os.execvp(cmd[0], cmd)
