import json, pprint, datetime
import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

## Adding global attributes

roomId = "Y2lzY29zcGFyazovL3VzL1JPT00vZWI4MDU0YzAtM2NkOC0xMWVhLThhMTQtNTlkNTU4ZjFhMmI0"
webexToken = "YjIwMjRhMmItOGRhYi00MGE4LTk5OTctZDRhNDcwZDA4NzMwMDY3MGYwZTktZjJi_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"

def main():
  server = "192.168.42.1"
  port = "55443"
  user = "cisco"
  password = "cisco"

  token = get_token(server, port, user, password)
  run = get_run(server, port, token, roomId, webexToken)
  #print(get_int_status(server, port, token))
  hostname = get_hostname(server, port, token)
  file = write_to_file(hostname, run, server, user, password)

def get_token(server, port, user, password):
    url = "https://{0}:{1}/api/v1/auth/token-services".format(server, port)
    payload = {}
    headers = {
      'Accept': 'application/json'
    }
    response = requests.post(url=url, auth=HTTPBasicAuth(user, password), headers=headers, data=payload, verify=False)
    json_response = response.json()
    return json_response['token-id']

def get_run(server, port, token, roomId, webexToken):
  url = "https://{0}:{1}/api/v1/global/running-config".format(server, port)
  payload = {}
  headers = {'X-auth-token': token}
  response = requests.get(url=url, headers=headers, data=payload, verify=False)
  text = response.text
  #webex_notify(roomId, webexToken, text)
  return response.text

def get_int_status(server, port, token):
  url = "https://{0}:{1}/api/v1/interfaces".format(server, port)
  payload = {}
  headers = {'X-auth-token': token}
  response = requests.get(url=url, headers=headers, data=payload, verify=False)

  print(response.json())

def get_hostname(server, port, token):
  url = "https://{0}:{1}/api/v1/global/host-name".format(server, port)
  payload = {}
  headers = {'X-auth-token': token}
  response = requests.get(url=url, headers=headers, data=payload, verify=False)
  json_response = response.json()
  return json_response['host-name']

def write_to_file(hostname, run, server, user, password):
  file_name = timeStamped("{0}".format(hostname))
  router_config = open(file_name, "w")
  router_config.write(run)
  router_config.close()

  upload_to_ownCloud(user, password, server, file_name)

def timeStamped(fname, fmt='{fname}_%d-%m-%Y-%H-%M'):
  return datetime.datetime.now().strftime(fmt).format(fname=fname)

def upload_to_ownCloud(user, password, server, file):
  url = 'http://10.66.211.61:8080/remote.php/dav/files/cisco/{}'.format(file)
  own_cloud_url = 'http://10.66.211.61:8080/remote.php/webdav/{}'.format(file)
  data = open(file, 'rb').read()
  response = requests.put(url=url, auth=HTTPBasicAuth(user, password), data=data, verify=False)
  text = 'UPLOAD: Config file for {0} {1} has been uploaded to OwnCloud. Download the file via {2}'.format(server, file, own_cloud_url)
  webex_notify(text)

def webex_notify(text):
  url = "https://api.ciscospark.com/v1/messages"
  payload = {
    "roomId": roomId,
    "text": text
  }
  headers = {'Authorization' : 'Bearer {}'.format(webexToken)}
  response = requests.post(url=url, headers=headers, data=payload)
  print (response.text)
  #return response.text

main()
