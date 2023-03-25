### IMPORTS

import pandas as pd


### FUNCTIONS

# Primary function to generate balance forecast
def gen_fcst_bal(dt_rng, dt_stt,
                 funds_rowdesc,
                 data_oth,
                 df_mth_sav_rev, df_mth_sav_exp):

    # Set up balance dataframe
    df_mth_sav_bal = pd.DataFrame(0,index = dt_rng, columns = funds_rowdesc)
    
    for idx, row in df_mth_sav_bal.iterrows():
        
        if idx == dt_stt:
            df_mth_sav_bal.loc[idx,'BB'] = data_oth.loc['BB_Sav','Amount']
            df_mth_sav_bal.loc[idx,'ADD'] = df_mth_sav_rev.loc[idx,'REV_TOT']
            df_mth_sav_bal.loc[idx,'WD'] = -df_mth_sav_exp.loc[idx,'EXP_TOT']
            df_mth_sav_bal.loc[idx,'RTN'] = 0
            df_mth_sav_bal.loc[idx,'EB'] = df_mth_sav_bal.loc[idx,'BB'] + df_mth_sav_bal.loc[idx,'ADD'] + df_mth_sav_bal.loc[idx,'WD']
        else:
            df_mth_sav_bal.loc[idx,'BB'] = df_mth_sav_bal.shift(1).loc[idx,'EB']
            df_mth_sav_bal.loc[idx,'ADD'] = df_mth_sav_rev.loc[idx,'REV_TOT']
            df_mth_sav_bal.loc[idx,'WD'] = -df_mth_sav_exp.loc[idx,'EXP_TOT']
            df_mth_sav_bal.loc[idx,'RTN'] = 0
            df_mth_sav_bal.loc[idx,'EB'] = df_mth_sav_bal.loc[idx,'BB'] + df_mth_sav_bal.loc[idx,'ADD'] + df_mth_sav_bal.loc[idx,'WD']
        
    return df_mth_sav_bal
