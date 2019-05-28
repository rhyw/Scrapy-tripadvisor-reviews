# Scrapy-tripadvisor-reviews
Using scrapy to scrape tripadvisor in order to get users' reviews.

The code in this repository was used to scrape and gather data from tripadvisor about some brazilian cities attractions. The data were used to train a sentiment analysis classifier used in https://github.com/igorbpf/Twitter-Sentiment (https://twisentiment.herokuapp.com/). 

# Setup
Install dependencies(under project rood dir, virtualenv preferred):

$ virtualenv --python=/usr/bin/python2.7 .env
$ source .env/bin/activate
$ pip install -r requirements.txt

# Usage
In the project's root folder, update "urls.txt" with the URLs you'd like to crawl tripadvisor reviews from, and then type:

$ scrapy crawl tripadvisor -o tripadvisor_reviews.csv

# Resume crawls
There're chances a large crawl job fails, following command makes sure it can be resumed(still rely on non-expire cookies), see also: https://docs.scrapy.org/en/latest/topics/jobs.html

$ scrapy crawl tripadvisor -s JOBDIR=./crawls/mycraps-1 -o tripadvisor_reviews.csv

Where './crawls/mycraps-1' is the directory where crawling state gets persisted. With command above, you'll be able to softly stop the spider job(by hitting Ctrl-C once) and resume shortly afterwards, with exactly the same command.

The reviews will be stored in a csv file named tripadvisor_reviews.csv
