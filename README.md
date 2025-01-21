# LinkedIn Scrapping Module

A powerful Python module for scraping job listings from LinkedIn with customizable search parameters and automatic retry mechanisms.

## Features

- Custom job search queries
- Location-based filtering
- Automatic retry mechanism
- Data export to DataFrame
- Configurable wait times
- Easy to integrate

## Installation

Install the module using pip:

```bash
pip install git+https://github.com/icecore2/linkedin_scrapper_module.git
```

## Usage

Here's a simple example to get you started:
```python
from linkedin_scrapper import LinkedInScraper
from time import sleep

# Configure search parameters
search_query = 'Quality assurance'
location = 'Calgary, AB, Canada'
jobs = []
retries = 5
retry_count = 0
wait_threshold = 1

# Initialize scraper
linkedin = LinkedInScraper(query_search=search_query, location=location)

# Fetch jobs with retry mechanism
while not jobs:
    linkedin.get_new_jobs_data()

    print(f"Going to sleep for {wait_threshold} seconds (retry: {retry_count}/{retries})...")
    sleep(wait_threshold)

    wait_threshold += wait_threshold
    retry_count += 1

    if retry_count == retries:
        break

# Convert results to DataFrame
df = linkedin.convert_to_dataframe()

if jobs:
    print(f"Source: {jobs}")
```

## Configuration Options
* `query_search`: Job search keywords
* `location`: Geographic location for job search
* `retries`: Number of retry attempts
* `wait_threshold`: Initial wait time between retries

## Data Output
The scraper returns job data including:
* Job title
* Company name
* Location
* Job description
* Posted date
* And more...

## Requirements
* Python 3.8+
* pandas
* requests
* beautifulsoup4

## Contributing
We welcome contributions! Please follow these steps:
* Fork the repository
* Create your feature branch (`git checkout -b feature/amazing-feature`)
* Commit your changes (`git commit -m 'Add amazing feature'`)
* Push to the branch (`git push origin feature/amazing-feature`)
* Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support, please open an issue in the GitHub repository.

## Acknowledgments
* LinkedIn for providing the job data platform
* All contributors who have helped improve this module
