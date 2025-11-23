# translator.py
# 번역 기능 담당 모듈
# 담당: 번역 팀원

from transformers import MarianMTModel, MarianTokenizer
import torch
from config import SUPPORTED_LANGUAGE_PAIRS, MAX_TOKEN_LENGTH

# ============================================
# 모델 캐시
# ============================================
_model_cache = {}

def get_model(source_lang: str, target_lang: str):
    """
    번역 모델을 가져옵니다. (캐싱 적용)
    
    Args:
        source_lang: 원본 언어 코드 (예: 'en')
        target_lang: 대상 언어 코드 (예: 'ko')
    
    Returns:
        (tokenizer, model) 튜플 또는 (None, None)
    """
    cache_key = f"{source_lang}-{target_lang}"
    
    # 캐시 확인
    if cache_key in _model_cache:
        print(f"✅ [Translator] 캐시에서 모델 로드: {cache_key}")
        return _model_cache[cache_key]
    
    # 새로 로드
    print(f"📥 [Translator] 모델 다운로드 중: {cache_key}")
    
    try:
        model_name = f"Helsinki-NLP/opus-mt-{source_lang}-{target_lang}"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        
        # 캐시에 저장
        _model_cache[cache_key] = (tokenizer, model)
        print(f"✅ [Translator] 모델 로드 완료: {cache_key}")
        
        return tokenizer, model
        
    except Exception as e:
        print(f"❌ [Translator] 모델 로드 실패: {cache_key} - {str(e)}")
        return None, None


def translate(text: str, source_lang: str, target_lang: str) -> dict:
    """
    텍스트를 번역합니다.
    
    Args:
        text: 번역할 텍스트
        source_lang: 원본 언어 코드
        target_lang: 대상 언어 코드
    
    Returns:
        {
            'success': bool,
            'translated': str or None,
            'error': str or None
        }
    """
    # 언어 쌍 유효성 검사
    lang_pair = f"{source_lang}-{target_lang}"
    if lang_pair not in SUPPORTED_LANGUAGE_PAIRS:
        return {
            'success': False,
            'translated': None,
            'error': f'지원하지 않는 언어 쌍: {lang_pair}'
        }
    
    # 모델 가져오기
    tokenizer, model = get_model(source_lang, target_lang)
    
    if tokenizer is None or model is None:
        return {
            'success': False,
            'translated': None,
            'error': f'모델을 로드할 수 없습니다: {lang_pair}'
        }
    
    try:
        # 토큰화
        inputs = tokenizer(
            text,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=MAX_TOKEN_LENGTH
        )
        
        # 번역 수행
        with torch.no_grad():
            translated = model.generate(**inputs)
        
        # 디코딩
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        
        return {
            'success': True,
            'translated': result,
            'error': None
        }
        
    except Exception as e:
        return {
            'success': False,
            'translated': None,
            'error': f'번역 중 오류: {str(e)}'
        }


def get_cached_models() -> list:
    """현재 캐시된 모델 목록 반환"""
    return list(_model_cache.keys())


def clear_cache():
    """모델 캐시 초기화 (메모리 해제)"""
    global _model_cache
    _model_cache = {}
    print("🗑️ [Translator] 모델 캐시 초기화됨")


# ============================================
# 테스트용
# ============================================
if __name__ == '__main__':
    # 단독 실행 시 테스트
    print("=" * 50)
    print("🧪 Translator 모듈 테스트")
    print("=" * 50)
    
    test_text = "Hello, how are you?"
    print(f"\n원본: {test_text}")
    
    result = translate(test_text, 'en', 'ko')
    
    if result['success']:
        print(f"번역: {result['translated']}")
    else:
        print(f"에러: {result['error']}")
    
    print(f"\n캐시된 모델: {get_cached_models()}")
