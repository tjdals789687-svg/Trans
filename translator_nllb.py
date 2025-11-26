from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

# NLLB 모델
MODEL_NAME = 'facebook/nllb-200-distilled-600M'

# 언어 코드
LANGUAGE_CODES = {
    'en': 'eng_Latn',
    'ko': 'kor_Hang',
    'ja': 'jpn_Jpan',
    'zh': 'zho_Hans',
    'es': 'spa_Latn',
    'fr': 'fra_Latn',
    'de': 'deu_Latn',
}

_model = None
_tokenizer = None

def load_model():
    global _model, _tokenizer
    
    if _model is not None:
        return _tokenizer, _model
    
    print(f"Loading model: {MODEL_NAME}")
    _tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    _model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    print("Model loaded")
    
    return _tokenizer, _model

def translate(text: str, source_lang: str, target_lang: str) -> dict:
    src_code = LANGUAGE_CODES.get(source_lang)
    tgt_code = LANGUAGE_CODES.get(target_lang)
    
    if not src_code or not tgt_code:
        return {
            'success': False,
            'translated': None,
            'error': f'지원하지 않는 언어: {source_lang} → {target_lang}'
        }
    
    try:
        tokenizer, model = load_model()
        tokenizer.src_lang = src_code
        
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        
        with torch.no_grad():
            try:
                forced_bos_token_id = tokenizer.get_lang_id(tgt_code)
            except AttributeError:
                try:
                    forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_code)
                except:
                    forced_bos_token_id = None
            
            if forced_bos_token_id is not None:
                translated_tokens = model.generate(
                    **inputs,
                    forced_bos_token_id=forced_bos_token_id,
                    max_length=512,
                    num_beams=5,
                    early_stopping=True,
                    no_repeat_ngram_size=3,
                )
            else:
                translated_tokens = model.generate(
                    **inputs,
                    max_length=512,
                    num_beams=5,
                    early_stopping=True,
                    no_repeat_ngram_size=3,
                )
        
        result = tokenizer.batch_decode(translated_tokens, skip_special_tokens=True)[0].strip()
        
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

def get_supported_languages() -> dict:
    return LANGUAGE_CODES.copy()
