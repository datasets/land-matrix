<a className="gh-badge" href="https://datahub.io/core/land-matrix"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# Land Matrix Data Files

This directory contains CSV files extracted from the Land Matrix API:

- `deals.csv`: Contains information about land deals
- `investors.csv`: Contains information about investors

These files are automatically updated weekly via GitHub Actions.

## Data Source

Data is sourced from the Land Matrix API: https://landmatrix.org/api/legacy_export/

## Last Updated

This data was last updated on: 2025-04-11

> Note: The date will be updated when the GitHub Action runs.

## Automation

The data is automatically updated using a GitHub Action. See `.github/workflows/update-data.yml` for details.

### Openness and Licensing

The [Disclaimer and License page](http://landportal.info/landmatrix/index.php#pages-disclaimer) links to [terms and conditions](http://landportal.info/page/terms-and-conditions-use). The only specific reference to a license therein (which seems to be for entire website and not just database) is within No contract section where it states:

> ... Furthermore, the coordinators of the Land Portal may add, change, improve, or update the information of the website without notice and may in its sole discretion alter, limit or discontinue part of this site or deny at its sole discretion any user access to this site or any portion thereof.
> 
> For more information, see Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License.

This license is, of course, not open as per the http://OpenDefinition.org/ due to its non-commercial restriction.
