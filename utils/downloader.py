import os
import feedparser
from bilix.sites.bilibili import DownloaderBilibili
import asyncio


def get_data_from_feed(feed_url, data_extractor=lambda x: x):

    # Parse the feed with feedparser
    feed = feedparser.parse(feed_url)

    if not callable(data_extractor):
        raise ValueError("data_extractor 必须是一个可调用的函数")

    result = []
    for entry in feed.entries:
        try:
            extracted_data = data_extractor(entry)
            if extracted_data is not None:
                result.append(extracted_data)
        except Exception as e:
            print(f"处理条目时出错: {e}")
    return result


async def download_video_from_url(url, path):
    if not os.path.exists(path):
        os.makedirs(path)
    async with DownloaderBilibili() as d:
        await d.get_video(url=url, path=path)


async def download_bilibili_videos(urls, path):
    # 创建一个异步任务列表
    tasks = [download_video_from_url(url=url, path=path) for url in urls]

    # 并行运行所有下载任务
    await asyncio.gather(*tasks)
