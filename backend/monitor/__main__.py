import sys
import pathlib
import time

if __name__ == "__main__":
    sys.path.insert(1, str(pathlib.Path(__file__).parent.parent))
    from monitor import Monitor
    try:
        monitor = Monitor()        
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("CTRL+C detected, exiting...")
        sys.exit()