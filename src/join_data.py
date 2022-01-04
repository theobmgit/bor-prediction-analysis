import pandas as pd


def join_data():
    # Join by Movie_ID
    data = pd.read_csv("../dataset/data.csv")
    data_mpaa = pd.read_csv("../dataset/data_mpaa.csv")
    data2 = data.merge(data_mpaa, on='Movie_ID', how='left', suffixes=('', '_right'))
    data2 = data2.reset_index(drop=True)
    data2.drop('Movie_Title_right', axis=1, inplace=True)
    data2.to_csv("../dataset/data_joined.csv", index=False)


join_data()
