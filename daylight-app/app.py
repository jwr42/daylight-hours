# """
# Title: Daylight App
# Author: Jonathan Roberts
# """

# import modules
import requests
import pandas as pd
from shiny.express import input, render, ui
from shiny import reactive
from shinywidgets import render_widget
import ipyleaflet as Map
from datetime import datetime
from shinyswatch import theme

# location options
cities = {
    "Null Island": (0, 0),
    "Cardiff": (51.483333, -3.183333),
    "London": (51.507222, -0.1275),
    "Edinburgh": (55.953333, -3.189167),
    "Belfast": (54.596389, -5.93),
}

# --------------------------------------------------------
# Shiny Application UI Elements
# --------------------------------------------------------

ui.page_opts(title="☀️ Daylight Time")

with ui.sidebar():
    ui.input_select("city", "Select City", choices=list(cities.keys()), selected="London")
    ui.input_date("date", "Select Date")
    "Toggle Dark Mode"
    ui.input_dark_mode(mode="light")
    ui.input_action_button("show_info", "App Info")


with ui.layout_column_wrap(fill=False):

    with ui.value_box():
        "Sunrise"

        @render.express
        def sunrise():
            get_df().results["sunrise"]

    with ui.value_box():
        "Sunset"

        @render.express
        def sunset():
            get_df().results["sunset"]

    with ui.value_box():
        "Day Length"

        @render.express
        def day_length():
            get_df().results["day_length"]

    with ui.value_box():
        "Date"

        @render.express
        def date_selected():
            input.date().strftime("%d %b %Y")

with ui.card():
    ui.card_header("Map")

    @render_widget
    def map():
        return Map.Map(zoom=12, center=cities[input.city()])

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

@reactive.calc
def get_df():
    city = input.city()
    date = input.date()
    # post request to the api
    url = 'https://api.sunrisesunset.io/json?'
    params = {
        "lat": cities[city][0],
        "lng": cities[city][1],
        "date": date,
    }
    r = requests.post(url, params=params)
    df = pd.DataFrame(r.json())
    return df


@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_select("city")


@reactive.effect
@reactive.event(input.show_info)
def show_important_message():
    m = ui.modal(
        ui.markdown("This shiny python app displays the sunrise and sunset time, as well as the length of daylight time for the selected day. The application submits post requests to the [Sunrise Sunset API](https://sunrisesunset.io/api/) for a slection of cities across the United Kingdom."),
        title="Application Information",
        easy_close=True,
        footer=None,
    )
    ui.modal_show(m)
