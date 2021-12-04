import requests
import json

def provision_device(device, provision_url, username, password):
	server_url = "{\"formData\":{\"AutoProvisionServerURL\":\"%s\"}}" % (provision_url)
	session = requests.session()
	request_login = session.post(f"http://{device}/api/auth/login?p=Login", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=f"username={username}&pwd={password}")
	request_login_json_data = json.loads(request_login.content)
	if request_login_json_data["ret"] == "ok":
		session.post(f"http://{device}/api/inner/writeconfig?p=SettingAutop", headers={"Content-Type": "text/plain"}, data=server_url)
		session.post(f"http://{device}/api/autop/now?p=SettingAutop", data="")
		return "{0}: Has been provisioned.\r".format(device)
	elif request_login_json_data["error"]["webStatus"] == "lock":
		return "{0}: Has been locked for {1} minutes.\r".format(device,request_login_json_data["error"]['lockTime'])
	elif request_login_json_data["error"]["webStatus"] == "error":
		if request_login_json_data["error"]["msg"] == "error_username_or_password_is_wrong":
			return "{0}: Wrong credentials.\r".format(device)
 
	