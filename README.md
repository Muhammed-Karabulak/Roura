# Roura — Programmable Voice Assistant
 
Roura is a lightweight, keyword-based voice assistant for Windows. Unlike conventional AI assistants, Roura does not interpret natural language or infer intent. It listens for specific spoken keywords and executes the Python function mapped to that keyword. If a spoken word or phrase is not present in the command pool, nothing happens.
 
Roura is not intended to be used out of the box. It is a foundation — you bring your own commands.
 
---
 
## How It Works
 
Roura continuously listens through the microphone. When it detects speech, it converts it to text using an offline speech recognition model (Vosk) and checks whether the recognized text matches any registered command keyword. If a match is found, the associated function is called. If not, the input is ignored.
 
There is no AI reasoning, no fuzzy matching, and no internet dependency for core functionality.
 
---
 
## Command Types
 
Roura supports three types of commands, all registered through the `CommadSystem` class.
 
### 1. Parameterless Commands
 
A command registered only in the default command dictionary. It is triggered by saying the command keyword alone, with no additional words.
 
```
"clear computer"  →  clears the screen
```
 
### 2. Parameterized Commands
 
A command registered only in the parameterized command dictionary. It requires at least one word spoken after the command keyword. Everything spoken after the keyword is passed to the function as a single string.
 
```
"youtube funny cat videos"  →  calls youtube_func("funny cat videos")
```
 
If the command accepts multiple logical parameters, the function itself is responsible for splitting and processing that string.
 
### 3. Overloaded Commands (Parameterless + Parameterized)
 
A command registered in **both** dictionaries under the same keyword. Roura automatically selects the correct version at runtime:
 
- If additional words are spoken after the keyword → the **parameterized** version runs.
- If only the keyword is spoken → the **parameterless** version runs.
```
"search"              →  opens the search interface (no parameter)
"search python docs"  →  performs a search for "python docs" (with parameter)
```
 
---
 
## Chaining Commands with `and`
 
Multiple commands can be executed in a single utterance by separating them with the word `and`.
 
```
"youtube lofi music and clear computer"
```
 
Roura splits on `and` and processes each segment as an independent command. For parameterized commands, the parameter ends at the `and` keyword.
 
```
"search open source and clear"
→  search("open source")  +  clear()
```
 
---
 
## Built-in Control Commands
 
The following commands are built into the assistant and do not need to be registered manually.
 
| Command   | Description                                             |
|-----------|---------------------------------------------------------|
| `close`   | Pauses voice listening. The assistant stops processing spoken input. |
| `open`    | Resumes voice listening after it has been closed.       |
| `restart` | Fully restarts the assistant process.                   |
| `kill`    | Terminates the program entirely.                        |
 
---
 
## Project Structure
 
```
Roura/
├── Modules/
│   ├── CommandSys.py      # Command registration and dispatch logic
│   ├── SpeechToText.py    # Microphone capture and Vosk-based recognition
│   └── TextToSpeech.py    # Spoken feedback output
├── Roura.py               # Main controller and entry point
├── Roura.bat              # Windows launcher script
├── Restart.bat            # Restart helper script
├── requirements.txt       # Python dependencies
└── README.md
```
 
---
 
## Requirements
 
- Python 3.10 or later
- Windows (certain commands rely on Windows-specific system calls)
- [ffmpeg](https://ffmpeg.org/) — required by `pydub` for audio playback and processing
- Vosk speech recognition model: `vosk-model-small-en-us-0.15`
> The model folder is **not included** in this repository. Download it separately from the [official Vosk models page](https://alphacephei.com/vosk/models) and place the extracted `vosk-model-small-en-us-0.15` folder in the project root before running.
 
---
 
## Installation
 
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```
 
---
 
## Running
 
```bash
python Roura.py
```
 
Or launch via the provided batch file:
 
```
Roura.bat
```
 
---
 
## Adding Custom Commands
 
Roura is designed to be extended. All custom commands are registered through the `CommadSystem` class.
 
### Step 1 — Write the command function
 
It is strongly recommended to define your command functions inside a dedicated `Commands` class to avoid potential conflicts with Roura's internal namespace.
 
```python
class Commands:
    def open_browser(self):
        import webbrowser
        webbrowser.open("https://www.google.com")
 
    def search_web(self, query: str):
        import webbrowser
        webbrowser.open(f"https://www.google.com/search?q={query}")
```
 
### Step 2 — Register the commands in the `CommadSystem` dictionaries
 
Commands are stored in dictionaries where the **key** is the spoken keyword Roura listens for, and the **value** is the function to call.
 
**Parameterless command** — add to the default commands dict:
 
```python
"open browser": commands.open_browser
```
 
**Parameterized command** — add to the parameterized commands dict:
 
```python
"search": commands.search_web
```
 
**Overloaded command** — add the same keyword to **both** dicts with the appropriate function in each.
 
### Parameter Handling
 
If a parameterized command function receives multi-part input (e.g. `"set timer 5 minutes"`), all words after the keyword arrive as a single string. The function is responsible for parsing that string as needed.
 
```python
def set_timer(self, args: str):
    parts = args.split()
    amount = parts[0]
    unit = parts[1] if len(parts) > 1 else "minutes"
    # ...
```
 
---
 
## License
 
This project is licensed under the [GNU General Public License v3.0](LICENSE).
 
## Contributing
 
See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.