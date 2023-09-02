### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt


### FUNCTIONS

# Main function to generate revenue forecast
def gen_fcst_rev(dt_rng, dt_stt, dt_rtr, dt_ssi,
                 rev_cat,
                 rev_sal, rev_gif, rev_oth, rev_ssi,
                 gr_sal, gr_ssi,
                 inv_brk, inv_ira, inv_fok,
                 rt_tax_sal):

    # Create dataframe
    df_mth_sav_rev = pd.DataFrame(index = dt_rng, columns = rev_cat)
    
    # Timeline - Start ---> Start + 1Yr
    for idx, row in df_mth_sav_rev.loc[dt_stt:dt.date(dt_stt.year,12,1),:].iterrows():
        df_mth_sav_rev.loc[idx,'REV_SAL'] = rev_sal * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_SSI'] = 0
        df_mth_sav_rev.loc[idx,'REV_GIF'] = rev_gif if idx.month in (2,12) else 0
        df_mth_sav_rev.loc[idx,'REV_OTH'] = rev_oth
        df_mth_sav_rev.loc[idx,'REV_BRK'] = -inv_brk.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_IRA'] = -inv_ira.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_FOK'] = -inv_fok.loc[idx,'WD'] * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_TOT'] = df_mth_sav_rev.loc[idx,:].sum()
    
    # Timeline - Start + 1Yr ---> Retire
    for idx, row in df_mth_sav_rev.loc[dt.date(dt_stt.year + 1,1,1):dt.date(dt_rtr.year - 1,12,1),:].iterrows():
        df_mth_sav_rev.loc[idx,'REV_SAL'] = df_mth_sav_rev.shift(12).loc[idx,'REV_SAL'] * (1 + np.random.choice(gr_sal,1,replace = False)[0])
        df_mth_sav_rev.loc[idx,'REV_SSI'] = 0
        df_mth_sav_rev.loc[idx,'REV_GIF'] = rev_gif if idx.month in (2,12) else 0
        df_mth_sav_rev.loc[idx,'REV_OTH'] = df_mth_sav_rev.shift(12).loc[idx,'REV_OTH']
        df_mth_sav_rev.loc[idx,'REV_BRK'] = -inv_brk.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_IRA'] = -inv_ira.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_FOK'] = -inv_fok.loc[idx,'WD'] * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_TOT'] = df_mth_sav_rev.loc[idx,:].sum()

    # Timeline - Retire ---> Retire + 1Yr
    for idx, row in df_mth_sav_rev.loc[dt_rtr:dt.date(dt_rtr.year,12,1),:].iterrows():
        df_mth_sav_rev.loc[idx,'REV_SAL'] = 0
        df_mth_sav_rev.loc[idx,'REV_SSI'] = 0
        df_mth_sav_rev.loc[idx,'REV_GIF'] = 0
        df_mth_sav_rev.loc[idx,'REV_OTH'] = df_mth_sav_rev.shift(12).loc[idx,'REV_OTH']
        df_mth_sav_rev.loc[idx,'REV_BRK'] = -inv_brk.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_IRA'] = -inv_ira.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_FOK'] = -inv_fok.loc[idx,'WD'] * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_TOT'] = df_mth_sav_rev.loc[idx,:].sum()
        
    # Timeline - Retire + 1Yr ---> Social Security Eligibility
    for idx, row in df_mth_sav_rev.loc[dt.date(dt_rtr.year + 1,1,1):dt.date(dt_ssi.year - 1,12,1),:].iterrows():
        df_mth_sav_rev.loc[idx,'REV_SAL'] = 0
        df_mth_sav_rev.loc[idx,'REV_SSI'] = 0
        df_mth_sav_rev.loc[idx,'REV_GIF'] = 0
        df_mth_sav_rev.loc[idx,'REV_OTH'] = df_mth_sav_rev.shift(12).loc[idx,'REV_OTH']
        df_mth_sav_rev.loc[idx,'REV_BRK'] = -inv_brk.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_IRA'] = -inv_ira.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_FOK'] = -inv_fok.loc[idx,'WD'] * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_TOT'] = df_mth_sav_rev.loc[idx,:].sum()
        
    # Timeline - Social Security Eligibility ---> Social Security Eligibility + 1Yr
    for idx, row in df_mth_sav_rev.loc[dt_ssi:dt.date(dt_ssi.year,12,1),:].iterrows():
        df_mth_sav_rev.loc[idx,'REV_SAL'] = 0
        df_mth_sav_rev.loc[idx,'REV_SSI'] = rev_ssi
        df_mth_sav_rev.loc[idx,'REV_GIF'] = 0
        df_mth_sav_rev.loc[idx,'REV_OTH'] = df_mth_sav_rev.shift(12).loc[idx,'REV_OTH']
        df_mth_sav_rev.loc[idx,'REV_BRK'] = -inv_brk.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_IRA'] = -inv_ira.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_FOK'] = -inv_fok.loc[idx,'WD'] * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_TOT'] = df_mth_sav_rev.loc[idx,:].sum()

    # Timeline - Social Security Eligibility + 1Yr ---> End
    for idx, row in df_mth_sav_rev.loc[dt.date(dt_ssi.year + 1,1,1):,:].iterrows():
        df_mth_sav_rev.loc[idx,'REV_SAL'] = 0
        df_mth_sav_rev.loc[idx,'REV_SSI'] = df_mth_sav_rev.shift(12).loc[idx,'REV_SSI'] * (1 + np.random.choice(gr_ssi,1,replace = False)[0])
        df_mth_sav_rev.loc[idx,'REV_GIF'] = 0
        df_mth_sav_rev.loc[idx,'REV_OTH'] = df_mth_sav_rev.shift(12).loc[idx,'REV_OTH']
        df_mth_sav_rev.loc[idx,'REV_BRK'] = -inv_brk.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_IRA'] = -inv_ira.loc[idx,'WD']
        df_mth_sav_rev.loc[idx,'REV_FOK'] = -inv_fok.loc[idx,'WD'] * (1 - rt_tax_sal)
        df_mth_sav_rev.loc[idx,'REV_TOT'] = df_mth_sav_rev.loc[idx,:].sum()
        
    return df_mth_sav_rev
