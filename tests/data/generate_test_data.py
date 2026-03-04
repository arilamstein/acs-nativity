"""
Generate small datasets used during development.

These CSV files allow features like plotting and automatic title
generation to be tested without repeatedly calling the Census API.

Run this script manually to regenerate the datasets in tests/data/.
"""

from pathlib import Path

from acs_nativity import get_nativity_timeseries

# State codes
from censusdis.states import CA, NY

# County codes
from censusdis.counties.new_york import NASSAU

# Place codes
from censusdis.places.new_york import NEW_YORK_CITY

DATA_DIR = Path(__file__).parent


# National data
df = get_nativity_timeseries(us="*")
df.to_csv(DATA_DIR / "data_us.csv", index=False)


# State data
df = get_nativity_timeseries(state=CA)
df.to_csv(DATA_DIR / "data_state.csv", index=False)


# County data
df = get_nativity_timeseries(state=NY, county=NASSAU)
df.to_csv(DATA_DIR / "data_county.csv", index=False)


# Place data
df = get_nativity_timeseries(state=NY, place=NEW_YORK_CITY)
df.to_csv(DATA_DIR / "data_place.csv", index=False)
