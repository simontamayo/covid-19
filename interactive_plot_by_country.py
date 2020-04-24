# ### Code to create an interactive plot with recorded cases and percentage changes
# ##### for questions contact simon_tamayo@mckinsey.com
# In order to run this script you must have an input dataframe (df_) with COVID19 data
# with the following columns ['Date', 'Country', "Confirmed", "Recovered", "Deaths"]

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly as py


def main():
    print("This script creates an interactive Contry report of COVID19 cases")
    # Load input data
    df_ = pd.read_csv("./data/countries-aggregated.csv")

    # Filter by country
    country = "Chile"
    df_col = df_[df_["Country"] == country]

    # Reindex by date in order to gather only a given timelapse
    df_col["Date"] = pd.to_datetime(df_col["Date"], format="%Y-%m-%d")
    df_col.set_index("Date", inplace=True)
    df_col = df_col.loc["2020-03-01":].copy()

    # Create dictionnaries in order to have homogeneous colors and symbols
    dict_colors = {"Deaths": "red", "Confirmed": "navy", "Recovered": "Gray"}
    dict_symbol = {
        "Deaths": "triangle-down",
        "Confirmed": "circle",
        "Recovered": "triangle-up",
    }
    dict_sizes = {"Deaths": 8, "Confirmed": 5, "Recovered": 8}

    # Create a plotly figure with 3 subplots
    fig = make_subplots(
        rows=3,
        cols=1,
        row_heights=[0.7, 0.15, 0.15],
        shared_xaxes=True,
        vertical_spacing=0.02,
    )

    # Add traces to the first subplot with scatter lines
    for c in ["Confirmed", "Recovered", "Deaths"]:
        fig.add_trace(
            go.Scatter(
                x=df_col.index,
                y=df_col[c],
                mode="lines+markers",
                marker_symbol=dict_symbol[c],
                name=c,
                marker=dict(color=dict_colors[c], size=dict_sizes[c]),
            ),
            row=1,
            col=1,
        )

    # Add a trace to the 2nd subplot with an area plot of "Confimed" percentage change
    fig.add_trace(
        go.Scatter(
            x=df_col.index,
            y=(100 * df_col["Confirmed"].pct_change()).round(1),
            marker_color=dict_colors["Confirmed"],
            marker_symbol=dict_symbol["Confirmed"],
            name="%change " + str("Confirmed"),
            stackgroup="one",
        ),
        row=2,
        col=1,
    )

    # Add a trace to the 3rd subplot with an area plot of "Deaths" percentage change
    fig.add_trace(
        go.Scatter(
            x=df_col.index,
            y=(100 * df_col["Deaths"].pct_change()).round(1),
            marker_color=dict_colors["Deaths"],
            marker_symbol=dict_symbol["Deaths"],
            name="%change " + str("Deaths"),
            stackgroup="one",
        ),
        row=3,
        col=1,
    )

    # Update layout with title and graphic settings
    fig.update_layout(
        title_text="COID19 report " + country,
        template="ggplot2",
        autosize=False,
        width=1000,
        height=600,
        margin=dict(l=10, r=10, b=10, t=50),
    )

    # Save and show
    py.offline.plot(
        fig,
        filename="./results/" + country + "_" + str(df_col.index[-1].date()) + ".html",
        auto_open=False,
    )
    fig.show()


if __name__ == "__main__":
    main()
