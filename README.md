# What's Capturer

A capture tool used to capture pictures from web like Sina, it's powered by python3.

## How to use

- install `python` and libs
  - install `python3`
  - install `BeautifulSoup` - `bs4`
  - install `requests`
- update your [Parameters](#parameters) of each kind of web
- run `main.py`

## Parameters

### Sina

- `uid`: user-id(10 numbers) of sina weibo that you want to capture
- `cookies`: your cookies after login the sina weibo
- `path`: directory to save the pictures

### Lofter

- `username`: username of lofter that you want to capture
- `path`: directory to save the pictures, see the function `getRootPath` in `getImgFromLofter.py`
- `queryNumber`: number of blogs in each query packet, default value is 40