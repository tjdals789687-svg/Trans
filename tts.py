from __future__ import annotations

import os
import hashlib
from typing import Dict, Optional

from config import TTS_ENABLED, AUDIO_DIR, TTS_MODELS


_tts_cache: Dict[str, "TTS"] = {}


def _safe_import_tts() -> Optional["TTS"]:
    
    if not TTS_ENABLED:
        return None

    try:
        from TTS.api import TTS  # type: ignore
        return TTS
    except Exception:
        return None


def is_available() -> bool:
    return _safe_import_tts() is not None


def generate_audio_filename(text: str, language: str) -> str:
    base = f"{language}:{text}".encode("utf-8")
    digest = hashlib.md5(base).hexdigest()[:16]
    return f"tts_{language}_{digest}.wav"


def synthesize(text: str, language: str = "en") -> Dict[str, Optional[str]]:
    text = (text or "").strip()
    language = (language or "en").strip().lower() or "en"

    if not text:
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": "Text is empty.",
        }

    TTS = _safe_import_tts()
    if TTS is None:
        if not TTS_ENABLED:
            err = "TTS is disabled in config.TTS_ENABLED."
        else:
            err = "TTS library (coqui-TTS) is not installed. Install 'TTS>=0.22.0'."
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": err,
        }

    model_name = TTS_MODELS.get(language, TTS_MODELS.get("en"))

    if model_name is None:
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": f"No TTS model configured for language '{language}'.",
        }

    if language not in _tts_cache:
        _tts_cache[language] = TTS(model_name=model_name, progress_bar=False)
    tts_model = _tts_cache[language]

    os.makedirs(AUDIO_DIR, exist_ok=True)

    filename = generate_audio_filename(text, language)

    audio_path_fs = os.path.join(AUDIO_DIR, filename)

    try:
        tts_model.tts_to_file(text=text, file_path=audio_path_fs)
    except Exception as e:
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": f"TTS synthesis failed: {e}",
        }

    audio_path = f"{AUDIO_DIR}/{filename}".replace("\\", "/")
    audio_url = f"/static/audio/{filename}"

    return {
        "success": True,
        "audio_path": audio_path,
        "audio_url": audio_url,
        "error": None,
    }


#if __name__ == "__main__":
#    sample_text = "Hello, world!"
#    sample_lang = "en"

#    if not is_available():
#        print("TTS is not available. Check config.TTS_ENABLED and TTS installation.")
#    else:
#        result = synthesize(sample_text, sample_lang)
#        print(result)