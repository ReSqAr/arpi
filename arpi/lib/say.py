import tempfile
import hashlib
import pathlib
import threading
import subprocess
import enum


def _say(filepath, mode, kill_event):
    """
        Helper function which just plays a given file
        in an interruptable manner.
    """
    print("DEBUG: playing", filepath)

    mplayer = ["mplayer", "-af", "scaletempo", "-speed", ]
    if mode == "slow":
        mplayer += ["0.7"]
    else:
        mplayer += ["0.9"]

    # play
    process = subprocess.Popen(mplayer + [str(filepath)])

    # check for kill event
    while True:
        if kill_event.wait(1):
            print("DEBUG: playing (killed)", filepath)
            process.terminate()
            break
        if process.poll() is not None:
            break

    print("DEBUG: playing (finished)", filepath)


class EngineEnum(enum.Enum):
    """
        Engine selection helper enum.
    """
    gTTS = "gTTS"  # google
    pico2wave = "pico2wave"
    Mute = "mute"


class Say:
    """
        Objects which encapsulates the TTS functionality.
    """

    def __init__(self, global_config):
        self._global_config = global_config

        # setup internal variables
        self._locale = global_config.locale.replace("_", "-")  # used by pico2wave
        self._language = global_config.language  # used by google
        self._tmp_dir_path = pathlib.Path(tempfile.mkdtemp(prefix="tmp-say"))

        # select engine (with implicit sanity check)
        self._engine = EngineEnum(global_config.config['tts']['engine'])
        print("DEBUG: tts engine: {}".format(self._engine))

        # private variables
        self._current_thread = None
        self._current_thread_kill_event = threading.Event()
        self._current_thread_lock = threading.Lock()

    def __call__(self, text, mode="normal", blocking=False):
        """
            Say the given text.
        """
        print("DEBUG: say:", text)

        if self._engine == EngineEnum.Mute:
            return

        if mode not in ("normal", "slow"):
            raise RuntimeError("Unknown mode '{}'".format(mode))

        filename = hashlib.sha256(text.encode("utf8")).hexdigest() + ".wav"
        filepath = self._tmp_dir_path / filename

        # avoid unnecessary regeneration
        if not filepath.exists():
            print("DEBUG: say (generation)")
            self._create_file(filepath, text)

        print("DEBUG: say (output)")
        with self._current_thread_lock:
            # stop current thread
            if self._current_thread:
                self._current_thread_kill_event.set()
                self._current_thread.join()

            # start new thread
            self._current_thread_kill_event.clear()
            self._current_thread = threading.Thread(target=_say, args=(filepath, mode, self._current_thread_kill_event))
            self._current_thread.start()

        # block if desired
        if blocking:
            self._current_thread.join()

    def _create_file(self, filepath, text):
        """
            Save TTS result to the given file.
        """
        if self._engine == EngineEnum.gTTS:
            from gtts import gTTS
            tts = gTTS(text=text, lang=self._language)
            tts.save(str(filepath))
        elif self._engine == EngineEnum.pico2wave:
            subprocess.check_call(["pico2wave", "--lang", self._locale, "--wave", str(filepath), text])
        else:
            raise RuntimeError("Unknown engine '{}'".format(self._engine))
