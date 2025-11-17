# 한국어 지원 번역기 Version 0.1-KR
# M2M100 모델 사용 (100개 언어 지원!)

from flask import Flask, render_template, request, jsonify
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

app = Flask(__name__)

# 전역 변수로 모델 저장
model = None
tokenizer = None

def load_model():
    """M2M100 번역 모델 로드 (서버 시작 시 1번만 실행)"""
    global model, tokenizer
    print("📥 다국어 번역 모델을 로딩 중입니다...")
    print("⚠️  처음 실행 시 약 2GB 모델을 다운로드합니다 (10-20분 소요)")
    
    # M2M100 모델 - 100개 언어 지원 (한국어 포함!)
    model_name = "facebook/m2m100_418M"
    tokenizer = M2M100Tokenizer.from_pretrained(model_name)
    model = M2M100ForConditionalGeneration.from_pretrained(model_name)
    
    print("✅ 모델 로딩 완료!")
    print("✅ 지원 언어: 한국어, 영어, 일본어, 중국어, 독일어, 프랑스어 등 100개 언어")

@app.route('/')
def home():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    """번역 API"""
    # 1. 사용자가 보낸 데이터 받기
    data = request.json
    text = data.get('text', '')
    source_lang = data.get('source_lang', 'en')  # 기본값: 영어
    target_lang = data.get('target_lang', 'ko')  # 기본값: 한국어
    
    # 2. 빈 텍스트 체크
    if not text:
        return jsonify({'error': '텍스트를 입력해주세요!'}), 400
    
    # 3. 번역 실행
    try:
        # 소스 언어 설정
        tokenizer.src_lang = source_lang
        
        # 텍스트 인코딩
        encoded = tokenizer(text, return_tensors="pt")
        
        # 타겟 언어로 번역
        forced_bos_token_id = tokenizer.get_lang_id(target_lang)
        generated_tokens = model.generate(
            **encoded,
            forced_bos_token_id=forced_bos_token_id
        )
        
        # 결과 디코딩
        result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        
        # 4. 결과 반환
        return jsonify({
            'original': text,
            'translated': result,
            'source_lang': source_lang,
            'target_lang': target_lang
        })
    
    except Exception as e:
        # 에러 발생 시
        print(f"번역 오류: {e}")
        return jsonify({'error': f'번역 중 오류가 발생했습니다: {str(e)}'}), 500

@app.route('/languages')
def get_languages():
    """지원하는 언어 목록 (주요 언어만)"""
    languages = {
        'en': 'English (영어)',
        'ko': '한국어 (Korean)',
        'ja': '日本語 (일본어)',
        'zh': '中文 (중국어)',
        'de': 'Deutsch (독일어)',
        'fr': 'Français (프랑스어)',
        'es': 'Español (스페인어)',
        'ru': 'Русский (러시아어)',
        'ar': 'العربية (아랍어)',
        'hi': 'हिन्दी (힌디어)'
    }
    return jsonify(languages)

if __name__ == '__main__':
    # 서버 시작 전에 모델 로드
    load_model()
    
    # 서버 실행
    print("\n🚀 한국어 지원 번역기가 시작됩니다!")
    print("👉 브라우저에서 http://localhost:5000 으로 접속하세요")
    print("🌍 지원 언어: 한국어, 영어, 일본어, 중국어 등 100개 언어\n")
    app.run(debug=True, port=5000)
