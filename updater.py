import requests


repo = "https://raw.githubusercontent.com/ReDeced/BortovoyComputer/refs/heads/master"

print("Проверка версий")
last_version = requests.get(f"{repo}/version.txt").text
with open("version.txt", "r", encoding="utf-8") as version_file:
    current_version = version_file.read()

if current_version != last_version:
    print("Обновление")
    with open("MOTVOY_III.py", "w", encoding="utf-8") as file:
        file.write(requests.get(f"{repo}/MOTVOY_III.py").text)
    with open("generate_voice.py", "w", encoding="utf-8") as file:
        file.write(requests.get(f"{repo}/generate_voice.py").text)
    with open("main.py", "w", encoding="utf-8") as file:
        file.write(requests.get(f"{repo}/main.py").text)
    with open("version.txt", "w", encoding="utf-8") as file:
        file.write(last_version)
    print("Обновление завершено")

print("Запуск")