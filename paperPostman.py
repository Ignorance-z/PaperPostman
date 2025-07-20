# -*- coding: utf-8 -*-
import time
from argparse import ArgumentParser

import feedparser
import requests



def get_arxiv_papers(category, start_date, end_date):
    base_url = "http://export.arxiv.org/api/query?"

    query = f"cat:{category}+AND+submittedDate:[{start_date}+TO+{end_date}]"

    response = requests.get(
        base_url + f'search_query={query}&max_results=1000&sortBy=submittedDate&sortOrder=ascending')

    if response.status_code == 200:
        # 解析Atom feed
        feed = feedparser.parse(response.content)

        papers = []
        for entry in feed.entries:
            paper = {
                'title': ''.join(entry.title.split('\n')),
                'authors': [author.name for author in entry.authors],
                'published': entry.published,
                'updated': entry.updated,
                'summary': ''.join(entry.summary.split('\n')),
                'link': entry.links[0].href
            }
            papers.append(paper)

        return papers
    else:
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    params = ArgumentParser(description='Get arxiv papers')
    params.add_argument('-c', type=str, default="cs.CL", help='arxiv category')
    params.add_argument('-s', type=str, default="20250717", help='start date')
    params.add_argument('-e', type=str, default="20250720", help='end date')

    args = params.parse_args()
    category = args.c
    start_date = args.s
    end_date = args.e

    papers = get_arxiv_papers(category, start_date, end_date)
    t = time.strftime("%Y%m%d", time.localtime())

    with open(f'{category}_papers_{t}.txt', 'w', encoding='utf-8') as f:
        for idx, paper in enumerate(papers):
            f.write(f"{idx + 1}: {paper['title']}\n")
            f.write(f"Authors: {paper['authors']}\n")
            f.write(f"Summary: {paper['summary']}\n")
            f.write(f"Link: {paper['link']}\n\n")
