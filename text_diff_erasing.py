
#잘 안됨

import os
from difflib import SequenceMatcher

def calculate_similarity(file1, file2):
    if not (os.path.exists(file1) and os.path.exists(file2)):
        return None
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2:
        text1 = f1.read()
        text2 = f2.read()
        similarity = SequenceMatcher(None, text1, text2).ratio()
        return similarity

def delete_similar_files(folder_path, threshold=0.9):
    files = os.listdir(folder_path)
    files_to_delete = []

    for i, file1 in enumerate(files[:-1]):
        for file2 in files[i+1:]:
            file1_path = os.path.join(folder_path, file1)
            file2_path = os.path.join(folder_path, file2)
            similarity = calculate_similarity(file1_path, file2_path)

            if similarity is not None and similarity >= threshold:
                files_to_delete.append(file2)

    for file_to_delete in files_to_delete:
        file_path_to_delete = os.path.join(folder_path, file_to_delete)
        print(f"Deleting {file_to_delete}")
        os.remove(file_path_to_delete)

if __name__ == "__main__":
    folder_path = "videos/example_Optimizer-Overview.mp4"  # 폴더 경로를 적절하게 수정해주세요.
    delete_similar_files(folder_path)
