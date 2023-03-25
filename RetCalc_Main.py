### IMPORTS

# Timing Function
import time
startTime = time.time()

# Analysis
import pandas as pd
import numpy as np

# Custom Functions
import RetPlan_Exp
import RetPlan_Inv
import RetPlan_Rev
import RetPlan_Bal
import RetPlan_Viz


### DATA

# Descriptors
funds_rowdesc = ['BB','ADD','WD','RTN','EB']

# Paths
data_path = ''
data_file = ''
data_full = data_path + data_file

# Sheets
data_shts_inv = 'Investments'
data_shts_rev = 'Revenue'
data_shts_exp = 'Expense'
data_shts_oth = 'Other'

# Read in data
data_inv = pd.read_excel(data_full, sheet_name = data_shts_inv, index_col = 'Fund')
data_rev = pd.read_excel(data_full, sheet_name = data_shts_rev, index_col = 'Category')
data_exp = pd.read_excel(data_full, sheet_name = data_shts_exp, index_col = 'Category')
data_oth = pd.read_excel(data_full, sheet_name = data_shts_oth, index_col = 'Category')


### KEY DATES

# Events
dt_stt = data_oth.loc['Date_Start'][0]
dt_end = data_oth.loc['Date_End'][0]
dt_rtr = data_oth.loc['Date_Retire'][0]
dt_ssi = data_oth.loc['Date_SocSec'][0]

# Key Dates - Withdrawals
dt_wd_brk = data_inv.loc['BRK','Withdrawal_Dt']
dt_wd_ira = data_inv.loc['IRA','Withdrawal_Dt']
dt_wd_fok = data_inv.loc['FOK','Withdrawal_Dt']
dt_wd_res = data_inv.loc['RES','Withdrawal_Dt']

# Withdrawal Amounts
wd_brk = data_inv.loc['BRK', 'Withdrawal']
wd_ira = data_inv.loc['IRA', 'Withdrawal']
wd_fok = data_inv.loc['FOK', 'Withdrawal']

# Fund Beginning Balances
bb_brk = data_inv.loc['BRK','BB']
bb_ira = data_inv.loc['IRA','BB']
bb_fok = data_inv.loc['FOK','BB']
bb_res = data_inv.loc['RES','BB']
bb_sav = data_oth.loc['BB_Sav','Amount']

# Distributions - Investment Returns
srs_rtn_brk = np.random.normal(loc = data_inv.loc['BRK','Return'], scale = data_inv.loc['BRK','Rtn_SD'], size = data_oth.loc['Dist_Size','Amount'])
srs_rtn_ira = np.random.normal(loc = data_inv.loc['IRA','Return'], scale = data_inv.loc['IRA','Rtn_SD'], size = data_oth.loc['Dist_Size','Amount'])
srs_rtn_fok = np.random.normal(loc = data_inv.loc['FOK','Return'], scale = data_inv.loc['FOK','Rtn_SD'], size = data_oth.loc['Dist_Size','Amount'])
srs_rtn_res = np.random.normal(loc = data_inv.loc['RES','Return'], scale = data_inv.loc['RES','Rtn_SD'], size = data_oth.loc['Dist_Size','Amount'])

# Distributions - Salary Increases
srs_infl_sal = np.random.normal(loc = data_rev.loc['REV_SAL','Growth'], scale = data_rev.loc['REV_SAL','Growth_SD'], size = data_oth.loc['Dist_Size','Amount'])
srs_infl_ssi = np.random.normal(loc = data_rev.loc['REV_SSI','Growth'], scale = data_rev.loc['REV_SSI','Growth_SD'], size = data_oth.loc['Dist_Size','Amount'])

# Derived Parameters
dt_rng = pd.date_range(start = dt_stt, end = dt_end, freq = 'MS')

# Simulation Data Structures
sims = data_oth.loc['Sims','Amount']

simdict_exp = dict()
simdict_rev = dict()
simdict_inv_brk = dict()
simdict_inv_ira = dict()
simdict_inv_fok = dict()
simdict_bal = dict()


### RUN FORECAST

for sim in range(sims):
    
    # Expenses
    fcst_exp = RetPlan_Exp.gen_fcst_exp(data_exp, data_oth,
                                        dt_stt, dt_rtr, dt_rng)
    
    # Investments
    fcst_inv_brk = RetPlan_Inv.gen_inv_df(dt_rng, dt_stt, dt_wd_brk, dt_rtr,
                    funds_rowdesc, 
                    bb_brk, wd_brk, 
                    fcst_exp.loc[:,'EXP_BRK'],srs_rtn_brk, 
                    0, 0,
                    data_inv.loc['BRK','Decay'], data_exp.loc['EXP_BRK','Inflation'])
    
    fcst_inv_ira = RetPlan_Inv.gen_inv_df(dt_rng, dt_stt, dt_wd_ira, dt_rtr,
                    funds_rowdesc, 
                    bb_ira, wd_ira, 
                    fcst_exp.loc[:,'EXP_IRA'],srs_rtn_ira, 
                    0, 0,
                    data_inv.loc['IRA','Decay'], data_exp.loc['EXP_IRA','Inflation'])
    
    fok_match = data_rev.loc['REV_SAL','Amount'] * data_oth.loc['FOK_Match','Amount']
    fcst_inv_fok = RetPlan_Inv.gen_inv_df(dt_rng, dt_stt, dt_wd_fok, dt_rtr,
                    funds_rowdesc, 
                    bb_fok, wd_fok, 
                    fcst_exp.loc[:,'EXP_FOK'],srs_rtn_ira, 
                    fok_match, data_rev.loc['REV_SAL','Growth'],
                    data_inv.loc['IRA','Decay'], data_exp.loc['EXP_FOK','Inflation'])
    
    srs_exp_res = pd.Series(0, index = dt_rng)
    fcst_inv_res = RetPlan_Inv.gen_inv_df(dt_rng, dt_stt, dt_wd_res, dt_rtr,
                    funds_rowdesc, 
                    bb_res, 0, 
                    srs_exp_res, srs_rtn_res, 
                    0, 0,
                    data_inv.loc['RES','Decay'], 0)
    
    # Revenue    
    fcst_rev = RetPlan_Rev.gen_fcst_rev(dt_rng, dt_stt, dt_rtr, dt_ssi,
                     data_rev.index,
                     data_rev.loc['REV_SAL','Amount'], data_rev.loc['REV_GIF','Amount'],
                     data_rev.loc['REV_OTH','Amount'], data_rev.loc['REV_SSI','Amount'],
                     srs_infl_sal, srs_infl_ssi,
                     fcst_inv_brk, fcst_inv_ira, fcst_inv_fok,
                     data_oth.loc['Tax_Salary','Amount'])
    
    # Balances    
    fcst_bal = RetPlan_Bal.gen_fcst_bal(dt_rng, dt_stt,
                     funds_rowdesc,
                     data_oth,
                     fcst_rev, fcst_exp)
    
    # Store Data
    simdict_exp[sim] = fcst_exp
    simdict_rev[sim] = fcst_rev
    simdict_inv_brk[sim] = fcst_inv_brk
    simdict_inv_ira[sim] = fcst_inv_ira
    simdict_inv_fok[sim] = fcst_inv_fok
    simdict_bal[sim] = fcst_bal


### VISUALIZATIONS AND ANALYSIS

# Plot balances over time for all simulations
RetPlan_Viz.plot_bal(simdict_bal, dt_rng, dt_end, sims)

# Plot giving as a percent of total expenses
RetPlan_Viz.giv_dist(simdict_exp, sims)

# Plot return distribution at each month over forecast horizon
dct_totret = RetPlan_Viz.plot_retpct(simdict_inv_brk, simdict_inv_ira, simdict_inv_fok)

# Print calculator execution time
executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
