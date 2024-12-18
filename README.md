# Linkedin Scrapping Module

## Getting Started

Usage example:

```Python
    from time import sleep

search_query = 'Quality assurance'
location = 'Calgary, AB, Canada'
jobs = []
retries = 5
retry_count = 0
wait_threshold = 1

linkedin = LinkedInScraper(query_search=search_query, location=location)

while not jobs:
    linkedin.get_new_jobs_data()

    print(f"Going to sleep for {wait_threshold} seconds (retry: {retry_count}/{retries})...")
    sleep(wait_threshold)

    wait_threshold += wait_threshold
    retry_count += 1

    if retry_count == retries:
        break

df = linkedin.convert_to_dataframe()

if jobs:
    print(f"Source: {jobs}")
```

## Contributing

This project welcomes contributions and suggestions. For details, visit the repository's [Contributor License Agreement (CLA)](https://cla.opensource.microsoft.com) and [Code of Conduct](https://opensource.microsoft.com/codeofconduct/) pages.
