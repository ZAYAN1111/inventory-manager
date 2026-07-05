import os
import sys
from pathlib import Path
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


# Look for toolow.mp3 in the same directory as this script
SCRIPT_DIR = Path(__file__).parent  # audio_player.py is in project root
SOUND_FILE = SCRIPT_DIR / "toolow.mp3"


class AudioPlayer:
    """Simple audio player for playing toolow.mp3 sound effects."""
    
    _instance = None
    _player = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._player is None:
            self._player = QMediaPlayer()
            self._output = QAudioOutput()
            self._output.setVolume(80 / 100.0)  # Set to 80% volume by default
            self._player.setAudioOutput(self._output)
    
    def set_volume(self, volume):
        """Set volume 0-100."""
        self._output.setVolume(volume / 100.0)
    
    def play_low_stock_alert(self):
        """Play the toolow.mp3 sound if it exists."""
        print(f"[Audio] Looking for: {SOUND_FILE}", file=sys.stderr)
        print(f"[Audio] Absolute path: {SOUND_FILE.resolve()}", file=sys.stderr)
        
        if not os.path.exists(SOUND_FILE):
            print(f"[Audio] Warning: {SOUND_FILE} not found", file=sys.stderr)
            return
        
        try:
            from PySide6.QtCore import QUrl
            abs_path = SOUND_FILE.resolve()
            url = QUrl.fromLocalFile(str(abs_path))
            
            print(f"[Audio] Playing: {abs_path}", file=sys.stderr)
            self._player.setSource(url)
            self._player.play()
            print(f"[Audio] Playback started", file=sys.stderr)
        except Exception as e:
            print(f"[Audio] Error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
