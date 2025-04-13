import scrapy
from bs4 import BeautifulSoup
import os
import pandas as pd
from tqdm import tqdm
from collections import defaultdict

class StackSpider(scrapy.Spider):
    name = 'stack'
    allowed_domains = ['stackoverflow.com']

    # Year : Page number mapping (starting point for last 3 months)
    years_index = {
        2024: 1429,
        2023: 11020,
        2022: 26952,
        2021: 53814,
        2020: 84599,
        2019: 121799,
        2018: 156985,
        2017: 194607,
        2016: 236787,
        2015: 280657,
        2014: 324286,
        2013: 366692,
    }

    existing_ids = set()
    max_pages = 2000  # upper cap per year

    # Progress tracking
    progress_bars = {}
    pages_scraped = defaultdict(int)

    def start_requests(self):
        # Load already scraped data if exists
        if os.path.exists('last_10_years_stackoverflow.csv'):
            df = pd.read_csv('last_10_years_stackoverflow.csv')
            self.existing_ids = set(df['QuestionID'].astype(str))

        # Loop over years in reverse (newest first)
        for year, start_page in sorted(self.years_index.items(), reverse=True):
            self.progress_bars[year] = tqdm(
                total=self.max_pages, desc=f"Scraping {year}", position=year % 10, leave=False
            )

            yield scrapy.Request(
                url=f"https://stackoverflow.com/questions?tab=newest&pagesize=50&page={start_page}",
                callback=self.parse,
                meta={'year': year, 'page_num': start_page}
            )

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        questions = soup.find_all('div', class_='s-post-summary js-post-summary')
        stop_scraping = False
        year = response.meta['year']

        for question in questions:
            try:
                # Extract Question ID
                qid = question.get('data-post-id')
                if not qid or qid in self.existing_ids:
                    continue

                # Extract Date
                time_span = question.find('span', class_='relativetime')
                date_str = time_span.get('title').split()[0] if time_span else None
                if not date_str:
                    continue

                y, m, _ = map(int, date_str.split('-'))
                if m < 10:  # stop if data is older than 3 months
                    stop_scraping = True
                    break

                # Extract Tags
                tag_ul = question.find('ul', class_='ml0 list-ls-none js-post-tag-list-wrapper d-inline')
                tags = [a.get_text(strip=True) for a in tag_ul.find_all('a')] if tag_ul else []

                for tag in tags:
                    yield {
                        'Year': year,
                        'QuestionID': qid,
                        'DateTime': date_str,
                        'Tag': tag
                    }

                self.existing_ids.add(qid)

            except Exception as e:
                self.logger.warning(f"[{year}] Skipped due to error: {e}")
                continue

        # Update progress bar
        self.pages_scraped[year] += 1
        self.progress_bars[year].update(1)

        # Stop scraping for this year if date condition met
        if stop_scraping:
            self.progress_bars[year].close()
            self.logger.info(f"✅ Finished scraping year: {year}")
            return

        # Fetch next page if limit not exceeded
        next_page = response.meta['page_num'] + 1
        if next_page - self.years_index[year] < self.max_pages:
            yield scrapy.Request(
                url=f"https://stackoverflow.com/questions?tab=newest&pagesize=50&page={next_page}",
                callback=self.parse,
                meta={'year': year, 'page_num': next_page}
            )
