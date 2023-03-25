### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt


### FUNCTIONS

# Primary function to generate forecast for a specified investment account
def gen_inv_df(dt_rng, dt_stt, dt_wd, dt_rtr,
                funds_rowdesc, 
                bb, wd_init, 
                srs_exp,srs_rtn, 
                fok_match, sal_growth,
                rtn_dcy, rt_infl):
    
    df = pd.DataFrame(index = dt_rng, columns = funds_rowdesc)    
    df_fok_match = pd.DataFrame(index = dt_rng, columns = ['Amount'])

    # Populate 401K match dataframe
    for idx, row in df_fok_match.iterrows():
        if (idx >= dt_stt) and (idx < dt.date(dt_stt.year + 1,1,1)):
            df_fok_match.loc[idx,'Amount'] = fok_match
        elif (idx >= dt.date(dt_stt.year,1,1)) and (idx < dt_rtr):
            df_fok_match.loc[idx,'Amount'] = df_fok_match.shift(12).loc[idx,'Amount'] * sal_growth
        elif idx >= dt_rtr:
            df_fok_match.loc[idx,'Amount'] = 0
    
    # Populate investment fund rollforward
    for idx, row in df.iterrows():
        if idx == dt_stt:
            df.loc[idx,'BB'] = bb
            df.loc[idx,'ADD'] = srs_exp[idx] + df_fok_match.loc[idx,'Amount']
            df.loc[idx,'WD'] = 0
            df.loc[idx,'RTN'] = (df.loc[idx,'BB'] + df.loc[idx,'ADD']) * np.random.choice(srs_rtn, 1, replace = False)[0] * (rtn_dcy ** df.index.get_loc(idx))
            df.loc[idx,'EB'] = df.loc[idx,'BB'] + df.loc[idx,'ADD'] + df.loc[idx,'WD'] + df.loc[idx,'RTN']
        elif (idx > dt_stt) and (idx < dt_wd):
            df.loc[idx,'BB'] = df.shift(1).loc[idx,'EB']
            df.loc[idx,'ADD'] = srs_exp[idx] + df_fok_match.loc[idx,'Amount']
            df.loc[idx,'WD'] = 0
            df.loc[idx,'RTN'] = (df.loc[idx,'BB'] + df.loc[idx,'ADD']) * np.random.choice(srs_rtn, 1, replace = False)[0] * (rtn_dcy ** df.index.get_loc(idx))
            df.loc[idx,'EB'] = df.loc[idx,'BB'] + df.loc[idx,'ADD'] + df.loc[idx,'WD'] + df.loc[idx,'RTN']
        elif (idx >= dt_wd) and (idx < dt.date(dt_wd.year + 1,1,1)):
            df.loc[idx,'BB'] = df.shift(1).loc[idx,'EB']
            df.loc[idx,'ADD'] = srs_exp[idx] + df_fok_match.loc[idx,'Amount']
            df.loc[idx,'WD'] = wd_init
            df.loc[idx,'RTN'] = (df.loc[idx,'BB'] + df.loc[idx,'ADD']) * np.random.choice(srs_rtn, 1, replace = False)[0] * (rtn_dcy ** df.index.get_loc(idx))
            df.loc[idx,'EB'] = df.loc[idx,'BB'] + df.loc[idx,'ADD'] + df.loc[idx,'WD'] + df.loc[idx,'RTN']
        elif (idx >= dt.date(dt_wd.year + 1,1,1)):
            if df.shift(1).loc[idx,'EB'] > 0:
                df.loc[idx,'BB'] = df.shift(1).loc[idx,'EB']
                df.loc[idx,'ADD'] = srs_exp[idx] + df_fok_match.loc[idx,'Amount']
                df.loc[idx,'WD'] = df.shift(12).loc[idx,'WD'] * (1 + rt_infl)
                df.loc[idx,'RTN'] = (df.loc[idx,'BB'] + df.loc[idx,'ADD']) * np.random.choice(srs_rtn, 1, replace = False)[0] * (rtn_dcy ** df.index.get_loc(idx))
                df.loc[idx,'EB'] = df.loc[idx,'BB'] + df.loc[idx,'ADD'] + df.loc[idx,'WD'] + df.loc[idx,'RTN']
            elif df.shift(1).loc[idx,'EB'] <= 0:
                df.loc[idx,'BB'] = df.shift(1).loc[idx,'EB']
                df.loc[idx,'ADD'] = srs_exp[idx] + df_fok_match.loc[idx,'Amount']
                df.loc[idx,'WD'] = 0
                df.loc[idx,'RTN'] = 0
                df.loc[idx,'EB'] = df.loc[idx,'BB'] + df.loc[idx,'ADD'] + df.loc[idx,'WD'] + df.loc[idx,'RTN']
                
    return df
