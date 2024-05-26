
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


scrapy crawl ourcommons -o contacts.csv -t csv -s JOBDIR=crawl/spider1