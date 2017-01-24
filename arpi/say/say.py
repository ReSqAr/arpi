import tempfile
import hashlib
import pathlib
import threading
import subprocess

from gtts import gTTS

def _say(filepath, kill_event):
    print( "DEBUG: playing", filepath )
    process = subprocess.Popen(["mplayer",str(filepath)])
    
    while True:
        if kill_event.wait(1):
            print( "DEBUG: playing (killed)", filepath )
            process.terminate()
            break
        if process.poll() is not None:
            break
    
    print( "DEBUG: playing (finished)", filepath )

class Say:
    def __init__(self, configpath):
        self._configpath = configpath
        
        self._language = "en"
        self._tmpdirpath = pathlib.Path(tempfile.mkdtemp(prefix="tmp-say"))
        
        self._current_thread = None
        self._current_thread_kill_event = threading.Event()
        self._current_thread_lock = threading.Lock()
    
    def __call__(self, text):
        print("DEBUG: say: ", text)
        
        filename = hashlib.sha256(text.encode("utf8")).hexdigest() + ".wav"
        filepath = self._tmpdirpath / filename
        
        # avoid unnecessary regernation
        if not filepath.exists():
            print("DEBUG: say (generation)")
            tts = gTTS(text=text, lang=self._language)
            tts.save(str(filepath))
        
        print("DEBUG: say (output)")
        with self._current_thread_lock:
            # stop current thread
            if self._current_thread:
               self._current_thread_kill_event.set()
               self._current_thread.join()
            
            # start new thread
            self._current_thread_kill_event.clear()
            self._current_thread = threading.Thread(target=_say, args=(filepath,self._current_thread_kill_event))
            self._current_thread.start()
            
