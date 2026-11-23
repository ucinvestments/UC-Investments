# UC Investment Explorer
All code used to make: http://ucinvestments.info/ (as of May 2nd 2024).

## Refresh explorer data

From the repository root, install `Finance/requirements.txt` in a Python 3.11+
environment and run:

```sh
python -m pip install -r Finance/requirements.txt
python Finance/run_all.py
```

The command discovers the latest holdings PDFs linked from the official UCRP
and GEP policy pages, checks the PDF line items against the printed investment
totals, and validates the latest Regents Form 13F against its cover sheet. It
fetches dated proxy holdings for matched funds and writes one validated snapshot
to `Webapp/static/data/holdings-snapshot.json`. A failed refresh leaves the
previous snapshot in place. Use `--output PATH` to generate a separate snapshot
for inspection. Set `SEC_USER_AGENT` to your organization and contact email if
running this refresh for your own deployment.

The Companies view uses estimated exposures and cites the source and date of
each proxy. The Regents 13F view shows reported securities separately because
its coverage and reporting period differ. The existing named targets such as
`python Finance/run_all.py pdf` produce intermediate research files and do not
publish an explorer snapshot.

Matched fund details include dates and links for UC’s private equity and
alternative investment fee reports. These figures supplement the holdings
records. The Regents 13F view identifies UCBG by CUSIP and calculates indirect
equity exposure only when the ETF holdings and the 13F report date match.

The Resources page links the campus endowments view and its downloadable data. Refresh that separate
dataset with `python Finance/scrapers/campus_endowments.py`. Some campus
endowment assets already appear in UC investment pool disclosures.

Run the refresh regression tests with
`python -m unittest discover -s Finance/tests`.

## Scheduled refresh

GitHub Actions checks for new data on Mondays at 16:23 UTC. The workflow
validates both datasets and opens one review PR when the data changes. Merging
that PR updates the files used by the site's next deployment. A failed run
leaves the current data in place. Follow **Refresh explorer data** under
Actions and enable failed workflow notifications in GitHub to receive alerts.

The repository must allow GitHub Actions to create pull requests. Maintainers
can also run the workflow on the default branch from the Actions tab.

## Contributing

We welcome pull requests with better sources for fund composition. The
explorer shows where holdings have no company breakdown. The historical
`Data-Collection/csv-files/` directory has examples of earlier contributions.

Thank you <3  
