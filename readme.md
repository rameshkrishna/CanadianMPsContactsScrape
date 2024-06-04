# Canadian MP Contact Scraper

This project is a web scraper built with Scrapy to extract contact details of Canadian Members of Parliament (MPs) from the OurCommons website.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Output](#output)
- [Contributing](#contributing)
- [License](#license)

## Installation

To get started with this project, you'll need to have Python installed on your machine. Follow the steps below to set up the project:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/rameshkrishna/CanadianMPsContactsScrape.git
   cd CanadianMPsContactsScrape
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On macOS and Linux:
     ```sh
     source venv/bin/activate
     ```
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```

4. **Install the required dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

## Usage

To run the scraper and save the contact details to a CSV file, use the following command:

```sh
scrapy crawl ourcommons -o contacts.csv -t csv -s JOBDIR=crawl/spider1
```

This command will start the Scrapy spider named `ourcommons` and save the scraped data to `contacts.csv`.

## Project Structure

```
CanadianMPsContactsScrape/
│
├── scrapy.cfg
├── venv/
├── ourcommons/
│   ├── __init__.py
│   ├── items.py
│   ├── middlewares.py
│   ├── pipelines.py
│   ├── settings.py
│   └── spiders/
│       └── ourcommons.py
├── requirements.txt
└── README.md
```

- **scrapy.cfg**: The configuration file for the Scrapy project.
- **venv/**: The virtual environment directory.
- **ourcommons/**: The main Scrapy project directory.
  - \***\*init**.py\*\*: Marks the directory as a Python package.
  - **items.py**: Defines the data structures for the scraped items.
  - **middlewares.py**: Contains custom middleware components.
  - **pipelines.py**: Handles the post-processing of scraped data.
  - **settings.py**: The project settings.
  - **spiders/**: The directory where the spider code is stored.
    - **ourcommons.py**: The spider for scraping OurCommons.

## Output

The scraper outputs a CSV file named `contacts.csv` containing the following fields:

- Name
- Constituency
- Party
- Email
- Phone number

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure your code follows the project's style guidelines and includes appropriate tests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

