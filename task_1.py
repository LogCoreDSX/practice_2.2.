#task 2.1

import requests

# Константы
URL_LIST = [
    "https://github.com/",
    "https://www.binance.com/en",
    "https://tomtit.tomsk.ru/",
    "https://jsonplaceholder.typicode.com/",
    "https://moodle.tomtit-tomsk.ru/"
]


#Функция быстрый вывод частых сообщений
def say(mode0=" ", mode1=" "):
    if mode0 == "s":
        print("<--- Beginning work Program --->\n")
    elif mode0 == "e":
        print("\n<--- End work Program --->")
    elif mode0 == "er":
        if mode1 == "req":
            print("Error. Request failed !\n")


#Функция определение статуса по коду ответа
def get_status_text(status_code):
    if status_code == 200:
        return "Available"
    elif status_code == 403:
        return "No access"
    elif status_code == 404:
        return "Not Found"
    elif status_code == 500 or status_code == 502 or status_code == 503:
        return "Server Error"
    else:
        return "Not Available"


#Функция проверка статуса одного URL
def check_url_status(url): #
    try:
        response = requests.get(url, timeout = 10, allow_redirects = True)
        status_code = response.status_code
        status_text = get_status_text(status_code)
        return status_code, status_text

    except requests.exceptions.RequestException:
        return None, "Not Available"


#Главная часть
say("s")
print("<-- HTTP Status Site -->\n")
status_list = []
for i in URL_LIST:
    print(f"Checking: {i}")
    status_code_main, status_text_main = check_url_status(i)
    if  status_code_main is None:
        print(f"  Status: {status_text_main}\n")
        status_list.append({
            "url": i,
            "status": status_text_main,
            "code": "N/A"
        })
    else:
        print(f"  Status: {status_text_main} - {status_code_main}\n")
        status_list.append({
            "url": i,
            "status": status_text_main,
            "code":  status_code_main
        })
print("\n<-- Final Status -->\n")
print("URL - Available - Code \n")
for i in status_list:
    print(f"{i['url']} - {i['status']} - {i['code']}")
with open('resource/result/http_monitor.txt', 'w') as file_save: # Сохранение в файл
    file_save.write("- HTTP Status Monitor -\n\n")
    file_save.write("URL - Available - Code\n\n")
    for i in status_list:
        file_save.write(f"{i['url']} - {i['status']} - {i['code']}\n")
print("\n> Results saved in resource/result/http_monitor.txt")
say("e")
