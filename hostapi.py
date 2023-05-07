import os

import requests
import config

api_base_url = "https://www.pythonanywhere.com/api/v0/user/vincinemaApi"
api_token = config.api_token

consindex = -1
consoles = []
def GetConsoles():
    global consindex, consoles
    response = requests.get(api_base_url + "/consoles/", headers={"Authorization": "Token " + api_token})
    if response.status_code == 200:
        consoles = response.json()
        print("Select console:")
        for i in range(len(consoles)):
            print(f"{i + 1}. {consoles[i]['name']}")
        while True:
            try:
                consindex = int(input("Enter console index: "))
                if consindex > len(consoles) or consindex < 1:
                    print("Error: Invalid console index.")
                else:
                    consindex -= 1
                    break
            except ValueError:
                print("Error: Invalid console index.")
    else:
        print("Error: Could not retrieve console data.")
        exit()

GetConsoles()


def GetOutput():
    response = requests.get(api_base_url + "/consoles/{id}/get_latest_output/".format(id=consoles[consindex]["id"]),headers={"Authorization": "Token " + api_token})
    if response.status_code == 200:
        os.system("cls")
        print(f"{response.json()['output']}", end="")
    else:
        print("Error: Could not retrieve console output.")


def SendInput(text):
    print("waiting for response...")
    response = requests.post(api_base_url + "/consoles/{id}/send_input/".format(id=consoles[consindex]["id"]),
                             data={"input": text + "\n"}, headers={"Authorization": "Token " + api_token})
    print(response.text)
    if response.status_code != 200:
        print("Error: Could not send input to console.")


is_reloading = False
import time
import threading


def print_time():
    curent_time = time.time()
    while is_reloading:
        print(f"reloading, seconds passed {round(time.time() - curent_time, 2)}", end="\r")
        if not is_reloading:
            break


def printUpload():
    curent_time = time.time()
    while is_uploading:
        print(f"uploading, seconds passed {round(time.time() - curent_time, 2)}", end="\r")
        if not is_uploading:
            break


is_uploading = False


def reload(param=1):
    global is_reloading, is_uploading
    if param == 1:
        is_uploading = True
        threading.Thread(target=printUpload).start()
        uploadfile()
        is_uploading = False
        print("------------------uploaded--------------------")
    is_reloading = True
    threading.Thread(target=print_time).start()
    response = requests.post(api_base_url + "/webapps/vincinemaapi.pythonanywhere.com/reload/",
                             headers={"Authorization": "Token " + api_token})
    is_reloading = False
    print(response.text)
    if response.status_code != 200:
        print("Error: webapp reload failed")
    else:
        print("------------------reloaded--------------------")


def uploadfile():
    with open("D:\\VNTU\\1 course\\2 semestr\\web\\testflaks\\app.py", "rb") as f:
        file_data = f.read()
    response = requests.post(api_base_url + "/files/path/home/vincinemaApi/Cinema/app.py",
                             headers={"Authorization": "Token " + api_token},
                             files={"content": ("app.py", file_data, "application/octet-stream")})
    if response.status_code != 201 and response.status_code != 200:
        print("Error: Could not upload file.")
        exit()


while True:
    GetOutput()
    command = input()
    if command == "reload":
        reload()
    elif command == "exit":
        exit()
    elif command == "upload":
        uploadfile()
    elif command == "reload -r":
        reload(0)
    elif command == "url":
        os.system("start https://vincinemaapi.pythonanywhere.com/")
    elif command == "chconsole":
        GetConsoles()
    elif command == "help":
        print('''
        reload - reloads webapp
        reload -r - reloads webapp without uploading
        url - opens webapp url
        upload - uploads app.py
        chconsole - changes console
        exit - exits
        ''')
        input("press enter to continue")
    else:
        SendInput(command)
