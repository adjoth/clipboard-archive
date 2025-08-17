#import pyperclip # pip install pyperclip
from tkinter import Tk
from pathlib import Path
import time, atexit, json

class ClipboardManager:
    data : dict = {}
    key: str| None = None
    key_value: list = []
    SLEEP_DURATION_SEC = 0.5
    FILE_NAME = Path('data','_data.json')

    @staticmethod
    def setup():
        """
        Load data from data/_data.json file if it exists. And store it in the data attribute.
        """
        if ClipboardManager.FILE_NAME.exists():
            with open(ClipboardManager.FILE_NAME, 'r') as file:
                ClipboardManager.data = json.load(file)
        else:
            raise FileNotFoundError(f"Data file {ClipboardManager.FILE_NAME} not found. Please create it first.")
        

    @staticmethod
    def run():
        ClipboardManager.print_data_keys()
        ClipboardManager.select_key_from_data()
        ClipboardManager.loop_copying_clipboard_to_data()

    @staticmethod
    def print_data_keys():
        """
        Print the keys of the data dictionary.
        """
        for index, key in enumerate(ClipboardManager.data.keys()):
            print(f"{index + 1}: {key}")

    @staticmethod
    def select_key_from_data():
        """
        Select a key from the data dictionary and return its value.
        If the key does not exist, return an empty string.
        """
        data = ClipboardManager.data
        while True:
            key = input("Enter the key to select from data: ")
            ClipboardManager.key = key
            if key in data:
                ClipboardManager.key_value = data[key]
                break
            elif( key.isdigit() ):
                key = int(key) - 1
                keys_list = list(data.keys())
                if( key >= 0 and key < len(keys_list) ):
                    ClipboardManager.key = keys_list[key]
                    ClipboardManager.key_value = data[ClipboardManager.key]
                    break
                else:
                    print("Invalid selection. Please try again.")
            else:
                # Create a new key if it does not exist
                print(f"Creating new list for {key}")
                ClipboardManager.data[key] = []
                ClipboardManager.key_value = data[key]
                break
    
    @staticmethod
    def loop_copying_clipboard_to_data():
        while True:
            time.sleep(ClipboardManager.SLEEP_DURATION_SEC) 
            clip = Tk().clipboard_get()
            if clip not in ClipboardManager.key_value:
                print(f"Added to clipboard: {clip}")
                ClipboardManager.key_value.append(clip)

    @staticmethod
    def exit_handler():
        """
        Save the data to the data/_data.json file on exit.
        """
        ClipboardManager.data[ClipboardManager.key] = ClipboardManager.key_value
        with open(ClipboardManager.FILE_NAME, 'w') as file:
            json.dump(ClipboardManager.data, file, indent=4)

if __name__ == "__main__":
    ClipboardManager.setup()
    atexit.register(ClipboardManager.exit_handler)
    ClipboardManager.run()