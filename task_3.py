#task 2.3

import requests
import json
import os


#Константы
URL_CBR = "https://www.cbr-xml-daily.ru/daily_json.js"
SAVE_FILE = "resource/result/save.json"
MAX_PASS_LINE = [0, 100]


#Функция быстрый вывод частых сообщений
def say(mode0= None, mode1="\n"):
    if mode0 in range(MAX_PASS_LINE[0],MAX_PASS_LINE[1]): print(mode1 * mode0)
    elif mode0 == "s": print("<--- Beginning work Program --->\n")
    elif mode0 == "e": print("\n<--- End work Program --->")
    elif mode0 == "er":
        if mode1 == "req": print("Error. Request failed !\n")
        elif mode1 == "load": print("Error. Failed to LOAD save file !\n")
        elif mode1 == "code": print("Error. Currency code  NOT FOUND !\n")
        elif mode1 == "group": print("Error. Group NOT FOUND !\n")
        elif mode1 == "empty": print("Error. Input CANNOT be empty !\n")
        elif mode1 == "exists": print("Error. Group already exists !\n")
        elif mode1 == "mode": print("Error. Mode NOT FOUNT !\n")
        elif mode1 == "save": print("Error. Failed to SAVE file !\n")


#Функция ввод строки с проверкой
def input_string(text):
    while True:
        input_str = input(f"> {text}")
        if input_str.strip() == "":
            say("er", "empty")
            continue
        return input_str.strip()


#Функция получение данных о курсах валют
def get_currency_data():
    try:
        response = requests.get(URL_CBR, timeout = 10)
        response.raise_for_status()
        data_dict = response.json()
        return data_dict["Valute"]
    except (requests.exceptions.RequestException, KeyError):
        say("er", "req")
        return {}


#Функция Вывод всех валют
def show_all_currencies(currency_dict):
    print("\n-- All Currencies --\n")
    print(f"{'Code':<8} {'Name':<35} {'Rate':<12} {'Nominal':<8}")
    say(70, "-")
    for code, info_dict in currency_dict.items():
        print(
            f"{code:<8} {info_dict['Name']:<35} "
            f"{info_dict['Value']:<12.4f} {info_dict['Nominal']:<8}")
    print("\n")



#Функция вывод валюты по коду
def show_currency_by_code(currency_dict):  #
    print("\n-- Find Currency --\n")
    currency_code = input_string("Enter currency code (USD, EUR, etc): ")
    if currency_code in currency_dict:
        info_dict = currency_dict[currency_code]
        print(f"\nCurrency: {info_dict['Name']} ({currency_code})")
        print(f"Rate: {info_dict['Value']:.4f} RUB")
        print(f"Nominal: {info_dict['Nominal']}")
        print(f"Previous rate: {info_dict['Previous']:.4f} RUB")
    else:
        say("er", "code")
    say(1)


#Функция сохранение и загрузка группы
def edit_groups(mode_main=" ", group_dict = None):
    if mode_main == "SAVE":
        try:
            os.makedirs(os.path.dirname(SAVE_FILE), exist_ok = True)
            with open(SAVE_FILE, 'w') as file_save:
                json.dump(
                    group_dict, file_save, ensure_ascii = False, indent = 4)
            print("Groups saved successfully\n")
        except FileNotFoundError:
            say("er", "save")
    elif mode_main == "LOAD":
        if not os.path.exists(SAVE_FILE):
            return {}
        try:
            with open(SAVE_FILE, 'r', encoding = 'utf-8') as file_load:
                return json.load(file_load)
        except (json.JSONDecodeError, FileNotFoundError):
            say("er", "load")
            return {}


#Функция создание новой группы
def create_group(group_dict):
    print("\n-- Create Group --\n")
    group_name = input_string("Enter group name: ")
    if group_name in group_dict:
        say("er", "exists")
        return group_dict
    group_dict[group_name] = []
    edit_groups("SAVE", group_dict)
    print(f"Group '{group_name}' created successfully\n")
    return group_dict


#Функция добавление валюты в группу
def add_currency_to_group(currency_dict, group_dict):
    print("\n-- Add Currency to Group --\n")

    if not group_dict:
        print("No groups found. Create a group first !\n")
        return group_dict

    print("Available groups:")
    for i in group_dict:
        print(f"  - {i}\n")

    group_name = input_string("Select group name: ")
    if group_name not in group_dict:
        say("er", "group")
        return group_dict

    currency_code = input_string("Enter currency code to add: ").upper()
    if currency_code not in currency_dict:
        say("er", "code")
        return group_dict

    if currency_code not in group_dict[group_name]:
        group_dict[group_name].append(currency_code)
        edit_groups("SAVE",group_dict)
        print(f"Currency '{currency_code}' added to group '{group_name}'\n")
    else:
        print(f"Currency '{currency_code}' already in group '{group_name}'\n")

    return group_dict


#Функция удаление валюты из группы
def remove_currency_from_group(group_dict):
    print("\n-- Remove Currency from Group --\n")
    if not group_dict:
        print("No groups found !\n")
        return group_dict

    print("Available groups:")
    for i in group_dict:
        print(f"  - {i} ({len(group_dict[i])} currencies)")
    print("\n")

    group_name = input_string("Select group name: ")
    if group_name not in group_dict:
        say("er", "group")
        return group_dict

    if not group_dict[group_name]:
        print(f"Group '{group_name}' is empty\n")
        return group_dict

    print(f"\nCurrencies in '{group_name}':")
    for i in group_dict[group_name]:
        print(f"  - {i}")
    print("\n")
    currency_code = input_string("Enter currency code to remove: ").upper()
    if currency_code in group_dict[group_name]:
        group_dict[group_name].remove(currency_code)
        edit_groups("SAVE",group_dict)
        print(
            f"Currency '{currency_code}' removed from group '{group_name}'\n")
    else:
        print(
            f"Currency '{currency_code}' not found in group '{group_name}'\n")

    return group_dict


#Функция показать все группы с курсами
def show_all_groups(group_dict, currency_dict):
    print("\n-- All Groups --\n")
    if not group_dict:
        print("No groups created yet\n")
        return
    for group_name, currency_codes in group_dict.items():
        print(f"Group: {group_name}")
        say(70, "-")
        if not currency_codes:
            print("  (empty group)")
        else:
            for i in currency_codes:
                if i in currency_dict:
                    info_dict = currency_dict[i]
                    print(f"  {i} - {
                    info_dict['Name']}: {info_dict['Value']:.4f} RUB")
                else:
                    print(f"  {i} - (unknown currency)")
        say(1)


#Функция показать конкретную группу
def show_specific_group(
        group_dict, currency_dict):
    print("\n-- Show Group --\n")
    if not group_dict:
        print("No groups created yet\n")
        return

    print("Available groups:")
    for i in group_dict:
        print(f"  - {i}")
    say(1)
    group_name = input_string("Select group name: ")
    if group_name not in group_dict:
        say("er", "group")
        return

    print(f"\nGroup: {group_name}")
    say(70, "-")
    if not group_dict[group_name]:
        print("  (empty group)")
    else:
        for i in group_dict[group_name]:
            if i in currency_dict:
                info_dict = currency_dict[i]
                print(f"  {i} - {info_dict['Name']}: {
                info_dict['Value']:.4f} RUB")
            else:
                print(f"  {i} - (unknown currency)")
    print("\n")


#Главная часть
say("s")
print("--- Currency Rates ---\n")
currency_dict_main = get_currency_data()
group_dict_main = edit_groups("LOAD")
while True:
    print("1) Show all currencies")
    print("2) Show currency by code")
    print("3) Create group")
    print("4) Add currency to group")
    print("5) Remove currency from group")
    print("6) Show all groups")
    print("7) Show specific group")
    print("8) Exit\n")
    select = input("> Select mode (1-8): ").strip()
    if select == "1":
        show_all_currencies(currency_dict_main)
    elif select == "2":
        show_currency_by_code(currency_dict_main)
    elif select == "3":
        group_dict_main = create_group(group_dict_main)
    elif select == "4":
        group_dict_main = add_currency_to_group(
            currency_dict_main, group_dict_main)
    elif select == "5":
        group_dict_main = remove_currency_from_group(group_dict_main)
    elif select == "6":
        show_all_groups(group_dict_main, currency_dict_main)
    elif select == "7":
        show_specific_group(group_dict_main, currency_dict_main)
    elif select == "8":
        print("\nExiting")
        break
    else:
        say("er", "mode")
    new_currency_dict = get_currency_data()
    if new_currency_dict is not None:
        currency_dict_main = new_currency_dict
say("e")
