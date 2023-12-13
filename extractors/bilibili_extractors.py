def bilibili_extractor_from_rank(data):
    # 定义一个字典来存储提取的数据
    extracted_data = {}

    # 安全地提取所需的字段
    extracted_data['title_value'] = data.get('title_detail',
                                             {}).get('value', 'No Title')
    extracted_data['summary_value'] = data.get('summary_detail',
                                               {}).get('value', 'No Summary')
    extracted_data['published_parsed'] = data.get('published_parsed',
                                                  'No Publish Date')
    extracted_data['link'] = data.get('link', 'No Link')
    extracted_data['author_name'] = data.get('author_detail',
                                             {}).get('name', 'No Author')

    return extracted_data
