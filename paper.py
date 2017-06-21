import graph_utils
import bt
import pandas as pd
import numpy as np


def get_bt_one_scanning_stats(df: pd.DataFrame):
    lat_entity_dict = graph_utils.get_discovery_latencies(df=df, key_entity="BSSID",
                                                          key_time="EndTime")
    lats = []
    ctr = 0
    for device in lat_entity_dict:
        if len(lat_entity_dict[device]) > 7:
            ctr += 1
            lats.extend(lat_entity_dict[device])
    print(ctr)
    print(np.percentile(np.array(lats), 10))
    print(np.percentile(np.array(lats), 30))
    print(np.percentile(np.array(lats), 50))
    print(np.percentile(np.array(lats), 70))
    print(np.percentile(np.array(lats), 90))
    print(np.percentile(np.array(lats), 100))


def main():
    get_bt_one_scanning_stats(pd.read_csv("samsung/WIFI_class.csv", dtype={bt.KEY_START_TIME: np.int64}))


if __name__ == '__main__':
    main()
