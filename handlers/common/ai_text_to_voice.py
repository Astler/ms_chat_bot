import random
from typing import Optional

import requests
from aiogram import types, Router, F
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile
import json
import os

from data.strings import glados_morning_messages

text_to_voice_router = Router()

voices = {
    "peter": "a84d19016bc34098b3c89d78f9299e33",
    "elon": "03397b4c4be74759b72533b663fbd001",
    "junkrat": "f18c58dc032c4c84b5c8a9b113dd36d8",
    "erik": "b4f55643a15944e499defe42964d2ebf",
    "van": "ac3e2eee47a1414d8e705613f7e5aca7",
    "heavy": "89241e36180e44bf85dadebd49871819",
    "glados": "ee885900b0874d12b1c3439d1e56cc95",
    "dude": "45a8f6b326c64fdd9321e2dabd6f6280",
    "junko": "d2feb61a72b64a87aa8e4775ebe35d0c",
    "spy": "fcca5dc25f6842ea8c0b1e16268f9d1c",
    "vox": "920a9f10d1394493a62e20ec7e6c110f",
    "deadpool": "8788e1f6157948fe9efcc509b152b50d",
}


@text_to_voice_router.message(Command(commands=["morning_say_test"]))
async def morning_say_test(message: types.Message, command: CommandObject):
    await message.reply("Morning!")

    glados_message = random.choice(glados_morning_messages)

    audio_content = await text_to_voice(glados_message, "glados")

    if audio_content:
        with open("morning_message.mp3", "wb") as audio_file:
            audio_file.write(audio_content)
        audio = FSInputFile("morning_message.mp3")
        await message.reply_voice(audio)
        os.remove("morning_message.mp3")
    else:
        await message.reply(glados_message)


@text_to_voice_router.message(Command(commands=["say"]))
async def bot_ai(message: types.Message, command: CommandObject):
    if not command.args:
        await message.reply("Please provide some text after the /say command.")
        return

    args = command.args.split()

    if args[0].lower() in voices:
        voice = args[0].lower()
        text = ' '.join(args[1:])
    else:
        voice = "junkrat"
        text = command.args

    if not text:
        await message.reply("Please provide some text to speak.")
        return

    audio_content = await text_to_voice(text, voice)

    if audio_content:
        with open("output.mp3", "wb") as audio_file:
            audio_file.write(audio_content)
        audio = FSInputFile("output.mp3")
        await message.reply_voice(audio)
        os.remove("output.mp3")
    else:
        await message.reply("An error occurred while processing your request.")


async def text_to_voice(text: str, voice: str = "glados") -> Optional[bytes]:
    url = "https://api.fish.audio/v1/tts"

    payload = {
        "text": text,
        "reference_id": voices.get(voice, voices["glados"]),
    }

    headers = {
        "Authorization": "Bearer f912f33e526c4783ae425e7cdc471a4f",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()

        if response.headers.get('Content-Type') == 'application/json':
            error_data = response.json()
            print(f"Error: {error_data.get('message', 'Unknown error occurred')}")
            return None
        else:
            return response.content

    except requests.RequestException as e:
        print(f"An error occurred while processing your request: {str(e)}")
        return None