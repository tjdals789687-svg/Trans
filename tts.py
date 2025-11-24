from __future__ import annotations

import os
import hashlib
from typing import Dict, Optional

from config import TTS_ENABLED, AUDIO_DIR, TTS_MODELS

# 언어별 TTS 모델 캐시
_tts_cache: Dict[str, "TTS"] = {}


def _safe_import_tts() -> Optional["TTS"]:
    """
    Coqui TTS 라이브러리를 안전하게 임포트.
    - config.TTS_ENABLED 가 False 이면 None 반환
    - 라이브러리가 설치 안 되어 있어도 None 반환
    """
    if not TTS_ENABLED:
        return None

    try:
        from TTS.api import TTS  # type: ignore
        return TTS
    except Exception:
        return None


def is_available() -> bool:
    """
    TTS 기능 사용 가능 여부 확인.
    - config.TTS_ENABLED 플래그
    - Coqui TTS 라이브러리 설치 여부
    둘 다 만족해야 True
    """
    return _safe_import_tts() is not None


def generate_audio_filename(text: str, language: str) -> str:
    """
    텍스트 + 언어 기반으로 고유한 파일 이름 생성.
    너무 길어지지 않도록 MD5 해시 사용.
    """
    base = f"{language}:{text}".encode("utf-8")
    digest = hashlib.md5(base).hexdigest()[:16]
    return f"tts_{language}_{digest}.wav"


def synthesize(text: str, language: str = "en") -> Dict[str, Optional[str]]:
    """
    실제로 음성 파일을 생성하는 핵심 함수.

    반환 형식(dict):
        {
            "success": True/False,
            "audio_path": "static/audio/tts_xxx.wav" 또는 None,
            "audio_url": "/static/audio/tts_xxx.wav" 또는 None,
            "error": 에러 메시지 또는 None
        }
    """
    # 0. 입력 정리
    text = (text or "").strip()
    language = (language or "en").strip().lower() or "en"

    if not text:
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": "Text is empty.",
        }

    # 1. TTS 라이브러리 임포트 + 사용 가능 여부 확인
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

    # 2. 모델 선택 (config.TTS_MODELS 사용)
    #    언어 키가 없으면 영어(en) 모델로 fallback
    model_name = TTS_MODELS.get(language, TTS_MODELS.get("en"))

    if model_name is None:
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": f"No TTS model configured for language '{language}'.",
        }

    # 3. 모델 로드 (언어별로 캐싱)
    if language not in _tts_cache:
        _tts_cache[language] = TTS(model_name=model_name, progress_bar=False)
    tts_model = _tts_cache[language]

    # 4. 오디오 파일 저장 경로 준비
    #    AUDIO_DIR 은 config.py 에서 'static/audio' 로 설정되어 있다고 가정
    os.makedirs(AUDIO_DIR, exist_ok=True)

    filename = generate_audio_filename(text, language)
    # 실제 파일 시스템 경로
    audio_path_fs = os.path.join(AUDIO_DIR, filename)

    # 5. 음성 파일 생성
    try:
        tts_model.tts_to_file(text=text, file_path=audio_path_fs)
    except Exception as e:
        return {
            "success": False,
            "audio_path": None,
            "audio_url": None,
            "error": f"TTS synthesis failed: {e}",
        }

    # 6. Flask 에서 쓸 경로/URL 형식으로 정리
    #    - audio_path: 프로젝트 기준 상대 경로 (static/audio/...)
    #    - audio_url : 브라우저에서 접근할 URL (/static/audio/...)
    audio_path = f"{AUDIO_DIR}/{filename}".replace("\\", "/")
    audio_url = f"/static/audio/{filename}"

    return {
        "success": True,
        "audio_path": audio_path,
        "audio_url": audio_url,
        "error": None,
    }


if __name__ == "__main__":
    """
    단독 실행 테스트:
        python tts.py
    """
    sample_text = "Hello, world!"
    sample_lang = "en"

    if not is_available():
        print("TTS is not available. Check config.TTS_ENABLED and TTS installation.")
    else:
        result = synthesize(sample_text, sample_lang)
        print(result)