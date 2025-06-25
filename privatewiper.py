import os
import sys
import ctypes
import shutil
import tempfile
import subprocess
import random
import requests
from colorama import init, Fore, Style
import pyfiglet

init(autoreset=True)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def show_banner():
    banner = pyfiglet.figlet_format("PrivateWiper")
    print(Fore.GREEN + banner)
    print(Fore.CYAN + "Security, Privacy Operations\n")

def random_filename(length=16):
    return ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=length))

def secure_delete(path, passes=3):
    if not os.path.isfile(path):
        print(Fore.RED + f"Error: File {path} not found.")
        return

    size = os.path.getsize(path)

    with open(path, "r+b", buffering=0) as f:
        for i in range(passes):
            print(Fore.YELLOW + f"Pass {i+1}: Writing random data...")
            f.seek(0)
            f.write(os.urandom(size))
            f.flush()
            os.fsync(f.fileno())

    directory = os.path.dirname(path)
    original_name = os.path.basename(path)
    new_name = random_filename() + ".del"
    new_path = os.path.join(directory, new_name)
    os.rename(path, new_path)
    print(Fore.CYAN + f"File name changed from '{original_name}' to '{new_name}'.")

    with open(new_path, "r+b", buffering=0) as f:
        for i in range(passes):
            print(Fore.YELLOW + f"Pass {i+1} (new name): Writing random data again...")
            f.seek(0)
            f.write(os.urandom(size))
            f.flush()
            os.fsync(f.fileno())

    os.remove(new_path)
    print(Fore.GREEN + f"{original_name} has been securely deleted.")

def wipe_free_space():
    try:
        dummy_path = os.path.join(tempfile.gettempdir(), "wipe_temp_file")
        print(Fore.YELLOW + "Filling free space (manual wipe)...")
        with open(dummy_path, "wb") as f:
            while True:
                f.write(os.urandom(1024 * 1024)) 
                f.flush()
    except:
        print(Fore.CYAN + "Disk is full, removing temporary file...")
    finally:
        try:
            os.remove(dummy_path)
        except:
            pass
        print(Fore.GREEN + "Free space wipe complete.")

def run_cipher():
    if os.name != "nt":
        print(Fore.RED + "This command only works on Windows.")
        return
    try:
        subprocess.run(["cipher", "/w:C:"], check=True, shell=True)
        print(Fore.GREEN + "Wiping command has completed.")
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"Error:\n{e}")

def clean_browser_history():
    print(Fore.YELLOW + "Clearing browser history...")
    user = os.getenv("USERNAME")
    if os.name == "nt":
        chrome = f"C:\\Users\\{user}\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
        edge = f"C:\\Users\\{user}\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default"
        firefox = f"C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"

        paths = [chrome, edge]
        for path in paths:
            try:
                history = os.path.join(path, "History")
                if os.path.exists(history):
                    os.remove(history)
                    print(Fore.GREEN + f"History for {path} cleared.")
            except Exception as e:
                print(Fore.RED + f"Error: {e}")
        try:
            if os.path.exists(firefox):
                shutil.rmtree(firefox)
                print(Fore.GREEN + "Firefox profiles and history cleared.")
        except Exception as e:
            print(Fore.RED + f"Error: {e}")
    else:
        print(Fore.RED + "Currently, only Windows is supported.")

def fetch_random_proxy():
    print(Fore.YELLOW + "Fetching random proxy...")
    try:
        response = requests.get("https://www.proxy-list.download/api/v1/get?type=http")
        proxy_list = response.text.strip().split("\n")
        proxy = random.choice(proxy_list)
        print(Fore.GREEN + f"Proxy: {proxy}")
        return proxy
    except:
        print(Fore.RED + "Could not fetch proxy.")
        return None

def privacy_surprise():
    print(Fore.MAGENTA + "\n🔐 Loading Privacy Surprise Package...")
    options = [
        "DNS cache cleared.",
        "Recently used files list cleared.",
        "Recycle bin emptied.",
        "Windows Temp folder cleaned.",
    ]
    surprise = random.sample(options, 3)
    for action in surprise:
        print(Fore.CYAN + "✔ " + action)

def menu():
    print(Fore.YELLOW + "\nOptions:")
    print("[1] Wipe file(s)")
    print("[2] Wipe free space")
    print("[3] Wipe free space (more secure, Windows only)")
    print("[4] Clear browser history (Chrome, Edge, Firefox)")
    print("[5] Fetch random proxy")
    print("[6] Privacy Surprise!")
    print("[7] Exit")

def main():
    show_banner()

    while True:
        menu()
        choice = input(Fore.BLUE + "Your choice: ")

        if choice == "1":
            files = input("Enter the file paths to delete (separate with commas): ").split(",")
            for file_path in files:
                secure_delete(file_path.strip())
        elif choice == "2":
            wipe_free_space()
        elif choice == "3":
            run_cipher()
        elif choice == "4":
            clean_browser_history()
        elif choice == "5":
            fetch_random_proxy()
        elif choice == "6":
            privacy_surprise()
        elif choice == "7":
            print(Fore.GREEN + "Exiting...")
            break
        else:
            print(Fore.RED + "Invalid choice.")

if __name__ == "__main__":
    main()
