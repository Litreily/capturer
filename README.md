# What's Capturer

A capture tool used to capture pictures from web like Sina.

## How to use

- install `python` and libs
  - install `python3`
  - install `BeautifulSoup` - `bs4`
  - install `requests`
- update your [Parameters](#parameters) of each kind of web
- run `main.py` or `***_spider.py`

## Parameters

### Sina

- `uid`: user-id(10 numbers) of sina weibo that you want to capture
- `cookies`: your cookies after login the sina weibo
- `path`: directory to save the pictures

### Lofter

- `username`: username of lofter that you want to capture
- `path`: directory to save the pictures, see the function `_get_path` in `lofter_spider.py`
- `query_number`: number of blogs in each query packet, default value is 40
