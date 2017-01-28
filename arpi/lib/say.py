import tempfile
import hashlib
import pathlib
import threading
import subprocess
import enum

from gtts import gTTS



def _say(filepath, mode, kill_event):
    print( "DEBUG: playing", filepath )
    
    mplayer = ["mplayer","-af", "scaletempo", "-speed", ]
    if mode == "slow":
        mplayer += ["0.7"]
    else:
        mplayer += ["0.9"]
    
    process = subprocess.Popen(mplayer + [str(filepath)])
    
    while True:
        if kill_event.wait(1):
            print( "DEBUG: playing (killed)", filepath )
            process.terminate()
            break
        if process.poll() is not None:
            break
    
    print( "DEBUG: playing (finished)", filepath )


class EngineEnum(enum.Enum):
    gTTS = "gTTS"
    pico2wave = "pico2wave"


class Say:
    def __init__(self, globalconfig):
        self._globalconfig = globalconfig
        
        self._locale = globalconfig.locale.replace("_","-") # used by pico2wave
        self._language = globalconfig.language # used by google
        self._tmpdirpath = pathlib.Path(tempfile.mkdtemp(prefix="tmp-say"))
        
        self._engine = EngineEnum.pico2wave
        #self._engine = EngineEnum.gTTS
        
        self._current_thread = None
        self._current_thread_kill_event = threading.Event()
        self._current_thread_lock = threading.Lock()
    
    def __call__(self, text, mode="normal", blocking=False):
        print("DEBUG: say:", text)
        
        if not mode in ("normal","slow"):
            raise RuntimeError("Unknown mode '{}'".format(mode))
        
        filename = hashlib.sha256(text.encode("utf8")).hexdigest() + ".wav"
        filepath = self._tmpdirpath / filename
        
        # avoid unnecessary regeneration
        if not filepath.exists():
            print("DEBUG: say (generation)")
            self._create_file( filepath, text)
        
        print("DEBUG: say (output)")
        with self._current_thread_lock:
            # stop current thread
            if self._current_thread:
               self._current_thread_kill_event.set()
               self._current_thread.join()
            
            # start new thread
            self._current_thread_kill_event.clear()
            self._current_thread = threading.Thread(target=_say, args=(filepath,mode,self._current_thread_kill_event))
            self._current_thread.start()
        
        # block if desired
        if blocking:
            self._current_thread.join()
        
    
    def _create_file(self, filepath, text):
        if self._engine == EngineEnum.gTTS:
            tts = gTTS(text=text, lang=self._language)
            tts.save(str(filepath))
        elif self._engine == EngineEnum.pico2wave:
            subprocess.check_call(["pico2wave", "--lang", self._locale, "--wave", str(filepath), text])
        else:
            raise RuntimeError("Unknown engine '{}'".format(self._engine))
        
