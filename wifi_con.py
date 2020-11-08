import subprocess
import time


def check_result(profile):
    result = subprocess.run(f"netsh wlan connect name={profile}", shell=True, stdout=subprocess.PIPE)
    result = result.stdout.decode('cp866', 'ignore')
    time.sleep(10)
    return result


def check_ping():
    ping = subprocess.run("ping 2miners.com", shell=True, stdout=subprocess.PIPE)
    ping = ping.stdout.decode('cp866', 'ignore')
    time.sleep(10)
    return ping


def time_print(string):
    print(time.strftime('%X', time.localtime()), end=' ')
    print(string)


profile = subprocess.run("netsh wlan show profile", shell=True, stdout=subprocess.PIPE)
profile = profile.stdout.decode('cp866', 'ignore')
profile_list = []
with open('wifi_list.txt', 'w+', encoding='utf-8') as file:
    file.write(profile)
    file.seek(0)
    for line in file.readlines():
        if 'Все профили пользователей' in line:
            start = line.find(':') + 2
            profile_list.append(line[start:].strip())

connected_ssid = ''

while True:
    ping = check_ping()
    interface = subprocess.run("netsh wlan show interface", shell=True, stdout=subprocess.PIPE)
    interface = interface.stdout.decode('cp866', 'ignore')
    start = interface.find('SSID')
    end = interface.find('\n', start)
    ssid = interface[start: end].strip()
    if 'Обмен пакетами' in ping:

        if not ssid == connected_ssid:
            time_print(f'Connected to {ssid}')
            connected_ssid = ssid
        else:
            time.sleep(15)
    else:
        for profile in profile_list:
            result = check_result(profile)
            new_ping = check_ping()
            time_print(f'Подключение к {profile} : {result[:-2]}')
            if 'Обмен пакетами' in new_ping:
                time_print(f'Доступ к сети {profile} : YES')
                break
            else:
                time_print(f'Доступ к сети {profile} : NO')
