import asyncio
import os
from utils.extractors import rss_extractor
from utils.processor import generate_subtitles_from_folder, srt_to_string
from utils.storage import objects_to_csv, save_to_pickle
from utils.downloader import download_bilibili_videos, get_data_from_feed


def load_as_article_loader(data):
    result = []
    for v in data:
        content = {}
        content['metadata'] = {"source": v.get('link', 'No Link')}
        content['page_content'] = v.get('subtitle', 'No Subtitle')
        result.append(content)
    return result


def add_subtitles_to_data(folder_path, data):
    for v in data:
        for filename in os.listdir(folder_path):
            if filename.endswith('.srt') and v.get(
                    'title_value', 'None') + '.srt' == filename:
                v['subtitle'] = srt_to_string(
                    os.path.join(folder_path, filename))
    return data


async def get_data_from_bilibili_rank(topN: int = 1):
    feed_url = 'https://rsshub.app/bilibili/ranking/0/3/1'
    video_folder = 'data/bilibili_videos'
    subtitles_folder = 'data/bilibili_subtitles'

    data = get_data_from_feed(feed_url=feed_url)
    data = data[:topN]
    data = [rss_extractor(data=d) for d in data]

    urls = [video_info.get('link', 'No Link') for video_info in data]

    await download_bilibili_videos(urls=urls, path=video_folder)
    generate_subtitles_from_folder(video_folder, subtitles_folder)

    return add_subtitles_to_data(subtitles_folder, data)


async def main():
    data = await get_data_from_bilibili_rank()

    objects_to_csv(objects=data,
                   attributes=data[0].keys(),
                   filename='data/bilibili.csv')

    docs = load_as_article_loader(data=data)
    save_to_pickle(data=docs, filename='data/bilibili.pkl')


if __name__ == "__main__":
    asyncio.run(main())
