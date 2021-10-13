import gtts
import os
from io import TextIOWrapper
from typing import NamedTuple
import glob
import json
from datetime import datetime


class Conf(NamedTuple):
    generationCharacters: str
    script_dir: str
    output_dir: str

def read_json_conf() -> Conf:
    f = open('conf.json', "r")
    data = json.loads(f.read())
    f.close()
    return Conf(
        generationCharacters=data['generationCharacters'],
        script_dir=data['script_dir'],
        output_dir=data['output_dir'],
    )

class Script(NamedTuple):
    description: str
    character: str
    dialog: str

def ReadScriptFile(file: TextIOWrapper) -> Script: 
    characterPrefix, character = file.readline().removesuffix('\n').split(": ")
    description = os.path.splitext(os.path.basename(file.name))[0]
    dialog = file.read().removeprefix('\n').removesuffix('\n').replace('\n', ' ')
    if (characterPrefix == "Character") and (character) and (dialog):
        return Script(description, character, dialog)
    raise ValueError(f'{file.name} is not a script file')

def GetScripts(path: str) -> list[Script]:
    scripts: list[Script] = []
    filenames = glob.glob(path + '/**/*.txt', recursive=True)
    for filename in filenames:
        if filename.endswith(".txt"):
            with open(filename) as f:
                try:
                    scripts.append(ReadScriptFile(f))
                except ValueError as e:
                    print(f'* ERROR reading .txt file {filename}: {e}')
    return scripts

def GetExistingMP3s(path: str) -> list[str]:
    filenames = glob.glob(path + '/**/*.mp3', recursive=True)
    existing_mp3s: list[str] = []
    for filename in filenames:
        existing_mp3s.append(os.path.splitext(os.path.basename(filename))[0])
    return existing_mp3s

print("*** SCRIPT TO SPEECH")

conf = read_json_conf()

print(f'*** Generating for character "{conf.generationCharacters}"\n')
scripts = GetScripts(conf.script_dir)
existing_mp3s = GetExistingMP3s(conf.output_dir)
for script in scripts:
    if (script.character in conf.generationCharacters):
        if (script.description not in existing_mp3s):
            print(f'{datetime.now().strftime("%H:%M:%S")} GENERATING {script.description}')
            tts = gtts.gTTS(script.dialog)
            tts.save(f"{conf.output_dir}/{script.description}.mp3")
        else:
            print(f'{datetime.now().strftime("%H:%M:%S")} SKIPPING {script.description}: mp3 already exists')
    else:
        print(f'{datetime.now().strftime("%H:%M:%S")} SKIPPING {script.description}: character {script.character} not in generation list')

print(f'{datetime.now().strftime("%H:%M:%S")} FINISHED')
