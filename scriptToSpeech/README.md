# Script to Speech

## Script File Format

A script file is used to generate the audio output
The script file name (with path and extension stripped) is the name of the audio file produced
Script .txt files should have the following format:

    Character: <character>
    
    <script line>
    ....
    <script line>
    EOF

MP3s will be generated for any script file with "Character: AI".

## Config

Uses a local json config file, check "conf.json.example".
