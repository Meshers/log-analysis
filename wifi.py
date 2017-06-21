import pandas as pd
import graph_utils


import datetime

KEY_START_TIME = "StartTime"
KEY_END_TIME = "EndTime"
KEY_SSID = "SSID"
KEY_BSSID = "BSSID"


def main():
    new_df = pd.read_csv("wifi_galaxy_new.csv")
    old_df = pd.read_csv("opo_false.csv")
    filtered_df = new_df[~new_df[KEY_SSID].isin(old_df[KEY_SSID])]
    print(len(filtered_df[KEY_START_TIME].unique()))
    print(len(filtered_df[KEY_SSID].unique()))
    series = filtered_df.groupby(by=KEY_START_TIME)[KEY_SSID].unique()
    max_element, index = max(zip(series, series.index), key=lambda x: len(x[0]))
    print(len(max_element))
    print(index)
    graph_utils.draw_discovery_graph(filtered_df, key_time=KEY_START_TIME, key_entity=KEY_SSID)


if __name__ == '__main__':
    main()
