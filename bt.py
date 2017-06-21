import pandas as pd
import graph_utils
import statistics
from typing import Iterable
import numpy as np

KEY_START_TIME = "StartTime"
KEY_DISC_TIME = "DiscoveryTime"
KEY_BT_NAME = "Name"
KEY_BT_ADDRESS = "Address"
KEY_WIFI_SSID = "SSID"
KEY_WIFI_BSSID = "BSSID"

OP_KEY_DEVICE = "Device"
OP_KEY_TRIAL = "Trial"
OP_KEY_MIN_LATENCY = "MinLatency"
OP_KEY_MAX_LATENCY = "MaxLatency"
OP_KEY_AVG_LATENCY = "AvgLatency"
OP_KEY_MEDIAN_LATENCY = "MedianLatency"
OP_KEY_MIN_JITTER = "MinJitter"
OP_KEY_MAX_JITTER = "MaxJitter"
OP_KEY_AVG_JITTER = "AvgJitter"
OP_KEY_MEDIAN_JITTER = "MedianJitter"


def get_ambient_wifi_entities(key_entity: str):
    return set(
        np.append(pd.read_csv("opo/WIFI_ambient.csv")[key_entity].unique(),
                  pd.read_csv("samsung/WIFI_ambient.csv")[key_entity].unique())
    )


def get_ambient_bt_entities(key_entity: str):
    if key_entity != KEY_BT_NAME:
        raise Exception("Incompatible ambient entity name!", key_entity)
    return ["Pulzz.D4F3", "Charge 2"]


def get_filtered_df(df_class: pd.DataFrame, ambient_entities: Iterable, key_entity: str):
    return df_class[~df_class[key_entity].isin(ambient_entities)]


def analyze_entity(df_class: pd.DataFrame, ambient_entities: Iterable, key_entity: str, graph_fname_prefix: str):
    df_filtered = get_filtered_df(df_class, ambient_entities, key_entity)

    graph_utils.draw_discovery_graph(df_filtered, key_time=KEY_START_TIME, key_entity=key_entity,
                                     fname=graph_fname_prefix + "_disc.html")

    latencies = [np.median(latencies) for latencies in
                 graph_utils.get_discovery_latencies(df=df_filtered, key_time=KEY_START_TIME,
                                                     key_entity=key_entity).values()
                 ]
    graph_utils.draw_histogram(latencies, step_size=1000, fname=graph_fname_prefix + "_lat.html")

    jitters = [np.median(jitters) for jitters
               in
               graph_utils.get_jitter_entity_dict(df_filtered, key_time=KEY_START_TIME, key_entity=key_entity).values()]
    graph_utils.draw_histogram(jitters, step_size=1000, fname=graph_fname_prefix + "_jitter.html")

    latency_stats = graph_utils.get_discovery_latency_stats(df_filtered, key_time=KEY_START_TIME, key_entity=key_entity,
                                                            percentile=90)
    with open(graph_fname_prefix + "latency", "w") as f:
        print(latency_stats, file=f)

    jitter_stats = graph_utils.get_overall_jitter_entity_stats(df_filtered, key_time=KEY_START_TIME,
                                                               key_entity=key_entity, percentile=90)
    with open(graph_fname_prefix + "jitter", "w") as f:
        print(jitter_stats, file=f)


def analyze_wifi(df_class: pd.DataFrame, ambient_entities: list, key_entity: str, graph_fname_prefix: str):
    df_filtered = get_filtered_df(df_class, ambient_entities, key_entity)
    graph_utils.draw_discovery_graph(df_filtered, key_time=KEY_START_TIME, key_entity=key_entity)


def get_paper_bt_analysis():
    pass


def get_paper_bt_all_scanning_analysis():
    pass


def main():
    df = pd.read_csv("clean_bt_xi_3_2.csv", dtype={KEY_START_TIME: np.int64})
    analyze_entity(df, [], key_entity=KEY_BT_ADDRESS, graph_fname_prefix="bt_xi_3_2")
    # wifi_file_dict = {"opo": ["WIFI_class.csv"], "samsung": ["WIFI_class.csv"], "xiaomi": ["WIFI_class.csv"]}
    # bt_file_dict = {"opo": ["BT_class1.csv", "BT_class2.csv"], "samsung": ["BT_class.csv"], "xiaomi": ["BT_class.csv"]}
    #
    # for device in wifi_file_dict:
    #     for fname in wifi_file_dict[device]:
    #         entity_name = KEY_WIFI_SSID
    #         df_class = pd.read_csv(device + "/" + fname)
    #         ambient_entities = get_ambient_wifi_entities(entity_name)
    #         analyze_entity(df_class, ambient_entities, entity_name, "wifi_" + device + "_" + fname)
    #
    # for device in bt_file_dict:
    #     for fname in bt_file_dict[device]:
    #         entity_name = KEY_BT_NAME
    #         df_class = pd.read_csv(device + "/" + fname)
    #         # ambient_entities = get_ambient_bt_entities(entity_name)
    #         analyze_entity(df_class, [], entity_name, "bt_" + device + "_" + fname)


if __name__ == '__main__':
    main()
