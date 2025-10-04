# -*- coding: utf-8 -*-
import time
from argparse import ArgumentParser
from typing import Tuple, List
from datetime import datetime, timedelta

import feedparser
import requests
from zai import ZhipuAiClient
import yaml


def load_config(yaml_path):
    """
    从 YAML 文件加载配置参数。
    @param yaml_path: YAML 文件路径
    @return: 配置字典
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def translate(papers: List[dict], config: dict) -> List[str]:
    client = ZhipuAiClient(api_key=config.get("ZHIPU_API_KEY"))  # 请填写您自己的 API Key

    chinese_summaries = []
    for paper in papers:
        text = paper.get("summary")
        response = client.chat.completions.create(
            model="glm-4.5",
            messages=[
                {"role": "user",
                 "content": f"你是一名精通英语的人工智能领域的专家，请你仔细思考，将下列英语文本翻译成中文：{text}。"
                            f"注意，你只需要翻译文本，不需要添加其他的任何信息"},
            ],
            thinking={
                "type": "disabled",  # 启用深度思考模式
            },
            temperature=0.6  # 控制输出的随机性
        )
        chinese_summaries.append(response.choices[0].message.content)
        time.sleep(5)

    return chinese_summaries


def get_arxiv_papers(category, start_date, end_date) -> Tuple[list, int]:
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

        return papers, papers.__len__()
    else:
        print(f"Error: {response.status_code}")
        return [], 0


if __name__ == "__main__":
    params = ArgumentParser(description='Get arxiv papers')
    params.add_argument('-c', type=str, nargs='+', default=["cs.CL", "cs.AI"], help='arxiv categories (支持多个)')
    params.add_argument('-s', type=str, help='start date (YYYYMMDD)')
    params.add_argument('-e', type=str, help='end date (YYYYMMDD)')

    args = params.parse_args()
    categories = args.c

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y%m%d")
    today = datetime.now().strftime("%Y%m%d")
    start_date = args.s if args.s else yesterday
    end_date = args.e if args.e else today

    config = load_config("./API_KEY.yaml")

    for category in categories:
        papers, count = get_arxiv_papers(category, start_date, end_date)
        with open(f'{category}_papers_{today}.txt', 'w', encoding='utf-8') as f:
            for idx, (paper, chinese_summary) in enumerate(zip(papers, translate(papers, config))):
                f.write(f"{idx + 1}: {paper['title']}\n")
                f.write(f"Authors: {paper['authors']}\n")
                f.write(f"Summary: {paper['summary']}\n")
                f.write(f"摘要: {chinese_summary}\n")
                f.write(f"Link: {paper['link']}\n")
                f.write(f"Updated: {paper['updated']}\n\n")

        print(f"Total {count} papers have been saved to {category}_papers_{today}")
