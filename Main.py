import firefox_decrypt
import Chrome
import Edge
from PasswordCrawler import PasswordCrawler
from tabulate import tabulate
import platform

chromelinuxStr = "Chrome-Linux"

if platform.system() == 'Linux':
    val = input('You have {} option{}: \n'
                '{} \n'
                'What browser do you want to use: '.format("1","", chromelinuxStr))
    if val == chromelinuxStr:
        chromeLinux = PasswordCrawler()
        data = chromeLinux.dump_passwords()
        print(tabulate(data, headers=["url", "username", "password"]))
    else:
        print("Browser typed wrong or is not supported")
else:
    val = input("You have 3 options: \n"
                "Chrome\n"
                "Edge\n"
                "Mozilla\n"
                "What browser do you want to use: ")

    if __name__ == "__main__":
        if val == "Edge":
            Edge.edge()
        elif val == "Chrome":
            Chrome.chrome()
        elif val == "Mozilla":
            firefox_decrypt.main()
        else:
            print("Browser typed wrong or is not supported")
