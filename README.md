# PaperPostman

## 1. Introduction

This is a small program used to obtain a collection of papers from arxiv in a specified category. It can be run through
the command line by specifying the category, start date, and end date to get a collection of papers within the specified
date range.

## 2. Usage

### 2.1 Dependencies

If pip is used for installation:

```shell
pip install feedparser requests pyyaml python-dotenv zai-sdk
```

If conda is used for installation:

```shell
conda install feedparser requests pyyaml python-dotenv zai-sdk
```

### 2.2 Run

```shell
python paperPostman.py [-c category] [-s start_date] [-e end_date]
```

If you want to use the default parameters, you will receive a collection of articles from the previous day on the two
categories of cs.CL and cs.AI

If you want to customize parameters, you can refer to the following instructions

+ `-c` is used to specify the category of the papers, such as: cs.CL, cs.AI, etc. The default is cs.CL. And the program
  supports collecting articles of multiple categories.
+ `-s` is used to specify the start date, the date format is "YYYYmmdd", the default is the previous day.
+ `-e` is used to specify the end date, the date format is "YYYYmmdd", the default is today.

### 2.3 Translation

The program supports automatic translation of the abstract of the papers. You need to get the API key from
the [ZhipuAI](https://bigmodel.cn/) website and save it in the `API_KEY.yaml` file in the root directory of the project.
The API key is saved in the `ZAI_API_KEY` variable.

### 2.4 Email
You can also use GitHub Action to automatically send the collection of papers to your email if you want.