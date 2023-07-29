#일단 잘 됨

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_cosine_similarity(file1, file2):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform([file1, file2])
    return cosine_similarity(tfidf_matrix)[0][1]

def main(input_folder):
    file_paths = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith('.txt')]
    grouped_folders = []

    for file_path in file_paths:
        current_group = None
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        for group in grouped_folders:
            representative_file = group[0]
            similarity = get_cosine_similarity(content, read_text_file(representative_file))
            similarity_percentage = similarity * 100

            if similarity_percentage >= 50:
                current_group = group
                break

        if current_group is None:
            grouped_folders.append([file_path])
        else:
            current_group.append(file_path)

    # Create directories and move files
    for idx, group in enumerate(grouped_folders):
        folder_name = f"group_{idx + 1}"
        os.makedirs(folder_name, exist_ok=True)
        for file_path in group:
            file_name = os.path.basename(file_path)
            new_file_path = os.path.join(folder_name, file_name)
            os.rename(file_path, new_file_path)

        if len(group) > 1:
            print(f"Similarity within Group {idx + 1}: {similarity_percentage:.2f}%")

if __name__ == "__main__":
    input_folder = "text - 복사본 (2)"  # Replace with the actual folder path.
    main(input_folder)
