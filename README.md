# What's Capturer

A capture tool used to capture pictures from web like Sina, LOFTER and huaban.

## Support Websites

- [Sina](https://weibo.com/)
- [Lofter](http://www.lofter.com/)
- [Toutiao](https://www.toutiao.com)
- [QQZone](https://qzone.qq.com/)
- [Huaban](https://huaban.com/)
- [Vmgirls](https://www.vmgirls.com/)

## How to use

- install `python3` and libs
- update your [Parameters](#parameters) of each kind of web
- run `./capturer` or run `main.py` or `***_spider.py` to capture images from 
  - `sina`
  - `lofter`
  - `toutiao`
  - `qqzone`
- run `huaban/run.py` to capture images from `huaban`
- run `vmgirls/run.py` to capture images from `vmgirls`

## Notices

Almost all of the file path based on `~/Pictures/python`, `~` means home dir.

## Parameters

### huaban

- `USERNAME`: username of huaban which you want to capture
- `ROOT_DIR`: directories where to store the images

### Sina

- `uid`: user-id(10 numbers) of sina weibo that you want to capture
- `cookies`: your cookies after login the sina weibo
- `path`: directory to save the pictures

### Lofter

- `username`: username of lofter that you want to capture
- `path`: directory to save the pictures, see the function `_get_path` in `lofter_spider.py`
- `query_number`: number of blogs in each query packet, default value is 40

