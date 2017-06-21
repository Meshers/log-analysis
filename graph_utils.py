import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go
import math
import statistics
import sys
import numpy as np

KEY_STAT_MAX = "max"
KEY_STAT_MIN = "min"
KEY_STAT_AVG = "avg"
KEY_STAT_MEDIAN = "median"
KEY_STAT_STD_DEV = "std. deviation"
KEY_STAT_PERCENTILE = "At requested percentile"


def draw_histogram(values, step_size: float, fname: str):
    histogram = go.Histogram(x=values, histnorm='percent',
                             xbins=dict(start=np.min(values), size=step_size, end=np.max(values)),
                             marker=dict(color='rgb(0,0,100)'))

    title = "Probability density graph. The area of each bar is equal to<br> the no of points" + \
            " in the corresponding bin/total no of points"

    layout = dict(
        title=title,
        autosize=True,
        bargap=0.015,
        # height=600,
        # width=700,
        hovermode='x',
        xaxis=dict(
            autorange=True,
            zeroline=False),
        yaxis=dict(
            autorange=True,
            showticklabels=True,
        ))
    fig1 = go.Figure(data=go.Data([histogram]), layout=layout)
    pl.plot(fig1, filename=fname, auto_open=False)


def draw_discovery_graph(df: pd.DataFrame, key_time: str, key_entity: str, fname: str):
    series = df.groupby(by=key_time)[key_entity].unique()
    series.sort_index(inplace=True)
    print(series)
    min_time = int(series.index[0])
    scatter = go.Scatter(
        x=list(map(lambda x: (int(x) - min_time) // 1000, series.index)),
        y=list(map(lambda x: len(x), series)),
        mode='lines+markers',
        name='lines+markers'
    )
    data = [scatter]
    pl.plot(data, filename=fname, auto_open=False)


def get_value_stats(values: list, percentile: int):
    return {
        KEY_STAT_MAX: max(values),
        KEY_STAT_AVG: np.mean(values),
        KEY_STAT_MEDIAN: np.median(values),
        KEY_STAT_PERCENTILE: np.percentile(values, percentile),
        KEY_STAT_STD_DEV: np.std(values)
    }


def get_discovery_latencies(df: pd.DataFrame, key_time, key_entity):
    min_time = min(df[key_time].unique())
    time_entity_series = df.groupby(by=key_entity)[key_time].apply(list)
    dict_entity_latencies = {}
    for entity, times in zip(time_entity_series.index, time_entity_series):
        times.sort()
        latencies = [times[i] - times[i - 1] for i in range(1, len(times))]
        if len(latencies) > 0:
            dict_entity_latencies[entity] = latencies
        else:
            print("WARNING:", entity, "was discovered only at time", (times[0] - min_time) / 1000, file=sys.stderr)

    return dict_entity_latencies


def get_discovery_latency_stats(df: pd.DataFrame, key_time: str, key_entity: str, percentile: int):
    dict_entity_latencies = get_discovery_latencies(df, key_time=key_time, key_entity=key_entity)
    dict_stats = {entity: get_value_stats(times, percentile) for entity, times in dict_entity_latencies.items()}
    return dict_stats


def get_overall_latency_entity_stats(df: pd.DataFrame, key_time: str, key_entity: str, percentile: int):
    """
    rather than putting all latencies of all entities together, the median latency of each entity is chosen as
    representative latency for that entity
    :param df:
    :param key_time:
    :param key_entity:
    :param percentile:
    :return:
    """
    dict_entity_latencies = get_discovery_latencies(df, key_time, key_entity)
    all_latencies = [np.median(latencies) for latencies in dict_entity_latencies.values()]
    return get_value_stats(all_latencies, percentile)


def get_jitter_entity_dict(df: pd.DataFrame, key_time: str, key_entity: str):
    latencies_dict = get_discovery_latencies(df, key_time, key_entity)
    jitter_dict = {entity: [abs(latencies[i] - latencies[i - 1]) for i in range(1, len(latencies))] for entity, latencies
                   in latencies_dict.items() if len(latencies) > 1}
    return jitter_dict


def get_overall_jitter_entity_stats(df: pd.DataFrame, key_time: str, key_entity: str, percentile: int):
    """
    rather than putting all latencies of all entities together, the median jitter of each entity is chosen as
    representative latency for that entity
    :param df:
    :param key_time:
    :param key_entity:
    :param percentile:
    :return:
    """
    dict_entity_jitter = get_jitter_entity_dict(df, key_time, key_entity)
    all_jitters = [np.median(jitters) for jitters in dict_entity_jitter.values()]
    return get_value_stats(all_jitters, percentile)
