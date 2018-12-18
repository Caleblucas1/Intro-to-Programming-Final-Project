# All imports
import sqlalchemy
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame
from numpy import genfromtxt
import re

#read entire table from wikipedia into an object
tables = pd.read_html("https://en.wikipedia.org/wiki/Farebox_recovery_ratio", skiprows=1)[0]

#create separate objects for each column in the table
continent = tables[0]
Country = tables[1]
System = tables[2]
Ratios = tables[3]
Fare_system = tables[4]
Fare_rate = tables[5]
Year = tables[6]
#print(type(System))


#cleaning up the ratio from percentage to decimal float
def CleanRatio(raw_ratio):
    s = raw_ratio.split("%")
    return float(s[0])/100.00

clean_ratios = []
for cells in Ratios:
    clean_ratios.append(CleanRatio(cells))
#print(clean_ratios)

#Cleaning up the fare system column, taking only the first two words in each column, ignoring hybrid systems
def SimpleFareSystem(raw_fare_system):
    n = str(raw_fare_system).split()[:2]
    return n

clean_Fare_system = []
for cells in Fare_system:
    clean_Fare_system.append(SimpleFareSystem(cells))
#print(clean_Fare_system)

#Cleaning up the fare rate column, keeping only the float number
def SimpleFareRate(raw_fare_rate):
    num = re.findall(r"[-+]?\d*\.\d+|\d+", str(raw_fare_rate))
    if len(num) >= 1:
        return float(num[0])
    else:
        return None

Clean_Fare_rate = []
for cells in Fare_rate:
    Clean_Fare_rate.append(SimpleFareRate(cells))
#print(Clean_Fare_rate)

#Changing all fare rates to USD
country_lst = list(Country)
Currency_conversion = {
                        "US": 1,
                        "Hong Kong": 0.13,
                        "Japan": 0.0088,
                        "Pakistan": 0.0072,
                        "Taiwan": 0.032,
                        "Singapore": 0.73,
                        "China": 0.14,
                        "Netherlands": 0.56,
                        "Germany": 1.13,
                        "Belgium": 1.13,
                        "Denmark": 0.15,
                        "UK": 1.26,
                        "Spain": 1.13,
                        "Italy": 1.13,
                        "Czech Republic": 0.044,
                        "France": 1.13,
                        "Sweden": 0.11,
                        "Austria": 1.13,
                        "Finland": 1.13,
                        "Switzerland": 1.01,
                        "Canada": 0.75,
                        "New Zealand": 0.69,
                        "Australia": 0.72
                        }

fare_in_usd = []
for country, fare in zip(country_lst, Clean_Fare_rate):
    if country in Currency_conversion.keys() and fare is not None:
        fare_in_usd.append(Currency_conversion[country] * fare)
    else:
        fare_in_usd.append(None)
#print(fare_in_usd)

#Cleaning up the Year column, taking out all footnotes and taking the first year when it is between the two years
year_lst = list(Year)
def CleanYear(raw_year):
    numb = re.findall(r"[-+]?\d*\.\d+|\d+", str(raw_year))
    return numb[0]

clean_years = []
for j in year_lst:
    clean_years.append(CleanYear(j))
# print(clean_years)

#Import database to sqlite DataFrame "tables"
from sqlalchemy import create_engine
engine = create_engine("sqlite:///:Farebox:", echo=True)
df = pd.DataFrame(tables)
df.to_sql('tables', con=engine) # Cant query with this code displayed- ValueError: Table 'tables' already exists
#print(df) # this is the same as tables object from above

# Shows me the table in SQL
from sqlalchemy import inspect
db_uri = "sqlite:///:Farebox:"
engine = create_engine(db_uri)
inspector = inspect(engine)

print(inspector.get_table_names(tables))
# engine.execute("Select * from tables").fetchall()