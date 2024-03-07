import os
from utils.processor import srt_to_string


def convert_srt_folder_to_txt(source_folder, target_folder, separator=" "):
    # 确保目标文件夹存在
    os.makedirs(target_folder, exist_ok=True)

    # 遍历源文件夹中的所有文件
    for file_name in os.listdir(source_folder):
        if file_name.endswith('.srt'):
            source_file_path = os.path.join(source_folder, file_name)

            # 使用 srt_to_string 函数处理 .srt 文件
            text = srt_to_string(source_file_path, separator)

            # 修改文件扩展名，并生成目标文件路径
            new_file_name = file_name.replace('.srt', '.txt')
            target_file_path = os.path.join(target_folder, new_file_name)

            # 将处理后的文本保存到新的 .txt 文件
            with open(target_file_path, 'w', encoding='utf-8') as new_file:
                new_file.write(text)

            print(
                f'File {new_file_name} has been successfully created in {target_folder}.'
            )


if __name__ == "__main__":
    # 定义源文件夹和目标文件夹的路径
    source_folder_path = 'data/bilibili_subtitles'
    target_folder_path = 'data/txt_files'

    # 调用函数进行转换
    convert_srt_folder_to_txt(source_folder_path, target_folder_path, '\n')
