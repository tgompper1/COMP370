# from random import random
from pathlib import Path
import pandas as pd
import json

from bokeh.layouts import column
from bokeh.plotting import curdoc, figure
from bokeh.models import Dropdown, ColumnDataSource

COMPANY_COLUMN_NAME = "mfr"

dates_boroughs_df = None
# nutrition_columns = None
boroughs = None
borough_lookup = None
borough_reverse_lookup = None

# plot_dataset = ColumnDataSource(dict(company=[], amount=[]))


def get_datafile_path(fname):
    return Path(__file__).parent / fname


def load_boroughs():
    global borough_lookup, borough_reverse_lookup, boroughs
    boroughs_path = get_datafile_path("boroughs.json")

    borough_lookup = json.load(open(boroughs_path, "r"))
    borough_lookup = {k: v.replace(" ", "\n") for k, v in borough_lookup.items()}
    borough_reverse_lookup = {v: k for k, v in borough_lookup.items()}

    boroughs = list(borough_reverse_lookup.keys())


def load_dates_boroughs_df():
    global datFe_boroughs_df, borough_columns

    # Load the data from the CSV file
    csv_path = get_datafile_path("dates_boroughs.csv")
    dates_boroughs_df = pd.read_csv(csv_path)   
    
    # reformat dates
    dates_boroughs_df['createdDate'] = dates_boroughs_df['createdDate'].str.split().str[0]
    dates_boroughs_df['createdDate'] = pd.to_datetime(dates_boroughs_df['createdDate'], format="%m/%d/%Y")

    dates_boroughs_df['closedDate'] = dates_boroughs_df['closedDate'].str.split().str[0]
    dates_boroughs_df['closedDate'] = pd.to_datetime(dates_boroughs_df['closedDate'], format="%m/%d/%Y")

    # get date diff
    dates_boroughs_df['date_diff'] = (dates_boroughs_df['closedDate'] - dates_boroughs_df['createdDate']).dt.days

    # groupby df
    dates_boroughs_df =  dates_boroughs_df.groupby(['date_diff', 'borough']).size().reset_index(name='count')
    



def grab_diff_data(numdays):

    return {
        "borough": boroughs,
        "days": [
            dates_boroughs_df.loc[borough_reverse_lookup[x]][numdays]
            for x in boroughs
        ],
    }


def update_plot(event):
    global plot_dataset

    print(event.item)

    new_data = grab_diff_data(event.item)
    plot_dataset.data = new_data


def main():
    print("Running main")

    global dates_boroughs_df, nutrition_columns, boroughs, plot_dataset

    # data prep section
    load_dates_boroughs_df()
    load_boroughs()

    # visualization section
    p = figure(x_range=[boroughs])  # x_range=["Co1", "Co2", "Co3"])

    p.vbar(
        x="borough",
        top="days",
        source=plot_dataset,
        width=0.9,
        color="blue",
    )

    dropdown = Dropdown(label="Num Days", menu=["0", "1", "2", "3"])
    dropdown.on_event("menu_item_click", update_plot)

    curdoc().add_root(column(dropdown, p))


main()
