### IMPORTS

import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt


### FUNCTIONS

# Plot balances for all simulations over forecast horizon
def plot_bal(simdict, dt_rng, dt_end, sims,
             fig_wd = 15, fig_ht = 10,
             pct_hi = 90, pct_lo = 10):
    
    # Set up main plot and positive balance counter
    ctr_pos_bal = dict({'Pos':0, 'Neg':0})
    fig, ax = plt.subplots(1,1, figsize = (fig_wd, fig_ht))
    
    # Ending balance list
    eb_list = [simdict[sim].loc[dt_end,'EB'] for sim in range(sims)]
    idx_med = eb_list.index(np.median(eb_list))
    idx_pct_hi = eb_list.index(np.percentile(eb_list, pct_hi))
    idx_pct_lo = eb_list.index(np.percentile(eb_list, pct_lo))

    # Plot horizontal line at 0
    plt.axhline(y = 0, color='black', linestyle='--')
    
    # Plot individual balance curves
    for sim in simdict.keys():
        
        if sim == idx_med:
            ax.plot(simdict[sim]['EB'], color = 'green', linewidth = 3)
        elif sim == idx_pct_hi:
            ax.plot(simdict[sim]['EB'], color = 'blue', linewidth = 3)
        elif sim == idx_pct_lo:
            ax.plot(simdict[sim]['EB'], color = 'red', linewidth = 3)
        else:
            ax.plot(simdict[sim]['EB'], linewidth = 0.5)
        
        # Count balance curves with negative balances at any point
        if (simdict[sim]['EB'] > 0).mean() == 1:
            ctr_pos_bal['Pos'] = ctr_pos_bal['Pos'] + 1
        else:
            ctr_pos_bal['Neg'] = ctr_pos_bal['Neg'] + 1
    
    # Annotation - Positive Balances and Percentage of Total Sims
    ax.annotate('Pos Bals: {}'.format(ctr_pos_bal['Pos']), xy=(100, 50), xycoords='figure pixels')
    ax.annotate('Neg Bals: {}'.format(ctr_pos_bal['Neg']), xy=(100, 60), xycoords='figure pixels')
    ax.annotate('% Pos: {}'.format(ctr_pos_bal['Pos'] / sum(ctr_pos_bal.values()),'.2%'), xy=(100, 70), xycoords='figure pixels')
    
    ax.set_xlim([dt_rng[0], dt_rng[-1]])
    
    return None

# Plot return distribution at each month over forecast horizon
def plot_retpct(inv_brk, inv_ira, inv_fok,
                flag_pd = 'Annual',
                fig_wd = 15, fig_ht = 10):
    
    dct_tot_ret = {}
    df_totret = pd.DataFrame()
    
    fig, ax = plt.subplots(1,1, figsize = (fig_wd, fig_ht))
    
    for dct in inv_brk.keys():

        dct_tot_ret[dct] = inv_brk[dct] + inv_ira[dct] + inv_fok[dct]

        if flag_pd == 'Annual':
            dct_tot_ret[dct] = dct_tot_ret[dct].groupby(dct_tot_ret[dct].index.year).agg(
                {'BB': 'mean', 'ADD': 'sum', 'WD': 'sum',
                 'RTN': 'sum', 'EB': 'last'})

        dct_tot_ret[dct]['RTN_PCT'] = dct_tot_ret[dct]['RTN'] / dct_tot_ret[dct]['EB']
        df_totret[dct] = dct_tot_ret[dct]['RTN'] / dct_tot_ret[dct]['EB']
    
    ax.boxplot(df_totret.T)
    ax.set_xticklabels(df_totret.index)
    
    return dct_tot_ret

# Plot distirbution of giving as a percent of total expenses for each year over the forecast horizon
def giv_dist(simdict_exp, sims, fig_wd = 15, fig_ht = 10):

    # Set up data structures and plots
    dist_pctgiv = pd.DataFrame()
    ctr = 0

    for fcst in simdict_exp:
        
        pctgiv_ann = simdict_exp[fcst].groupby(simdict_exp[fcst].index.year).sum().loc[:,'EXP_GIV']
        totexp_ann = simdict_exp[fcst].groupby(simdict_exp[fcst].index.year).sum().loc[:,'EXP_TOT']
        giv_ratio = pctgiv_ann / totexp_ann
        dist_pctgiv[ctr] = giv_ratio
                
        ctr+=1
    
    fig, ax = plt.subplots(1,1, figsize = (fig_wd, fig_ht))
    ax.boxplot(dist_pctgiv.T)
    ax.set_xticklabels(dist_pctgiv.index)

    return None

