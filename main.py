from functions import provision_device


def main():
    print("What needs to be the url?")
    provision_url = str(input("url: "))
    with open("device_list.txt") as file:
        device_list = file.readlines()
        device_list = [line.rstrip() for line in device_list]

    for device in device_list:
        provision_device(device, provision_url, "admin", "admin")

if __name__ == '__main__':
    main()
