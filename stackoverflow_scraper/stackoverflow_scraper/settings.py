BOT_NAME = 'stackoverflow_scraper'
LOG_FILE = 'scrapy_output.log'
LOG_LEVEL = 'INFO'


SPIDER_MODULES = ['stackoverflow_scraper.spiders']
NEWSPIDER_MODULE = 'stackoverflow_scraper.spiders'

ROBOTSTXT_OBEY = False  # We're ignoring robots.txt for full scraping

# ⚡ Speed and Anti-blocking Settings
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1  # 1 sec between requests to the same domain
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# ✅ AutoThrottle: Adapts speed based on response time
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 0.5  # Start with 1s delay
AUTOTHROTTLE_MAX_DELAY = 5    # Max delay if server is slow
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0  # Keep ~2 parallel requests per server

# 🧠 Smart middlewares (rotate user agents)
DOWNLOADER_MIDDLEWARES = {
    'stackoverflow_scraper.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# ⬇️ Export scraped data
FEED_FORMAT = 'csv'
FEED_URI = 'last_10_years_stackoverflow.csv'
FEED_EXPORT_ENCODING = 'utf-8'

# ✅ Enable retrying failed requests
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry up to 3 times for failed requests
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]  # Too many requests, etc.
