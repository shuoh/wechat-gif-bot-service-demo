from gifbot.config.constants import GOOGLE_API_KEY, GOOGLE_CSE_CX
import requests


def google_image_search(query, max_num=10, image_size='medium'):
    """
    :param query: search query in string
    :param max_num: max number of search results [1,10]
    :param image_size: image size. small/medium/large
    :return: list of URLs
    """
    params = {
        'q': query,
        'num': max_num,
        'start': 1,
        'imgSize': image_size,
        'searchType': 'image',
        'key': GOOGLE_API_KEY,
        'cx': GOOGLE_CSE_CX
    }

    response = requests.get('https://www.googleapis.com/customsearch/v1', params)
    result_items = response.json().get('items')

    if result_items is None:
        return []
    else:
        return [item.get('link') for item in result_items]
