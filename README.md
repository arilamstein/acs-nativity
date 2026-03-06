# acs-nativity
[![CI](https://github.com/arilamstein/acs-nativity/actions/workflows/python-package.yml/badge.svg?branch=main&event=push)](https://github.com/arilamstein/acs-nativity/actions/workflows/python-package.yml)

`acs-nativity` is a Python package for analyzing immigration trends in the United States using data from the American Community Survey (ACS). It provides a simple interface for downloading and visualizing data on the native-born and foreign-born population.

The package provides data as a time series covering the full span of ACS 1-year estimates (2005-2024). Under the hood, the package harmonizes two ACS tables: `B05002` (2005-2008) and `B05012` (2009 onward). The 2025 ACS 1-year estimates are expected to be released in September 2026. The Census Bureau did not release ACS 1-year estimates in 2020. 

`acs-nativity` makes it easy to work with data for several geographies covered by the ACS 1-year estimates. This includes the nation, all states, the District of Columbia, all metropolitan statistical areas, and all counties and places (i.e., towns or cities) with populations of 65,000 or more.

The package exposes three functions:

  * `get_nativity_timeseries()` - Downloads ACS nativity data and returns a dataframe covering all available ACS 1-year estimates for the given geography.
  * `plot_nativity_timeseries()` - Creates a time series visualization of nativity data.
  * `plot_nativity_change()` - Creates a bar chart showing the year-to-year change in a nativity measure.

## Installation

Install directly from GitHub:

```sh
pip install git+https://github.com/arilamstein/acs-nativity.git
```

## Example Workflow

The example below walks you through getting historic nativity data for the entire country, graphing it as a time series, and graphing the year-over-year changes.

### Getting Data

The code below will get nativity data for the entire country over the course of the entire ACS (2005-2024):
```python
from acs_nativity import (
    get_nativity_timeseries,
    plot_nativity_timeseries,
    plot_nativity_change,
)

df = get_nativity_timeseries(us="*")
df.head(1)
```
```text
   Name           Year  Total      Native     Foreign-born  Percent Foreign-born
0  United States  2005  288378137  252688295  35689842      12.376057
```
The parameter `us="*"` tells `get_nativity_timeseries` to return data for the entire country. The key columns are `Total`, `Native`, `Foreign-born`, and `Percent Foreign-born`. Those columns are provided for all geographies.

### Graphing Time Series

To plot a time series of the dataframe, call `plot_nativity_timeseries` and specify the column you want to chart. Most chart details (e.g., title and axis labels) are handled automatically, and annotations show when presidential administrations changed.

```python
fig = plot_nativity_timeseries(df, column="Foreign-born")
fig.show()
```

**Note:** In Jupyter notebooks, you can simply call `plot_nativity_timeseries(df, column="Foreign-born")` as the last line of a cell and the figure will render automatically. In a Python REPL or script, assign the figure to a variable and call `.show()`.

 ![Foreign-Born Population](images/nativity_us.png)

This graph shows that the foreign-born population has increased steadily since 2005, with a particularly large increase during the Biden administration.

### Graphing Year-over-Year Change

Sometimes it is helpful to show the year-over-year changes instead of raw values. To do that, call `plot_nativity_change` with a dataframe and a column: 

```python
fig = plot_nativity_change(df, column="Foreign-born")
fig.show()
```

**Note:** In Jupyter notebooks, you can simply call `plot_nativity_timeseries(df, column="Foreign-born")` as the last line of a cell and the figure will render automatically. In a Python REPL or script, assign the figure to a variable and call `.show()`.

![Year-over-Year Change](images/nativity_us_diff.png)

This chart makes it clear that the only year when the foreign-born population decreased was 2008.

## Choosing a Geography

`get_nativity_timeseries` can provide data for several geographies covered by the ACS 1-year estimates. This includes the nation, all states, the District of Columbia, all metropolitan statistical areas, and all counties and places (i.e., towns or cities) with populations of 65,000 or more.

To specify a geography, `acs-nativity` follows the same conventions as the `censusdis` package, which provides convenient constants for identifying Census geographies.

A geography is specified using a keyword argument where:

  * the keyword identifies the geography type (such as `state`)
  * the value is a constant imported from a `censusdis` module (such as `censusdis.states`)

Installing `acs-nativity` automatically installs `censusdis`, so these constants are available once the package is installed.

Below are examples for several common geographies.

| Geography | Module | Example |
|---|---|---|
| United States | — | `df = get_nativity_timeseries(us="*")` |
| State | `censusdis.states` | `from censusdis.states import MN`<br>`df = get_nativity_timeseries(state=MN)` |
| County | `censusdis.counties.<state_name>` | `from censusdis.states import NY`<br>`from censusdis.counties.new_york import NASSAU`<br>`df = get_nativity_timeseries(state=NY, county=NASSAU)` |
| City | `censusdis.places.<state_name>` | `from censusdis.states import IL`<br>`from censusdis.places.illinois import CHICAGO_CITY`<br>`df = get_nativity_timeseries(state=IL, place=CHICAGO_CITY)` |
| Metropolitan Statistical Area (MSA) | `censusdis.msa_msa` | `from censusdis.msa_msa import EL_PASO_TX_METRO_AREA`<br>`df = get_nativity_timeseries(` <br>`    metropolitan_statistical_area_micropolitan_statistical_area=`<br>`    EL_PASO_TX_METRO_AREA`<br>`)` |

You can learn more in the [Additional Geographies](https://censusdis.readthedocs.io/en/stable/intro.html#additional-geographies) section of the `censusdis` documentation. 
