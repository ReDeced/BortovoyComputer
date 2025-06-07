from MOTVOY_III import MOTVOY_III

import speech_recognition as sr
import os
from tkinter import Tk, filedialog
import win32com.client

root = Tk()
root.withdraw()

def listen_for_activation(recognizer, microphone):
    with microphone as source:
        print("Ожидание активационной фразы 'Ало, компьютер'...")
        recognizer.adjust_for_ambient_noise(source)  # Уменьшение фонового шума
        audio = recognizer.listen(source)

    try:
        # Распознаем речь с помощью Google Web Speech API (русский язык)
        phrase = recognizer.recognize_google(audio, language="ru-RU").lower()
        print(f"Распознано: {phrase}")

        if "алло компьютер" in phrase or "компьютер алло" in phrase:
            print("Слушаю...")
            return True
    except sr.UnknownValueError:
        pass  # Речь не распознана
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")

    return False


def listen_command(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    command = ""
    try:
        command = recognizer.recognize_google(audio, language="ru-RU")
        print(f"Вы сказали: {command}")
    except sr.UnknownValueError:
        print("Не удалось распознать команду")
    except sr.RequestError as e:
        print(f"Ошибка сервиса распознавания: {e}")

    return command


def main():
    motvoy = MOTVOY_III()

    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    running = True
    while running:
        try:
            if listen_for_activation(recognizer, microphone):
                motvoy.say("", output_path="assets/listening.wav")
                command = listen_command(recognizer, microphone).lower()
                if command != "":
                    if command.split()[0] == "скажи":
                        motvoy.say(" ".join(command.split()[1:]))

                    elif command.split()[0] == "запусти" or command.split()[0] == "открой":
                        try:
                            os.startfile(os.path.join("shortcuts", f"{' '.join(command.split()[1:])}.lnk"))
                            motvoy.say("", output_path="assets/opening.wav")
                        except FileNotFoundError:
                            motvoy.say("", output_path="assets/chose_file_for_shortcut.wav")
                            file_path = filedialog.askopenfilename(title="Выберите файл")

                            if file_path:
                                os.makedirs(f"./shortcuts", exist_ok=True)
                                shortcut_path = os.path.join("shortcuts", f"{' '.join(command.split()[1:])}.lnk")

                                shell = win32com.client.Dispatch("WScript.Shell")
                                shortcut = shell.CreateShortCut(shortcut_path)
                                shortcut.TargetPath = file_path
                                shortcut.WorkingDirectory = os.path.dirname(file_path)
                                shortcut.Save()

                                os.startfile(os.path.join("shortcuts", f"{' '.join(command.split()[1:])}.lnk"))
                                motvoy.say("", output_path="assets/opening.wav")

                    elif command == "работа завершена":
                        running = False

                    elif command == "выключи windows":
                        os.system("shutdown /s /f /t 1")
                        running = False

                    else:
                        print(command)

        except KeyboardInterrupt:
            running = False

    motvoy.close()

if __name__ == "__main__":
    main()