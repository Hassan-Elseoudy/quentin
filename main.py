import csv

import requests
from bs4 import BeautifulSoup

from QuentinExporter import QuentinExporter

headers = {
    'authority': 'proptechzone.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
    'cache-control': 'max-age=0',
    # Requests sorts cookies= alphabetically
    # 'cookie': '_gid=GA1.2.507602229.1673618965; _wpfuuid=e827016b-e80a-45a6-84c4-4d86715fd885; ln_or=eyIyNDUwMDE4IjoiZCJ9; _fbp=fb.1.1673618966429.62350412; _ga=GA1.2.1502793756.1673618965; _gat_gtag_UA_150924630_1=1; _ga_W5JG9JN9ET=GS1.1.1673623329.2.1.1673623613.0.0.0',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

cookies = {
    '_gid': 'GA1.2.507602229.1673618965',
    '_wpfuuid': 'e827016b-e80a-45a6-84c4-4d86715fd885',
    'ln_or': 'eyIyNDUwMDE4IjoiZCJ9',
    '_fbp': 'fb.1.1673618966429.62350412',
    '_ga': 'GA1.2.1502793756.1673618965',
    '_gat_gtag_UA_150924630_1': '1',
    '_ga_W5JG9JN9ET': 'GS1.1.1673623329.2.1.1673623613.0.0.0',
}


def get_text_from_file():
    file = open('text.txt', mode='r')
    all_of_it = file.read()
    file.close()
    return all_of_it


if __name__ == '__main__':

    soup = BeautifulSoup(get_text_from_file(), 'html.parser')
    li_tags = soup.find_all('li', class_='prop-arch-item')

    company_url: str = ''
    company_name: str = ''
    company_title: str = ''
    company_description: str = ''
    company_content: str = ''
    company_main_terms: str = ''
    company_detailed_terms: str = ''
    activity: str = ''
    company_linked_in: str = ''
    company_founding_year: str = ''
    company_employees: str = ''

    rows: [QuentinExporter] = []

    # Loop through the <li> tags
    for li in li_tags:
        article = li.find('article', class_='startups')
        if article:
            header = article.find('header', class_='home-arch-item-header')
            if header:
                if header.find('span', class_='home-arch-item-title'):
                    company_title = header.find('span', class_='home-arch-item-title').text

                terms_div = header.find('div', class_='startup-terms')
                if terms_div:
                    company_main_terms = ",".join(
                        [term.text for term in terms_div.find_all('span', class_='archive-item-term')
                         if term is not None])

            if article.find('div', class_='startup-excerpt'):
                company_description = article.find('div', class_='startup-excerpt').text

            link_btn = article.find('a', class_='home-arch-item-btn')
            if link_btn:
                link_href = link_btn['href']

                response = requests.get(link_href, headers=headers, cookies=cookies)
                link_soup = BeautifulSoup(response.content, 'html.parser')

                company_name = link_soup.find(class_='entry-title').text if link_soup.find(class_='entry-title') else ''
                company_url = link_soup.find(class_='startup-url').text if link_soup.find(class_='startup-url') else ''

                tew = link_soup.find(class_='top-excerpt-wrap')
                if tew:
                    if tew.find('p'):
                        activity = tew.find('p').text
                company_detailed_terms = ",".join(
                    [i.text for i in link_soup.find_all('li', class_='archived-sub-vertical-item')])

                stats = {}
                for stat in link_soup.find_all('div', class_='stat-cont'):
                    stat_title = stat.find('span', class_='startup-page-stat-title').text if stat.find('span',
                                                                                                       class_='startup-page-stat-title') else ''
                    stat_data = ",".join([s.text for s in stat.find_all('span', class_='startup-page-stat-data')])
                    stats[stat_title] = stat_data

                company_content = link_soup.find(class_='startup-content-inner').text if link_soup.find(
                    class_='startup-content-inner') else ''

                if link_soup.find(class_='sidebar-social-link'):
                    company_linked_in = link_soup.find('a', class_='sidebar-social-link').get('href', '')

                team = []
                team_member_divs = link_soup.find_all('div', class_='team-member-item')
                for team_member_div in team_member_divs:
                    person = {}

                    img_wrap_div = team_member_div.find('div', class_='team-member-img-wrap')
                    if img_wrap_div:
                        # Find the <img> tag and extract the src
                        img_tag = img_wrap_div.find('img')
                        if img_tag:
                            person['img'] = img_tag['src']

                    info_wrap_div = team_member_div.find('div', class_='team-member-info-wrap')
                    if info_wrap_div and len(info_wrap_div.find_all('span', class_='title-14')):
                        if info_wrap_div.find_all('span', class_='title-14')[0]:
                            person['name'] = info_wrap_div.find_all('span', class_='title-14')[0].text
                        if len(info_wrap_div.find_all('span', class_='title-14')) == 2 and \
                                info_wrap_div.find_all('span', class_='title-14')[1]:
                            person['title'] = info_wrap_div.find_all('span', class_='title-14')[1].text
                        a_tag = info_wrap_div.find('a')
                        if a_tag:
                            person['url'] = a_tag['href']
                    team.append(person)

                company_founding_year = stats.get('Year Founded', '')
                company_employees = stats.get('Employees', '')

                if not team:
                    rows.append(QuentinExporter(
                        company_url,
                        company_name,
                        activity,
                        company_linked_in,
                        company_founding_year,
                        company_employees,
                        '',
                        '',
                        '',
                        company_title,
                        company_description,
                        company_content,
                        company_main_terms,
                        company_detailed_terms,
                        stats
                    ))

                else:
                    for member in team[:min(len(team), 3)]:
                        rows.append(QuentinExporter(
                            company_url,
                            company_name,
                            activity,
                            company_linked_in,
                            company_founding_year,
                            company_employees,
                            member.get('name', ''),
                            member.get('title', ''),
                            member.get('url', ''),
                            company_title,
                            company_description,
                            company_content,
                            company_main_terms,
                            company_detailed_terms,
                            stats
                        ))

    with open('data.csv', 'w', ) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['company_url', 'company_name', 'activity', 'company_linked_in', 'company_founding_year',
                         'company_employees', 'person_full_name', 'person_job_title', 'person_url', 'company_title',
                         'company_description', 'company_content', 'company_main_terms', 'company_detailed_terms',
                         'stats'])
        for row in rows:
            writer.writerow(
                [row.company_url, row.company_name, row.activity, row.company_linked_in, row.company_founding_year,
                 row.company_employees, row.person_full_name, row.person_job_title, row.person_url, row.company_title,
                 row.company_description, row.company_content, row.company_main_terms, row.company_detailed_terms,
                 str(row.stats)])
