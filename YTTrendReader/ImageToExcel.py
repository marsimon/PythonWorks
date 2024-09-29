from googletrans import Translator
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re

# nltk의 stopwords 다운로드
nltk.download('stopwords')

# 번역기 객체 생성
translator = Translator()


# 각국 문장 예시 (사용자 문장을 여기에 넣어주세요)
sentences_by_country = {
    "Vietnam": ["pencukuran bulu kiwi terlalu berlebihan! Tidak ada kulit, Bukan masalah!"],
    "Japan": ["Your Japanese sentences here..."],
    # 나머지 국가도 마찬가지로 추가
}

# 번역 및 키워드 추출 함수
def translate_and_extract_keywords(sentences, language_code):
    translated_sentences = []
    
    # 각 문장을 한국어로 번역
    for sentence in sentences:
        print(sentence)
        detected = translator.detect(sentence)
        print(detected)
        translated = translator.translate(sentence, dest='ko').text
        translated_sentences.append(translated)
    
    # 모든 번역된 문장을 하나로 합치기
    all_text = ' '.join(translated_sentences)
    
    # 불용어 제거 및 텍스트 전처리
    stop_words = set(stopwords.words('korean'))
    words = re.findall(r'\b\w+\b', all_text)
    words = [word for word in words if word not in stop_words]
    
    # 빈도 계산
    word_freq = Counter(words)
    
    return word_freq.most_common(10)  # 상위 10개의 키워드를 추출

# 각 국가별로 번역하고 키워드 추출하기
keywords_by_country = {}
for country, sentences in sentences_by_country.items():
    if country == "Vietnam":
        language_code = 'vi'
    elif country == "Japan":
        language_code = 'ja'
    # 다른 국가도 마찬가지로 처리
    # ...
    
    keywords_by_country[country] = translate_and_extract_keywords(sentences, language_code)

# 결과 출력
for country, keywords in keywords_by_country.items():
    print(f"Country: {country}")
    print(f"Top Keywords: {keywords}")
    print("\n")
