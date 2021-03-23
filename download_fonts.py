from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse


def simple_get(url, resp_type):

    def is_good_response(resp, resp_type):
        content_type = resp.headers['Content-Type'].lower()
        return (resp.status_code == 200
                and content_type is not None
                and content_type.find(resp_type) > -1)

    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp, resp_type):
                return resp.content
            return None
    except RequestException as e:
        print('Error during get request to {0} : {1}'.format(url, str(e)))
        return None


def get_font_download_links(html_url):
    html = simple_get(html_url, 'html')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        anchors = soup.select("a[href*='/fonts/download']")
        anchors = [a for a in anchors if 'offsite' not in a.text]
    return anchors


def get_page_list(base_url, first_page_no, last_page_no):
    base_url_split = base_url.split('?')
    pieces = base_url_split[0].split('/')
    try:
        int(pieces[-1])
        pieces.pop(-1)
    except ValueError:
        pass
    pagelist = ['/'.join(['/'.join(pieces), str(no)]) for no in list(range((first_page_no - 1) * 50,
                                                                           50 * last_page_no, 50))]
    if len(base_url_split) == 2:
        pagelist = ['?'.join([link, base_url_split[1]]) for link in pagelist]
    return pagelist


def get_fonts(base_url, first_page_no, last_page_no):
    for page in get_page_list(base_url, first_page_no, last_page_no):
        print(f'Scanning page: {page}')
        links = get_font_download_links(page)
        for link in tqdm(links):
            font_name = link['href'].split('/')[-1]
            file_stream = simple_get('https://www.fontsquirrel.com'+link['href'], 'application')
            with open('fontfiles/' + font_name + '.zip', 'wb') as f:
                f.write(file_stream)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Downloads fonts into the fontfiles folder')
    parser.add_argument('--url', type=str,
                        help='url of the page with list of fonts', required=True)
    parser.add_argument('--start', type=int,
                        help='page no to start scraping', required=True)
    parser.add_argument('--end', type=int,
                        help='last page no to scrape', required=True)
    args = parser.parse_args()

    get_fonts(args.url, args.start, args.end)
