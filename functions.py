import requests
import json
import os

def provision_device(provision_url, devices, username, password):
    if devices == "device_list.txt":
    # if os.path.isfile(devices):
        with open("device_list.txt") as file:
        # with open(devices) as file:
            device_list = file.readlines()
            device_list = [line.rstrip() for line in device_list]
        for device in device_list:
            provision(provision_url, device, username, password)
    else:
        ips = [x.strip() for x in devices.split(',')]
        for ip in ips:
            provision(provision_url, ip, username, password)


def provision(provision_url, device, username, password):
    try:
        server_url = "{\"formData\":{\"AutoProvisionServerURL\":\"%s\"}}" % (provision_url)
        session = requests.session()
        request_login = session.post(f"http://{device}/api/auth/login?p=Login", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=f"username={username}&pwd={password}")
        if request_login.status_code == 200:
            request_login_json_data = json.loads(request_login.content)
            if request_login_json_data["ret"] == "ok":
                session.post(f"http://{device}/api/inner/writeconfig?p=SettingAutop", headers={"Content-Type": "text/plain"}, data=server_url)
                session.post(f"http://{device}/api/autop/now?p=SettingAutop", data="")
                # check if autoprovision has been pressed then show text. 
                return print(f"{device}: Has been provisioned.\r")
            elif request_login_json_data["error"]["webStatus"] == "lock":
                return print(f"{device}: Has been locked for " + request_login_json_data["error"]['lockTime'] + " minutes.\r")
            elif request_login_json_data["error"]["webStatus"] == "error":
                if request_login_json_data["error"]["msg"] == "error_username_or_password_is_wrong":
                    return print(f"{device}: Wrong credentials.\r")
        else:
            return print(f"{device}: Cannot connect to device.\r")
    except Exception:
        return print(f"{device}: Cannot connect to device.\r")
