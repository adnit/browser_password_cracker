import Chrome
import Edge

val = input("You have 3 options: \n"
            "Chrome\n"
            "Edge\n"
            "Mozilla\n"
            "What browser do you want to use: ")

if __name__ == "__main__":
    if val == "Edge":
        Edge.edge()
    if val == "Chrome":
        Chrome.chrome()
    else:
        print("Browser typed wrong or is not supported")
