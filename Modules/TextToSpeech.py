from os import remove
from os.path import exists
from tempfile import NamedTemporaryFile

from pyttsx3 import Engine, init
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.playback import play

class TextToSpeech:
    """Helper class that converts text to speech and applies robotic effects."""
    def __init__(self):
        """Sets default speech rate, volume, and selects the voice profile to use."""
        self.rate = 150
        self.volume = 0.9
        self.voice_id = self._resolve_voice_id()

    def _resolve_voice_id(self) -> str | None:
        """Finds an appropriate English (preferably male) voice id on the system."""
        engine = init()
        voices = engine.getProperty("voices")
        english_voices = []
        male_voice = None
        for v in voices:
            name = v.name.lower()
            vid = v.id.lower()
            if "english" in name or "en_" in vid:
                english_voices.append(v.id)
                gender = getattr(v, "gender", "").lower()
                if gender == "male" or any(m in name for m in ("david", "male", "john", "michael", "mark", "matthew")):
                    male_voice = v.id
                    break
        if male_voice is not None:
            return male_voice
        if english_voices:
            return english_voices[0]
        return None

    def _init_engine(self) -> Engine:
        """Creates and returns a configured pyttsx3 engine."""
        engine = init()
        engine.setProperty("rate", self.rate)
        engine.setProperty("volume", self.volume)
        if self.voice_id is not None:
            engine.setProperty("voice", self.voice_id)
        return engine

    def _apply_robotic_effect(self, sound: AudioSegment) -> AudioSegment:
        """Applies filters and layering operations to approximate a robotic effect
        on the raw audio segment."""
        original_rate = sound.frame_rate
        sound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(original_rate * 0.888)})
        sound = sound.set_frame_rate(original_rate)

        sound = sound.low_pass_filter(3200).high_pass_filter(120)
        robot_layer = sound - 8
        robot_layer = robot_layer.low_pass_filter(1200)

        sound = sound.overlay(robot_layer, position=30)
        sound = sound + 4
        return normalize(sound)

    def play(self, text: str) -> None:
        """Generate robotic speech from text and play it immediately without saving a permanent file."""
        with NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            temp_path = tmp.name

        engine = self._init_engine()
        try:
            engine.save_to_file(text, temp_path)
            engine.runAndWait()
        finally:
            try:
                engine.stop()
            except Exception:
                pass

        try:
            sound = AudioSegment.from_wav(temp_path)
            sound = self._apply_robotic_effect(sound)
            play(sound)
        finally:
            if exists(temp_path):
                remove(temp_path)
