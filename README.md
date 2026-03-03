# acs-nativity

A lightweight Python library for retrieving and visualizing historical ACS 1-Year nativity data for the United States and other Census geographies.

It provides tools to examine:

  - The size of the foreign-born population
  - Year-over-year changes in that population
  - Trends at national, state, county, or city levels

Data comes from the U.S. Census Bureau’s American Community Survey (ACS) 1-Year Estimates.

## Installation

Install directly from GitHub:

```sh
pip install git+https://github.com/arilamstein/acs-nativity.git
```

## Quick Example

```python
from acs_nativity import (
    get_nativity_timeseries,
    plot_nativity_timeseries,
    plot_nativity_change,
)

# Retrieve national data
df = get_nativity_timeseries(us="*")

# Plot total foreign-born population
plot_nativity_timeseries(
    df,
    column="Foreign-born",
    title="Foreign-Born Population in the United States<br>ACS 1-Year Estimates",
    y_label="Population",
)
```

![Foreign-Born Population](images/nativity_us.png)

```python
# Plot year-over-year change
plot_nativity_change(
    df,
    column="Foreign-born",
    title="Change in the US Foreign-Born Population<br>ACS 1-Year Estimates",
)
```

![Year-over-Year Change](images/nativity_us_diff.png)

## Learning More

To learn more about how to use `acs-nativity`, including how to work with other geographies (such as individual states and counties), see [Getting Started Notebook](notebooks/getting_started.ipynb).