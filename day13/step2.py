# PDF 파일에서 헤더와 푸터를 제외한 텍스트 추출하기
import pymupdf  # PyMuPDF
import os

pdf_file_path = "data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"  # PDF 파일 경로
doc = pymupdf.open(pdf_file_path) # PDF 문서 열기

# 헤더와 푸터의 높이 설정 (예시로 80 픽셀로 설정)
header_height = 80
footer_height = 80

full_text = ""

for page in doc: # 페이지 단위로 반복
    rect = page.rect  # 페이지의 전체 영역
    # 헤더와 푸터를 제외한 영역 계산
    header = page.get_text(clip=(0,0,rect.width, header_height))  # 헤더 영역
    footer = page.get_text(clip=(0, rect.height - footer_height, rect.width, rect.height))  # 푸터 영역
    content = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))  # 콘텐츠 영역

    # 'text' 외에 'blocks'나 'words' 구조로 추출도 가능
    full_text += content + "\n--------------------------------\n"  # 콘텐츠 영역의 텍스트만 추가

# 추출된 텍스트를 txt 파일로 저장
pdf_file_name = os.path.basename(pdf_file_path)  # PDF 파일 이름 추출
pdf_file_name = os.path.splitext(pdf_file_name)[0]  # 확장자 제거

# 헤더와 푸터를 제외한 텍스트를 저장
with open(f"output/{pdf_file_name}_with_preprocessing.txt", "w", encoding="utf-8") as f:
    f.write(full_text)

doc.close()  # 문서 닫기

print(f"PDF 파일에서 텍스트를 추출하여 output/{pdf_file_name}_with_preprocessing.txt 파일로 저장했습니다.")