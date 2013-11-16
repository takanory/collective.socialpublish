
def fb_page_info_list_to_str(li):
    items = []
    for item in li:
        page_id = item['id']
        page_title = item['name']
        token = item['access_token']
        items.append('|'.join([page_id, page_title, token]))
    return u'\n'.join(items)

def fb_page_info_str_to_dict(s):
    dic = {}
    for li in s.split('\n'):
        try:
            page_id, page_title, token = li.strip().split('|')
        except ValueError:
            continue
        dic[page_id.strip()] = {'title' : page_title.strip(),
                                'token' : token.strip()}
    return dic

def get_fb_page_token(settings, page_id):
    fb_page_info = settings.fb_page_info
    fb_page_info_dict = fb_page_info_str_to_dict(fb_page_info)
    page_title_token = fb_page_info_dict.get(page_id)
    if page_title_token is not None:
        return page_title_token['token']
    return ""
