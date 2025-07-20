# PaperPostman

## 1. 简介

这是一个用来从arxiv获取指定类别论文集合的小程序，可以通过命令行指定类别、开始日期和结束日期，获得指定日期范围内的论文集合

## 2. 使用方法

### 2.1 安装依赖

如果使用的是pip安装，则：

```shell
pip install feedparser
```

如果使用的是conda安装，则：

```shell
conda install feedparser
```

### 2.2 使用方法

```shell
python paperPostman.py [-c category] [-s start_date] [-e end_date]
```

其中：

+ -c表示类别，类别为arxiv官网提供的类别，例如：cs.CV、cs.CL等，默认为cs.CL
+ -s表示开始日期，日期格式均为"YYYYmmdd"，例如：20250717
+ -e表示结束日期，日期格式均为"YYYYmmdd"，默认为当天日期



