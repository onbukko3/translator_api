import re
import requests
from bs4 import BeautifulSoup as bs

def getting_slicing_point(word, string):
    max_index = 0
    for char in string:
        cur_index = word.index(char)
        if cur_index > max_index:
            max_index = cur_index
    return int(max_index+1)

def sc_combining(word, slicing_point, sc):
    word = word[:slicing_point] + sc + word[slicing_point:]
    return word

def src_tgt_dict_list(outputs):
    pair_list = []
    src = ""
    tgt = ""
    pair = ()
    for output in outputs:
        lang = []
        for i, char in enumerate(output):
            lang.append(char)
            if char == "1":
                src = ''.join(lang[:-1])
                # print(src)
                lang = []
            if char == "2":
                tgt = ''.join(lang[:-1])
                lang = []
                if src and tgt:
                    pair = src, tgt
                    pair_list.append(pair)
            if i == len(output) - 1:
                tgt = ''.join(lang)
                lang = []
                if src and tgt:
                    pair = src, tgt
                    pair_list.append(pair)
    return pair_list

def getting_lang_list(url):
    respond = requests.get(url)
    html = respond.text
    soup = bs(html, 'html.parser')
    tables = soup.findAll('table')
    rows = tables[1].find_all('tr')

    output_list = []
    for row in rows:
        row = re.sub('[^a-zA-Z]','', row.text)
        if row:
            if row.find('zh') == 0:
                slicing_point = getting_slicing_point(row, 'zh')
                row = sc_combining(row, slicing_point, '-')
            output_list.append(row)
    return output_list

def gettting_lang_pair_dict(url):
    respond = requests.get(url)
    html = respond.text
    soup = bs(html, 'html.parser')
    tables = soup.findAll('table')
    rows = tables[2].find_all('tr')

    outputs = []
    for row in rows:
        row = re.sub(r'\n', '', row.text)
        row = re.sub(r'→', '1', row)
        row = re.sub(r'\|', '2', row)
        row = re.sub('[^a-zA-Z0-9]', '', row)
        if row:
            outputs.append(row)

        pair_list = src_tgt_dict_list(outputs)

    return pair_list




