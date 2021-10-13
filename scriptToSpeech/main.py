import gtts
import os
from io import TextIOWrapper
from typing import NamedTuple
import glob

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

generationCharacters = ['AI']
my_path = "./../../scripts"
output_path = './../../output'

print(f'Generating MP3s from script .txt files for characters {generationCharacters}')

scripts = GetScripts(my_path)
existing_mp3s = GetExistingMP3s(output_path)
for script in scripts:
    if (script.character in generationCharacters):
        if (script.description not in existing_mp3s):
            print(f'* GENERATING for script {script.description}')
            tts = gtts.gTTS(script.dialog)
            tts.save(f"{output_path}/{script.description}.mp3")
        else:
            print(f'* SKIPPING for script {script.description}, mp3 already exists')
    else:
        print(f'* SKIPPING for script {script.description}, character {script.character} not in generation list')
