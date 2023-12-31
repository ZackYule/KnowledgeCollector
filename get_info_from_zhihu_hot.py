import os
from utils.downloader import get_data_from_feed
from utils.extractors import html_to_text, rss_extractor, zhihu_answer_extractor
from utils.processor import add_date_to_folder
from utils.storage import generate_datetime_filepath, objects_to_csv, save_to_csv


def get_data_from_zhihu_hot():
    feed_url = 'http://localhost:1200/zhihu/hot'

    question_data = get_data_from_feed(feed_url=feed_url)
    question_data = [rss_extractor(v, html_to_text) for v in question_data]

    data = []
    for question_d in question_data:
        question_url = question_d.get('link', '')
        if question_url != '' and 'www.zhihu.com' in question_url:
            question_feed_url = question_url.replace(
                'https://www.zhihu.com', 'http://localhost:1200/zhihu')
            answer_data = get_data_from_feed(feed_url=question_feed_url)
            answer_data = [
                zhihu_answer_extractor(v, html_to_text) for v in answer_data
            ]
            for answer_d in answer_data:
                answer_d['question_title'] = question_d.get('title', '')
                answer_d['question_link'] = question_d.get('link', '')
                answer_d['question_summary'] = question_d.get('summary', '')
            data.extend(answer_data)

    return data


def main():
    file_path = generate_datetime_filepath('zhihu')

    data = get_data_from_zhihu_hot()
    objects_to_csv(data, file_path)


if __name__ == "__main__":
    main()
