### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt


### FUNCTIONS

# Primary function to generate expense forecast
def gen_fcst_exp(data_exp, data_oth, 
                 dt_stt, dt_rtr, dt_rng):
    
    # Create expense dataframe
    df_mth_sav_exp = pd.DataFrame(
        index = dt_rng, 
        columns = data_exp.index.tolist())
    
    # Creation inflation distributions
    dict_exp_infl = dict()
    
    for cat in data_exp.index:
        dict_exp_infl[cat] = np.random.normal(
            loc = data_exp.loc[cat,'Inflation'], 
            scale = data_exp.loc[cat,'Inflation_SD'], 
            size = data_oth.loc['Dist_Size','Amount'])
        
    # Timeline - Start ---> Start + 1Yr
    for idx, row in df_mth_sav_exp.loc[dt_stt:dt.date(dt_stt.year,12,1),:].iterrows():
        for cat in data_exp.index:
            df_mth_sav_exp.loc[idx, cat] = data_exp.loc[cat, 'Amt_Init_Mth']
            
    # Timeline - Start + 1Yr ---> Retire (Adds YoY inflation)
    for idx, row in df_mth_sav_exp.loc[dt.date(dt_stt.year + 1,1,1):dt_rtr,:].iterrows():
        for cat in data_exp.index:
            df_mth_sav_exp.loc[idx, cat] = df_mth_sav_exp.shift(12).loc[idx,cat] * (
                1 + np.random.choice(dict_exp_infl[cat], 1, replace = False)[0])

    # Timeline - Retire ---> Retire + 1Yr (Resets home, giving, medical, travel and zeros investments)
    for idx, row in df_mth_sav_exp.loc[dt_rtr:dt.date(dt_rtr.year + 1,12,1),:].iterrows():
        for cat in data_exp.index:
            if cat in ['EXP_BRK','EXP_IRA','EXP_FOK']:
                df_mth_sav_exp.loc[idx, cat] = 0
            elif cat in ['EXP_HOM','EXP_GIV','EXP_MED','EXP_TRV']:
                df_mth_sav_exp.loc[idx, cat] = data_exp.loc[cat, 'Amt_Rtr_Mth']
            else:
                df_mth_sav_exp.loc[idx, cat] = df_mth_sav_exp.shift(12).loc[idx,cat] * (
                    1 + np.random.choice(dict_exp_infl[cat], 1, replace = False)[0])

    # Timeline - Retire + 1Yr ---> End (Adds YoY inflation)
    for idx, row in df_mth_sav_exp.loc[dt.date(dt_rtr.year + 1,12,1):,:].iterrows():
        for cat in data_exp.index:
            df_mth_sav_exp.loc[idx, cat] = df_mth_sav_exp.shift(12).loc[idx,cat] * (
                1 + np.random.choice(dict_exp_infl[cat], 1, replace = False)[0])

    # Create total line
    df_mth_sav_exp.loc[:,'EXP_TOT'] = df_mth_sav_exp.T.sum().T

        
    return df_mth_sav_exp
