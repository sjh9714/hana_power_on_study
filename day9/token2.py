# Hugging Face Transformers 라이브러리에서 AutoTokenizer 클래스를 가져온다.
#
# AutoTokenizer: 모델에 맞는 Tokenizer를 자동으로 선택하여 로드해준다.
#
# 예:
# bert-base-uncased -> BertTokenizer
# roberta-base      -> RobertaTokenizer
# gpt2              -> GPT2Tokenizer
from transformers import AutoTokenizer

# ============================================================
# 사전 학습된(pretrained) BERT 토크나이저 다운로드 및 로드
# ============================================================
#
# "bert-base-uncased"
#
# bert      : BERT 모델
# base      : 12개의 Transformer Layer 사용
# uncased   : 대소문자를 구분하지 않음
#
# 최초 실행 시:
#
# 1. Hugging Face Hub 접속
# 2. config.json 다운로드
# 3. tokenizer_config.json 다운로드
# 4. vocab.txt 다운로드
# 5. tokenizer.json 다운로드
#
# 다운로드된 파일은
#
# C:\Users\<사용자>\.cache\huggingface\hub
#
# 에 저장된다.
#
# 두 번째 실행부터는 캐시된 파일을 사용하므로
# 다운로드 과정 없이 빠르게 실행된다.
#
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")


# ============================================================
# 문자열을 토큰(Token)으로 분리
# ============================================================
#
# Tokenizer는 문장을 작은 단위(Token)로 나눈다.
#
# 예)
#
# "I love AI"
#
# ->
#
# ['i', 'love', 'ai']
#
#
# BERT는 WordPiece 알고리즘을 사용한다.
#
# 사전에 존재하는 단어는 그대로 사용하고
# 사전에 없는 단어는 여러 조각으로 분리한다.
#
# 예)
#
# "playing"
#
# ->
#
# ['play', '##ing']
#
#
# ## 의미
#
# "앞 토큰 뒤에 붙는 부분"
#
# play + ing
#
# ->
#
# playing
##BERT 사전에 unbelievable 이 존재함 
tokens = tokenizer.tokenize("unbelievable")

# ============================================================
# 토큰 출력
# ============================================================
#
# 결과:
#
# ['unbelievable']
#
# 이유:
#
# BERT Vocabulary(사전)에
# "unbelievable" 단어가 존재하기 때문
#
print(tokens)


#BERT 사전에 unbelievably 이 존재 하지 않음
tokens = tokenizer.tokenize("unbelievably")

print(tokens)
# 출력 결과 : ['un', '##bel', '##ie', '##va', '##bly']