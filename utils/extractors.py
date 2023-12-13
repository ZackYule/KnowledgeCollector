import html
from bs4 import BeautifulSoup


def html_to_text(html_content):
    """
    将HTML内容转换为纯文本。

    :param html_content: 包含HTML的字符串。
    :return: 纯文本字符串。如果解析HTML时发生错误，返回None。
    """
    try:
        # 使用BeautifulSoup解析HTML，这里使用'lxml'作为解析器
        soup = BeautifulSoup(html_content, 'html.parser')

        # 获取纯文本
        text = soup.get_text(separator=' ', strip=True)

        # 解码HTML实体
        text = html.unescape(text)

        return text
    except Exception as e:
        print(f"解析HTML时发生错误: {e}")
        return None


def rss_extractor(rss_data, process_fn=lambda x: x):
    """
    从RSS数据中提取特定字段，并可选地通过处理函数进一步处理这些字段。

    :param rss_data: 包含RSS信息的字典。
    :param process_fn: 对提取的数据进行处理的函数（默认不进行任何处理）。
    :return: 提取并处理后的数据字典。
    """
    # 安全地提取所需的字段
    extracted = {
        'title': rss_data.get('title', ''),
        'title_detail': rss_data.get('title_detail', {}).get('value', ''),
        'summary': rss_data.get('summary_detail',
                                {}).get('value', 'No Summary'),
        'published': rss_data.get('published', ''),
        'id': rss_data.get('id', ''),
        'link': rss_data.get('link', ''),
        'author_name': rss_data.get('author_detail', {}).get('name', '')
    }

    # 应用处理函数
    if callable(process_fn):
        processed_data = {
            key: process_fn(value)
            for key, value in extracted.items()
        }
    else:
        processed_data = extracted

    return processed_data


def zhihu_answer_extractor(zhihu_answer_data, process_fn=lambda x: x):
    """
    从RSS数据中提取特定字段，并可选地通过处理函数进一步处理这些字段。

    :param zhihu_answer_data: 包含RSS信息的字典。
    :param process_fn: 对提取的数据进行处理的函数（默认不进行任何处理）。
    :return: 提取并处理后的数据字典。
    """
    # 安全地提取所需的字段
    extracted = {
        'answer_title':
        zhihu_answer_data.get('title', ''),
        'answer_title_detail':
        zhihu_answer_data.get('title_detail', {}).get('value', ''),
        'answer_summary':
        zhihu_answer_data.get('summary_detail', {}).get('value', 'No Summary'),
        'answer_published':
        zhihu_answer_data.get('published', ''),
        'answer_id':
        zhihu_answer_data.get('id', ''),
        'answer_link':
        zhihu_answer_data.get('link', ''),
        'answer_author_name':
        zhihu_answer_data.get('author_detail', {}).get('name', '')
    }

    # 应用处理函数
    if callable(process_fn):
        processed_data = {
            key: process_fn(value)
            for key, value in extracted.items()
        }
    else:
        processed_data = extracted

    return processed_data
