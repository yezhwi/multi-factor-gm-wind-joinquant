# 自己使用的工具函数类
import QuantLib as ql
import pandas as pd
from WindPy import w


def get_trading_date_from_now(date_now, diff_periods, period=ql.Days):
    calculation_date = ql.Date(int(date_now.split('-')[2]), int(date_now.split('-')[1]), int(date_now.split('-')[0]))
    calendar = ql.China()
    date_diff = calendar.advance(calculation_date, diff_periods, period).to_date().strftime('%Y-%m-%d')
    return date_diff


def list_gm2wind(list_gm):
    gm2wind_dict = {'SHSE': 'SH', 'SZSE': 'SZ', 'CFFEX': 'CFE', 'SHFE': 'SHF', 'DCE': 'DCE', 'CZCE': 'CZC', 'INE': 'INE'}
    list_wind = [temp.split('.')[1]+'.'+gm2wind_dict[temp.split('.')[0]] for temp in list_gm]
    return list_wind


def list_wind2gm(list_wind):
    wind2gm_dict = {'SH': 'SHSE', 'SZ': 'SZSE', 'CFE': 'CFFEX', 'SHF': 'SHFE', 'DCE': 'DCE', 'CZC': 'CZCE', 'INE': 'INE'}
    list_gm = [wind2gm_dict[temp.split('.')[1]]+'.'+temp.split('.')[0] for temp in list_wind]
    return list_gm


def get_factor_from_wind(code_list, factor_list, date):
    # 还需加入本地存储机制，本地有的数据可以加快读取
    # 用单因子研究\single_factor.py中的因子类直接获取数据
    code_list = list_gm2wind(code_list)
    factors_dfs = []
    for factor in factor_list:
        factor_df = factor(date, code_list).get_factor()
        factors_dfs.append(factor_df)
    factors_df = pd.concat(factors_dfs, axis=1)
    return factors_df


def get_return_from_wind(code_list, date_start, date_end):
    # 还需加入本地存储机制，本地有的数据可以加快读取
    # 从wind上获待选股票收益率数据，为百分比数据，如：3代表3%
    w.start()
    code_list = list_gm2wind(code_list)
    date_start = get_trading_date_from_now(date_start, 1, ql.Days)
    return_data = w.wss(code_list, "pct_chg_per", "startDate="+date_start+";endDate="+date_end).Data[0]
    return_df = pd.DataFrame(data=return_data, index=code_list, columns=['return'])
    return return_df


if __name__ == '__main__':
    print(get_trading_date_from_now('2018-06-17', 0))