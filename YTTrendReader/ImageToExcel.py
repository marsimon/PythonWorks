from openpyxl import Workbook
from openpyxl.drawing.image import Image as ExcelImage


# 엑셀 파일 생성
wb = Workbook()
ws = wb.active

# 이미지 불러오기
image_path = "뱁새.png"  # 저장할 이미지 경로
img = ExcelImage(image_path)

# 이미지 크기 조정 (선택사항)
img.width, img.height = (80, 45)  # 원하는 크기로 조정

# 이미지 엑셀에 추가
ws.add_image(img, 'A1')  # 'A1' 셀 위치에 이미지 추가

# 엑셀 파일 저장
excel_file_path = "output_with_image.xlsx"
wb.save(excel_file_path)

print(f"이미지가 {excel_file_path}에 저장되었습니다.")
