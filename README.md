# Movie Box Office Revenue Analysis & Prediction

IT4142E Data Science Capstone, [Hanoi University of Science and Technology](https://hust.edu.vn/), 2021

## How to run

Note that in this project, the data crawler works independently. That means you have to run code manually. All the other
steps are visually demonstrated in our [demo](#demo-website). The `src` folder is for reference purpose only.

Therefore, this section title should be **How to run data crawler**.

```shell
cd src/crawler
scrapy crawl full2ImdbCrawler
```

Since the data crawler outputs two different files, we need to join them into a single final dataset:

```shell
cd ..
python join_data.py
```

## Project structure

```
├── dataset Dataset files in .csv
│   ├── extracted
│   ├── processed
│   └── **/*.csv
├── demo Demo website source
├── notebook Jupyter notebooks
├── src Data crawler and other source code only for reference purpose
├── README.md Project overview
```

## Dataset

After data collection: [data_joined.csv](./dataset/data_joined.csv)

After data cleaning: [cleaned_data.csv](./dataset/processed/cleaned_data.csv)

For Machine Learning: [feature_extracted.csv](./dataset/extracted/feature_extracted.csv)

## Demo website

Visit the project demo website at [theobmgit.github.io/it4142e-bor.github.io/](https://theobmgit.github.io/it4142e-bor.github.io/)
