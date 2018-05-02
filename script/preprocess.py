import pandas as pd
import numpy as np
import talking_data as td


def base(df):
    df.loc[:, 'click_time'] = pd.to_datetime(df['click_time'])


def set_time_features(df):
    '''
    ※めっちゃ重い
    1/10 サイズで20分
    '''
    df['weekday'] = df['click_time'].dt.dayofweeek
    df['hour'] = df['click_time'].dt.hour


def set_next_click(df, group_keys):
    '''
    ※めっちゃ重い
    1/10 サイズで20分
    '''

    df['next_click'] = np.abs(df.groupby(group_keys)[
                                  'click_time'
                              ].diff(-1).dt.total_seconds())


def set_prev_click(df, group_keys):
    df['prev_click'] = np.abs(df.groupby(group_keys)[
                                  'click_time'
                              ].diff(1).dt.total_seconds())


def set_ip_count(df):
    ip_count = df.groupby(['ip'])['channel'].count().reset_index()
    ip_count.columns = ['ip', 'clicks_by_ip']
    ip_count['clicks_by_ip'] = ip_count['clicks_by_ip'].astype('uint16')
    df = df.merge(ip_count, on='ip', how='left', sort=False)
    df['clicks_by_ip'] = df['clicks_by_ip'].astype('uint16')
    # df.drop('ip', axis=1, inplace=True)
