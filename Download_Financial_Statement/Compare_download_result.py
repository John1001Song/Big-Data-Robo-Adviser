import os
from os.path import isfile, join
from os import listdir
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile

N_fs_growth_ann_path = '../datasets/NASDAQ/financial_statement/growth/annual/'
N_fs_growth_qua_path = '../datasets/NASDAQ/financial_statement/growth/quarterly/'
N_stock_path = '../datasets/NASDAQ/stock_price/'

def get_all_file_name(file_path, file_format):
    # get all files names
    files_names = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    name_array = []

    for name in files_names:
        if file_format in name:
            name_array.append(name)

    return name_array

def match(ann_list, qua_list):
    for ann_ele in ann_list:
        if ann_ele not in qua_list:
            print('annual file: ', ann_ele, ' is not in the quarterly folder')

    for quar_ele in qua_list:
        if quar_ele not in ann_list:
            print('quarterly file: ', quar_ele, 'is not in the annual folder')

if __name__ == '__main__':
    ann_list = get_all_file_name(N_fs_growth_ann_path, '.xlsx')
    qua_list = get_all_file_name(N_fs_growth_qua_path, '.xlsx')
    stock_list = get_all_file_name(N_stock_path, '.csv')
    print(len(ann_list))
    print(len(qua_list))
    print(len(stock_list))
    match(ann_list, qua_list)