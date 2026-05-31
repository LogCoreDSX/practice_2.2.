#task 2.2

import psutil
import time


# Константы
MIN_REFRESH = 1
MAX_REFRESH = 60
EXIT_CHECK_INTERVAL = 10


#Функция быстрый вывод частых сообщений
def say(mode0= " ", mode1= " "):  # Быстрый вывод частых сообщений
    if mode0 == "s": print("<--- Beginning work Program --->\n")
    elif mode0 == "e": print("\n<--- End work Program --->")
    elif mode0 == "er":
        if mode1 == "num_nat": print(f"Error. Only NUMBER > {MIN_REFRESH}!\n")
        elif mode1 == "num_no": print("Error. Only NUMBER !\n")
        elif mode1 == "exit": print("Error. Enter 'y' or 'n' !\n")


#Функция ввод чисел с проверкой
def input_number_interval():
    num = 0
    while True:
        try:
            num = int(input("> Enter refresh interval (seconds) = "))
        except ValueError:
            say("er", "num_no")
            continue
        if num < MIN_REFRESH:
            say("er", "num_nat")
            continue
        if num > MAX_REFRESH:
            print(f"Error: {num} seconds is a long interval\n")
        break
    return num


#Функция получение инфо о статусе компьютера
def get_info_system(mode):
    if mode == "cpu":
        return psutil.cpu_percent(interval = 1)
    elif mode == "ram":
        memory_tuple = psutil.virtual_memory()
        return memory_tuple.percent
    elif mode == "disk":
        disk_tuple = psutil.disk_usage('/')
        return disk_tuple.percent
    return 0

#Функция проверка желания выйти каждые N циклов
def check_exit(cycle_count):
    if cycle_count % EXIT_CHECK_INTERVAL == 0:
        print("\n- Continue monitor operation or exit - ")
        print("Enter 'y' for exit else enter 'space' for continue" )
        while True:
            select = input("\n> Enter select: ").strip().lower()
            if select == 'y':
                return True
            else:
                print("\n- Continuing monitoring - ")
                return False
    return False


#Главная часть
say("s")
print("\n<-- System Monitor -->\n")
print("- System Monitor Configuration -")
print(f"Minimal refresh = {MIN_REFRESH} sec")
print(f"Maximal refresh = {MAX_REFRESH} sec\n")
refresh_seconds = input_number_interval()
print(f"\n-- Starting monitoring --\nRefresh every {refresh_seconds} sec")
print(f"Program will ask to exit every {EXIT_CHECK_INTERVAL} cycles")
cycle_counter = 0
try:
    while True:
        cycle_counter += 1
        print(f"\n-- Time : {time.strftime('%H:%M:%S')} --\n")
        cpu_percent = get_info_system("cpu")
        memory_percent = get_info_system("ram")
        disk_percent = get_info_system("disk")
        print(f"Load CPU = {cpu_percent}%")
        print(f"Used RAM = {memory_percent}%")
        print(f"Disk Occupancy = {disk_percent}%")
        with open('resource/result/system_monitor.log', 'a') as log_file:
            log_file.write(
                f"{time.strftime('%Y-%m-%d %H:%M:%S')} - CPU:{cpu_percent}%"
                f" RAM:{memory_percent}% DISK OCCUPANCY:{disk_percent}%\n")
        if check_exit(cycle_counter):
            break
        time.sleep(refresh_seconds)
except KeyboardInterrupt:
    print("\n")
finally:
    print("\n- Monitoring finished -")
    print(f"Total cycles completed: {cycle_counter}")
    print("Log saved in resource/result/system_monitor.log")
    say("e")
