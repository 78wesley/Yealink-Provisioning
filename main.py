from os import system
from functions import provision_device
import sys

def main():
    if len(sys.argv) > 1:
        provision_device(sys.argv[1], sys.argv[2], "admin", "admin")
    else:
        print("What needs to be the url?")
        question = str(input("url: "))
        provision_device(question, "device_list.txt", "admin", "admin")

if __name__ == '__main__':
    main()