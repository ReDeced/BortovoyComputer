import aiohttp.client_exceptions
import simpleaudio
import asyncio
import os
from time import time, sleep
import shutil

from fairseq.data import Dictionary
from pydub import AudioSegment  # Для конвертации аудио

import edge_tts
from rvc_python.infer import RVCInference

import torch

torch.serialization.add_safe_globals([Dictionary])


class MOTVOY_III:
    def __init__(self):
        print("ЗАГРУЗКА")
        os.makedirs(f"./temp", exist_ok=True)
        self.rvc = RVCInference(model_path="./models/MOTVOY_III_a.pth", device="cuda:0")
        self.rvc.load_model("MOTVOY_III_a.pth")
        self.rvc.set_params(f0up_key=2, protect=0.5)
        self.say("Проверка голоса", "assets/voice_check.mp3")
        print("ЗАГРУЗКА ЗАВЕРШЕНА")

    async def _generate_speech(self, text="Введите текст", path = ""):
        communicate = edge_tts.Communicate(
            text=text,
            voice="ru-RU-DmitryNeural",
            rate="+0%",
            volume="+0%",
            pitch="-10Hz"
        )
        dir_name = f"{time()}"
        os.makedirs(f"./temp/{dir_name}", exist_ok=True)  # Создаем папку
        input_path = f"temp/{dir_name}/rvc_input.mp3"
        err = False
        if path != "":
            output_path = f"temp/{dir_name}/rvc_output.wav"
            self.rvc.infer_file(path, output_path)
            return output_path, dir_name

        try:
            await communicate.save(input_path)
            output_path = f"temp/{dir_name}/rvc_output.wav"
            self.rvc.infer_file(input_path, output_path)
            return output_path, dir_name

        except aiohttp.client_exceptions.ClientConnectorDNSError as e:
            print("ОТСУТСТВУЕТ ПОДКЛЮЧЕНИЕ К ИНТЕРНЕТУ")
            output_path = f"assets/no_internet.wav"
            return output_path, dir_name

    def say(self, text, input_path = "", output_path = "", wait=False):
        wav_path = output_path
        if output_path == "":
            wav_path, temp_dir = asyncio.run(self._generate_speech(text, input_path))

        audio = AudioSegment.from_file(wav_path)

        if audio.frame_rate != 44100:
            audio = audio.set_frame_rate(44100)  # Устанавливаем стандартную частоту

            wav_path = wav_path.replace(".wav", "_converted.wav")

        audio.export(wav_path, format="wav")

        wave_obj = simpleaudio.WaveObject.from_wave_file(wav_path)
        play_obj = wave_obj.play()

        if wait:
            play_obj.wait_done()


    def close(self):
        self.say("Завершение работы", wait=True)
        self.rvc.unload_model()
        shutil.rmtree(f"./temp", ignore_errors=False)
        os.mkdir("temp")