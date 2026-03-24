import os
import shutil
from pathlib import Path

# 다운로드 폴더 경로
downloads_folder = r"C:\Users\student\Downloads"

# 파일 분류 규칙 정의
file_categories = {
    r"\images": [".jpg", ".jpeg"],
    r"\data": [".csv", ".xlsx"],
    r"\docs": [".txt", ".doc", ".pdf"],
    r"\archive": [".zip"]
}

def create_folders(base_path, categories):
    """분류 폴더가 없으면 생성"""
    for folder in categories.keys():
        folder_path = base_path + folder
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"폴더 생성: {folder_path}")
        else:
            print(f"폴더 이미 존재: {folder_path}")

def move_files(source_path, categories):
    """파일을 분류된 폴더로 이동"""
    if not os.path.exists(source_path):
        print(f"오류: {source_path} 경로가 존재하지 않습니다.")
        return
    
    # 다운로드 폴더의 모든 파일 순회
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)
        
        # 파일만 처리 (폴더 제외)
        if not os.path.isfile(file_path):
            continue
        
        # 파일 확장자 가져오기 (소문자로 변환)
        file_ext = os.path.splitext(filename)[1].lower()
        
        # 분류에 해당하는 폴더 찾기
        moved = False
        for folder, extensions in categories.items():
            if file_ext in extensions:
                destination_folder = source_path + folder
                destination_path = os.path.join(destination_folder, filename)
                
                # 같은 이름의 파일이 이미 존재하면 건너뛰기
                if os.path.exists(destination_path):
                    print(f"이미 존재함 (스킵): {filename}")
                else:
                    try:
                        shutil.move(file_path, destination_path)
                        print(f"이동됨: {filename} → {folder}")
                        moved = True
                    except Exception as e:
                        print(f"오류 발생 ({filename}): {e}")
                
                break
        
        if not moved and file_ext:
            print(f"분류 안 됨: {filename}")

def main():
    """메인 함수"""
    print("=" * 50)
    print("파일 자동 분류 시작")
    print("=" * 50)
    
    # 1단계: 필요한 폴더 생성
    print("\n[1단계] 분류 폴더 생성")
    create_folders(downloads_folder, file_categories)
    
    # 2단계: 파일 이동
    print("\n[2단계] 파일 분류 및 이동")
    move_files(downloads_folder, file_categories)
    
    print("\n" + "=" * 50)
    print("파일 분류 완료!")
    print("=" * 50)

if __name__ == "__main__":
    main()
