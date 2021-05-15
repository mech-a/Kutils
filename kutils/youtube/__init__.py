delete_keywords = ['&feature', '&list', '&index', '&lc', '&ab_channel', '&t']


# TODO redo youtube ID extraction with urlparse

def extract_youtube_ids_from_urls(urls):
    ids = []
    count_non_yt_vid = 0
    for url in urls:
        if not is_youtube_video_url(url):
            count_non_yt_vid += 1
            continue

        for kw in delete_keywords:
            if kw in url:
                url = url[:url.find(kw)]

        if is_link_shortened(url) and url.rfind('?') > 0:
            id = url[url.rfind('/') + 1:url.rfind('?')]
        elif is_link_shortened(url):
            id = url[url.rfind('/') + 1:]
        # TODO special chars not in id list
        elif '&' in url:
            id = url[url.rfind('=') + 1:url.find('&')]
        elif ']' in url:
            id = url[url.rfind('=') + 1:url.find(']')]
        else:
            id = url[url.rfind('=') + 1:]

        ids.append(id)
    return ids, count_non_yt_vid


def is_youtube_video_url(url: str) -> bool:
    # TODO better cleanurl
    return ('playlist' not in url) and ('youtube.com' in url or 'youtu.be' in url) and ('results' not in url)


def is_link_shortened(yt_url: str) -> bool:
    # not necessarily the best b/c of double youtube phenomenon (youtube.com...&feature=youtu.be)
    return 'youtu.be' in yt_url



# def find_url_idx_by_str(str):
#     # testing function for finding errors
#     for i in range(len(urls)):
#         if str in urls[i]:
#             return i
