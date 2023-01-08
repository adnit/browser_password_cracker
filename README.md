# Zhvillimi i aplikacionit që lexon passwordët e ruajtur në browseret klasik (Edge, Chrome, Mozilla)
## Teknologjitë e përdorura
* Python
  * `os`
  * `json`
  * `base64`
  * `sqlite3`
  * `win32crypt`
  * `Cryptodome.Cipher`
  * `shutil`
  * `datetime`
---
## Instalimi
- win32crypt

```bash
pip install pypiwin32p 
```

- Cryptodome.Cipher
```bash
pip install pycryptodomex
```

---
## Implementimi
> Hapat realizues:
1. Fillimisht kemi një funksion që merr datën dhe kohën
2. Marrja e qelësit enkriptues të shfletuesit
3. Dekriptimi i fjalëkalimit
4. Lidhja me databazë
5. Selektimi i rreshtave të tabelës "login"
6. Iterimi në të gjith rreshtat 
7. Printimi i të gjith rreshtave qe i merr
8. Mbyllja e databazës
9. Largimi i file-it te krijuar

### Marrja e qelësit enkriptues
```python
def fetching_encryption_key():
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
```

### Dekriptimi i fjalëkalimit
```python 
def password_decryption(password, encryption_key):
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
```
### Krijimi i një file për ruajtjen e të dhënave
```python
  key = fetching_encryption_key_chrome()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "Default", "Login Data")
    filename = "RandomeName.db"
    shutil.copyfile(db_path, filename)
```

### Marrja e të dhenave nga file ku i kemi ruajtur dhe shtypja e tyre
```python
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
```
## Leximi i fjalëkalimeve të ruajtura në Mozilla Firefox 

Firefox_decrypt.py është një mjet për nxjerrjen e fjalëkalimeve nga profilet e Mozilla Firefox. Nese fjalkalimi kryesore nuk dihet, nuk kthen asnje te dhene.

Kërkon akses te libnss3, i përfshirë me shumicën e produkteve të Mozilla-s. 

### Përdorimi 

```bash
   python firefox_decrypt.py
```

Mjeti do të paraqesë një listë të numëruar të profileve. 

Pastaj, një kërkesë për të vendosur fjalëkalimin kryesor për profilin:

* Nëse nuk është vendosur asnjë fjalëkalim, nuk do të kërkohet një i tillë.
* Nëse një fjalëkalim është vendosur dhe dihet, futeni atë dhe shtypni butonin Kthehu ose Enter
* Nëse është vendosur një fjalëkalim dhe nuk dihet më, nuk mund të vazhdosh

Nëse profilet e juaja janë të vendosura në një path tjeter, mund të përdorni komanden:

```bash
  python firefox_decrypt.py /folder/containing/profiles.ini/
```
### Mënyra të tjera 

Ju gjithashtu mund të zgjidhni një nga formatet e mbështetura me `--format`:

 * `human` - Një format që shfaq një rekord për çdo 3 rreshta
 * `csv` - Formatin csv
 * `tabular` - E ngjashme me csv, por në vend të kësaj shfaqen nw formë tabelare.


```bash
   python firefox_decrypt.py --format human 
```

---

## Punuan

- [@AdhuresaSylejmani](https://github.com/AdhuresaSylejmani)
- [@AdnitKamberi](https://github.com/adnit)
- [@ArbenDedaj](https://github.com/ArbDe)


