import pymupdf  # PyMuPDF
import easyocr
import pandas as pd

# 1. PDF의 해당 페이지를 고해상도 이미지로 변환
pdf_path = "data/과정기반 작물모형을 이용한 웹 기반 밀 재배관리 의사결정 지원시스템 설계 및 구축.pdf"
doc = pymupdf.open(pdf_path)

# 예시: 표가 있는 페이지 번호 지정 (0부터 시작하므로 3페이지면 2)
page_number = 5  
page = doc.load_page(page_number)

# 해상도를 높이기 위해 matrix 설정 (zoom=2는 2배 선명하게)
zoom = 2
mat = pymupdf.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)
image_path = "output/pdf_page_high_res.png"
pix.save(image_path)

print(f"[1] {page_number + 1}페이지를 이미지로 변환 완료: {image_path}")

# 2. EasyOCR 모델 로드 (한글과 영어 지정)
reader = easyocr.Reader(['ko', 'en'])
print("[2] OCR 모델 로드 완료. 텍스트 판독을 시작합니다...")
result = reader.readtext(image_path)

# 3. 추출된 데이터를 Y축(행) 기준으로 정렬 및 구조화
# EasyOCR 결과 구조: [([[x1,y1], [x2,y2], [x3,y3], [x4,y4]], "텍스트", 신뢰도)]
ocr_data = []
for bbox, text, prob in result:
    top_left_x = bbox[0][0]  # 텍스트 박스의 좌측 X축 좌표
    top_left_y = bbox[0][1]  # 텍스트 박스의 상단 Y축 좌표
    ocr_data.append({'x': top_left_x, 'y': top_left_y, 'text': text.strip()})

# Y축 좌표를 기준으로 정렬 (같은 행에 있는 글자들을 묶기 위함)
# Y축 좌표 차이가 15~20 픽셀 이하이면 같은 행(Row)으로 간주합니다.
ocr_df = pd.DataFrame(ocr_data)
ocr_df = ocr_df.sort_values(by=['y', 'x']).reset_index(drop=True)

print("\n--- [OCR 추출 결과] ---")
current_y = -999
row_text = []
threshold = 20  # 같은 행으로 판정할 Y축 오차 범위 (글자 크기에 따라 조절)

for index, row in ocr_df.iterrows():
    if current_y == -999:
        current_y = row['y']
        row_text.append(row['text'])
    elif abs(row['y'] - current_y) <= threshold:
        row_text.append(row['text'])
    else:
        # 새로운 행 시작 시 이전 행 출력
        print("\t".join(row_text))
        row_text = [row['text']]
        current_y = row['y']

# 마지막 행 출력
if row_text:
    print("\t".join(row_text))