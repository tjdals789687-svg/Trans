# 기본 설정
MAX_TEXT_LENGTH = 5000

# 서버 설정
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5000
DEBUG_MODE = False

# 언어 설정
LANGUAGE_NAMES = {
    'en': 'English (영어)',
    'ko': '한국어',
    'ja': '日本語 (일본어)',
    'zh': '中文 (중국어)',
    'es': 'Español (스페인어)',
    'fr': 'Français (프랑스어)',
    'de': 'Deutsch (독일어)',
}

# TTS 설정
TTS_ENABLED = True
AUDIO_DIR = 'static/audio'

# TTS 모델 (단일 언어 모델만)
TTS_MODELS = {
    'en': 'tts_models/en/ljspeech/tacotron2-DDC',
    'es': 'tts_models/es/css10/vits',
    'fr': 'tts_models/fr/css10/vits',
    'de': 'tts_models/de/thorsten/tacotron2-DDC',
}
