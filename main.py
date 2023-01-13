import requests
from bs4 import BeautifulSoup

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

# Open a file: file
file = open('text.txt', mode='r')

# read all lines at once
all_of_it = file.read()

# close the file
file.close()


# Parse the HTML content
soup = BeautifulSoup(all_of_it, 'html.parser')

# Find all <li> tags with class "prop-arch-item"
li_tags = soup.find_all('li', class_='prop-arch-item')

# Loop through the <li> tags
for li in li_tags:
    # Find the <article> tag with class "startups"
    article = li.find('article', class_='startups')
    if article:
        # Find the <a> tag and extract the href
        a_tag = article.find('a')
        if a_tag:
            href = a_tag['href']
            print(href)

        # Find the <header> tag with class "home-arch-item-header"
        header = article.find('header', class_='home-arch-item-header')
        if header:
            # Find the <span> tag with class "home-arch-item-title" and extract its text
            title = header.find('span', class_='home-arch-item-title').text

            # Find the <div> tag with class "startup-terms"
            terms_div = header.find('div', class_='startup-terms')
            if terms_div:
                # Find all <span> tags with class "archive-item-term" and extract their text
                terms = [term.text for term in terms_div.find_all('span', class_='archive-item-term')]

        # Find the <div> tag with class "startup-excerpt" and extract its text
        excerpt = article.find('div', class_='startup-excerpt').text

        # Find the <a> tag with class "home-arch-item-btn" and extract its href
        link_btn = article.find('a', class_='home-arch-item-btn')
        if link_btn:
            link_href = link_btn['href']
            # Make a request to the link and extract the information

            response = requests.get(link_href, headers=headers, cookies=cookies)
            link_soup = BeautifulSoup(response.content, 'html.parser')

            # Extract the text from elements with class name "entry-title", "startup-url", "top-excerpt-wrap", "startup-top-info-stats-cont", "startup-side-info-icons-mobile", "startup-content-inner" and "startup-team-wrapper"
            entry_title = link_soup.find(class_='entry-title').text
            startup_url = link_soup.find(class_='startup-url').text
            top_excerpt_wrap = link_soup.find(class_='top-excerpt-wrap').text
            topics = ",".join([i.text for i in link_soup.find_all('li', class_='archived-sub-vertical-item')])


            stats = {}
            for stat in link_soup.find_all('div', class_='stat-cont'):
                stat_title = stat.find('span', class_='startup-page-stat-title').text
                stat_data = ",".join([s.text for s in stat.find_all('span', class_='startup-page-stat-data')])
                stats[stat_title] = stat_data

            startup_content_inner = link_soup.find(class_='startup-content-inner').text
            sidebar_social_link = link_soup.find(class_='sidebar-social-link').text

            team = []
            team_member_divs = link_soup.find_all('div', class_='team-member-item')
            for team_member_div in team_member_divs:
                person = {}
                # Find the <div> tag with class "team-member-img-wrap"
                img_wrap_div = team_member_div.find('div', class_='team-member-img-wrap')
                if img_wrap_div:
                    # Find the <img> tag and extract the src
                    img_tag = img_wrap_div.find('img')
                    if img_tag:
                        person['img'] = img_tag['src']
                # Find the <div> tag with class "team-member-info-wrap"
                info_wrap_div = team_member_div.find('div', class_='team-member-info-wrap')
                if info_wrap_div:
                    # Find the <span> tags and extract their text
                    person['name'] = info_wrap_div.find('span', class_='team-member-name').text
                    person['title'] = info_wrap_div.find('span', class_='team-member-title').text
                    # Find the <a> tag and extract the href
                    a_tag = info_wrap_div.find('a')
                    if a_tag:
                        person['url'] = a_tag['href']
                team.append(person)