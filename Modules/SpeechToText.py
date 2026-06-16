from vosk import Model, KaldiRecognizer
from pyaudio import PyAudio, paInt16
from json import loads

from os.path import abspath, dirname, join

class SpeechToText:
    """Vosk-based real-time speech-to-text component."""
    def __init__(
        self,
        sample_rate: int = 16000,
        chunk_size: int = 2000,
        on_final=(lambda text: print(text)),
    ):
        """Initializes configuration required for the speech recognition model,
        recognizer, and microphone stream."""
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

        self.final_fonk = on_final

        self._model = Model(self.resource_path("vosk-model-small-en-us-0.15"))
        self._rec = KaldiRecognizer(self._model, self.sample_rate)
        self._pa = PyAudio()
        self._stream = None

    def resource_path(self, relative_path):
        """Returns an absolute resource file path relative to the project root."""
        base = dirname(dirname(abspath(__file__)))
        return join(base, relative_path)

    def start(self):
        """Opens and starts the input stream for reading from the microphone."""
        self._stream = self._pa.open(
            format=paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        self._stream.start_stream()

    def CatchSpeech(self):
        """Processes an audio chunk and sends completed sentences to the callback."""
        data = self._stream.read(self.chunk_size, exception_on_overflow=False)

        # sentence complite
        if self._rec.AcceptWaveform(data):
            result = loads(self._rec.Result())
            if result["text"]:
                self.final_fonk(result["text"])
        del data

    def stop(self):
        """Safely closes the open audio stream and the PyAudio resources."""
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
        self._pa.terminate()
