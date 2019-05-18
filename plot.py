#!/usr/bin/env python
# coding=utf-8
import pandas as pd
import plotly as py
import plotly.graph_objs as go


def plot(df, filename, layout):
    grinders = df.index.values
    buckets = df.columns.values
    data = [
        go.Scatter(
            x=buckets,
            y=df.loc[grinder],
            mode='lines+markers',
            line=dict(
                shape='spline',
                width=1,
                smoothing=0.8
            ),
            marker=dict(
                size=3,
            ),
            name=grinder
        )
        for grinder in grinders
    ]
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename=filename, auto_open=True)


if __name__ == "__main__":
    df_non_cumulative = pd.read_csv('grinders.csv', index_col=0)
    print("Non-cumulative distribution:")
    print(df_non_cumulative)
    df_cumulative = df_non_cumulative.cumsum(axis=1)
    df_cumulative = pd.DataFrame(
        data=df_cumulative.iloc[:, 0:-1].values,
        index=df_cumulative.index,
        columns=[0, 400, 800, 1200, 1600, float('inf')]
    )
    print("Cumulative distribution:")
    print(df_cumulative)

    cumulative_layout = go.Layout(
        title="Grind Distribution (cumulative)",
        xaxis=dict(
            dtick=25,
            range=(0, 1600),
            fixedrange=True,
        ),
        yaxis=dict(
            dtick=0.05,
            tickformat=",.0%",
            fixedrange=True,
            range=(0, 1.01),
        )
    )
    non_cumulative_layout = go.Layout(
        title="Grind Distribution (non-cumulative)",
        xaxis=dict(
            fixedrange=True,
        ),
        yaxis=dict(
            dtick=0.05,
            tickformat=",.0%",
            fixedrange=True,
            range=(0, 0.6),
        )
    )
    plot(df=df_non_cumulative, filename="noncumulative.html", layout=non_cumulative_layout)
    plot(df=df_cumulative, filename="cumulative.html", layout=cumulative_layout)
