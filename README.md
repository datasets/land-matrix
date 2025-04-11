<a className="gh-badge" href="https://datahub.io/core/land-matrix"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

The Land Matrix dataset is a comprehensive global database of large-scale land acquisitions and leases. It provides detailed records documenting land deals since 2000, focusing on transactions that involve the conversion of land from local community use or important ecosystem service provision to commercial production.

## Data

The data is sourced from the Land Matrix database (specifically [their API][api]) which in turn compiles information from a variety of sources including research papers, government records, company websites, and media reports.

The dataset includes several key components:

* [Deals data][deals] - Information about land acquisitions including location, size, and purpose
* [Investors data][investors] - Details about the entities involved in land deals
* [Combined database][database] - Merged information providing a comprehensive view of global land acquisitions

The Land Matrix focuses on deals that:
- Target low and middle-income countries
- Have been initiated since the year 2000
- Cover an area of 200 hectares or more
- Entail a transfer of rights to use, control or own land through sale, lease or concession

[api]: https://landmatrix.org/api/
[deals]: https://landmatrix.org/list/deals
[investors]: https://landmatrix.org/list/investors
[database]: https://landmatrix.org/data-downloads/

## Preparation

Process is recorded and automated in python scripts:

```
scripts/process.py     # Downloads and extracts deals.csv and investors.csv
scripts/combine_data.py # Combines the data into a single database.csv file
```

Dependencies are listed in `scripts/requirements.txt` and can be installed with:

```
pip install -r scripts/requirements.txt
```

## Automation

Up-to-date (auto-updates every week) Land Matrix dataset can be found on the datahub.io:
https://datahub.io/core/land-matrix

This repository contains an automated pipeline that regularly fetches and processes data from the Land Matrix API through GitHub Actions, ensuring that analyses are based on the most current information available.

## License

The Land Matrix data is made available under the [Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/) (CC BY-SA 4.0).
