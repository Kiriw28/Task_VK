# Импорт и устновка необходимых модулей

import os
import time
import winreg
from webbrowser import open as wb_open

os.system("pip install selenium")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Скачивание файла settings.reg

download_path = os.path.dirname(os.path.abspath(__file__))

chrome_options = Options()
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver_download = webdriver.Chrome(chrome_options)
driver_download.get("https://drive.google.com/uc?export=download&id=1IGENwFzLm8bBEboISadYSNEdxbnjz1fH")
button_element = driver_download.find_element(By.ID, "uc-download-link")
button_element.click()
time.sleep(4)
driver_download.close()

download_path += '\settings.reg'

# Вносим изменения в регистр

f = open(download_path, 'r')
lines = []
while True:
    line = f.readline()
    line = line.replace('\x00', '')
    if not line:
        break
    if len(line) > 2:
        lines.append(line)
key1 = ''
sub_key = ''
typest = ''
value = ''
got = 0
for string in lines:
    i = 0
    while i < len(string):
        if string[i] == '\\':
            n = i + 1
            while string[n] != ']':
                key1 += string[n]
                n += 1
            i = n
            key = winreg.OpenKeyEx(winreg.HKEY_CURRENT_USER, key1, access=winreg.KEY_SET_VALUE)
        if string[i] == '"':
            got = 1
            sub_key = ''
            n = i + 1
            while True:
                if string[n] == '"':
                    break
                else:
                    sub_key += string[n]
                    n += 1
            i = n
        if string[i] == '=':
            typest = ''
            n = i + 1
            while True:
                if string[n] == ':':
                    break
                else:
                    typest += string[n]
                    n += 1
            i = n
        if string[i] == ':':
            value = ''
            n = i + 1
            while n < len(string):
                value += string[n]
                n += 1
            value = int(value)
            i = n
        i += 1
    if got == 1:
        if typest == 'dword':
            type = winreg.REG_DWORD
        winreg.SetValueEx(key, sub_key, 0, type, value)
        print('done')
winreg.CloseKey(key)

# Запускаем Goose Goose Duck

wb_open('steam://rungameid/1568590')
