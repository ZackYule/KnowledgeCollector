import csv
import os
import pickle
from typing import List
import logging
from logger_config import setup_logging
from utils.processor import add_date_to_folder

logger = logging.getLogger(__name__)


def save_to_pickle(data, filename):
    """
    将数据保存为 pickle 文件。

    参数:
    data -- 要保存的数据
    filename -- 保存文件的名称（包括路径，如果需要）
    """
    try:
        # 提取目录路径并检查是否存在，如果不存在则创建
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(filename, 'wb') as file:
            pickle.dump(data, file)

        logger.info(f"数据已成功保存到文件 {filename}")
    except Exception as e:
        logger.warn(f"保存数据时出错: {e}")


def read_from_pickle(filename):
    """
    从 pickle 文件中加载数据。

    参数:
    filename -- 包含数据的 pickle 文件的名称（包括路径，如果需要）
    """
    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        logger.warn(f"文件未找到: {filename}")
    except Exception as e:
        logger.warn(f"读取数据时出错: {e}")


def save_to_csv(data, filename, attributes: List[str] = []):
    """
    将数据保存到CSV文件中。

    :param data: 要保存的数据，格式为列表的列表（每个子列表代表一行）。
    :param filename: CSV文件的名称。
    """
    try:
        # 提取目录路径并检查是否存在，如果不存在则创建
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        # 使用'with'语句打开文件，确保用完后自动关闭
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 首先写入表头
            if len(attributes) > 0:
                writer.writerow(attributes)
            # 写入数据
            for row in data:
                writer.writerow(row)
    except Exception as e:
        logger.warn(f"保存数据时出错: {e}")


def read_from_csv(filename):
    """
    从CSV文件中读取数据。

    :param filename: CSV文件的名称。
    :return: 一个列表，包含CSV文件中的所有行，每行是一个列表。
    """
    try:
        data = []
        # 使用'with'语句打开文件，确保用完后自动关闭
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)

            # 读取数据
            for row in reader:
                data.append(row)

        return data
    except FileNotFoundError:
        logger.warn(f"文件未找到: {filename}")
    except Exception as e:
        logger.warn(f"读取数据时出错: {e}")


def objects_to_csv(objects, filename, attributes: List[str] = []):
    """
    将具有不同属性的对象列表保存到CSV文件中。

    :param objects: 对象的列表。
    :param attributes: 要从对象中提取的属性名列表。
    :param filename: CSV文件的名称。
    """
    # 转换对象列表为列表的列表
    assert len(objects) > 0
    if len(attributes) == 0:
        attributes = objects[0].keys()
    data = []
    for obj in objects:
        row = [obj.get(attr, '') for attr in attributes]
        data.append(row)
    save_to_csv(data=data, filename=filename, attributes=attributes)


def generate_datetime_filepath(website: str, date_format='%Y-%m-%d'):
    folder_path = '/Users/zack/Knowledge/' + website
    file_name = 'answers.csv'
    folder_path = add_date_to_folder(folder_path, date_format='%Y-%m-%d')
    file_path = os.path.join(folder_path, file_name)

    return file_path
