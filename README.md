# Roura
Roura is a simple desktop assistant that runs on Windows and listens for voice
commands. It connects speech-to-text, command execution, and text-to-speech to
let users control the system and define custom commands.

## Features
- Capture voice commands from the microphone
- Execute built-in commands and user-defined commands
- Support parameterized commands when the command accepts arguments
- Chain multiple commands with `and`
- Speak back executed commands and feedback via text-to-speech

## Command Behavior
Roura supports three kinds of command definitions:

1. **Default-only commands**
   - If a command exists only in the default command table, it runs without
     parameters.
   - Example: `clear computer`

2. **Commands in both default and parameterized tables**
   - If a command exists in both tables, Roura chooses the parameterized version
     when parameters are provided.
   - If no parameters are provided, the default version runs.
   - Example: a command can work both as `music` and `music <term>`.

3. **Parameterized-only commands**
   - If a command exists only in the parameterized table, it requires a
     parameter.
   - Example: `youtube <query>` must include a query term.

## How to Speak Commands
- Say the command phrase first.
- If the command accepts parameters, continue by speaking the parameter.
- To run multiple commands in a row, speak the first command, then say `and`,
  and then speak the next command.

### Examples
- `youtube funny videos`
- `search open source and clear`

## Requirements
- Python 3.10+
- Windows (some commands depend on Windows-specific utilities)
- ffmpeg (used by pydub for audio playback and processing)

## Installation
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running
```powershell
python Roura.py
```
Or run `Roura.bat`.

## Model Note
The `SpeechToText` component uses the `vosk-model-small-en-us-0.15` model,
which is bundled with this repository in the project root
(`vosk-model-small-en-us-0.15/`).

- No separate download is required — the model is included when you clone
  the repository.
- If you want to use a different or updated Vosk model, replace the
  `vosk-model-small-en-us-0.15` folder with your chosen model and update the
  model path in the code if the folder name changes.

## Contributing
See `CONTRIBUTING.md` for contribution guidelines.

## License
This project is licensed under the [GNU General Public License v3.0](LICENSE).

### Third-Party Notices
This repository bundles the `vosk-model-small-en-us-0.15` speech recognition
model and depends on the `vosk` Python package, both developed by
Alpha Cephei Inc. and distributed under the
[Apache License 2.0](https://github.com/alphacep/vosk-api/blob/master/COPYING).