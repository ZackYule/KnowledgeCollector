from datetime import datetime
import os
import subprocess
import sys


def srt_to_string(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text = ""
    for line in lines:
        if not line.startswith(
            ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\n')):
            text += line.strip() + " "

    return text


def generate_subtitles_from_video(video_path,
                                  output_folder,
                                  model='small',
                                  srt_only='true',
                                  language='zh'):
    """
    Generates subtitles for a video using auto-subtitle.

    Parameters:
    video_path (str): Path to the video file.
    output_folder (str): Directory where the output should be saved.
    model (str): Model size for transcription ('tiny', 'base', 'small', 'medium', 'large').
    """

    try:
        # Constructing the command
        command = [
            'auto_subtitle', video_path, '-o', output_folder, '--model', model,
            '--srt_only', srt_only, '--language', language
        ]

        # Executing the command
        subprocess.run(command, check=True)
        print(f"Subtitles generated successfully for {video_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating subtitles: {e}",
              file=sys.stderr)


def generate_subtitles_from_folder(folder_path, output_folder):
    # 获取文件夹中所有文件
    files = os.listdir(folder_path)

    # 循环遍历所有文件
    for file in files:
        # 构建完整的文件路径
        file_path = os.path.join(folder_path, file)

        # 检查是否为视频文件（例如，通过扩展名）
        if file_path.endswith('.mp4'):
            generate_subtitles_from_video(file_path, output_folder)


def add_date_to_folder(folder_path, date_format='%Y-%m-%d'):
    """
    将当前日期添加到文件夹路径。

    :param folder_path: 原始文件夹路径。
    :param date_format: 日期的格式字符串，默认为 '%Y-%m-%d'。
    :return: 修改后的文件夹路径。
    """
    # 获取当前日期
    today = datetime.now().strftime(date_format)

    # 创建新的文件夹路径
    new_folder_path = f"{folder_path}_{today}"

    return new_folder_path
