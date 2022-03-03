'''
simplified_analysis.py
Rafael Guerra

This code compares two chemical databases and creates CSV files for their common items as well as which items exist only in each database.

'''

# Import Libraries
import pandas as pd
import numpy as np

# Load Data
sl = pd.read_csv('sl.csv')
cpisi = pd.read_csv('cpisi.csv')

# Remove NaN, Not Available, and others
sl['mutated_cas'] = sl['cas_number'].replace(
    ['0','Not Available','Propietary',np.nan,'NA'],'SL Only')

cpisi['mutated_cas'] = cpisi['cas_number'].replace(
    ['0','Not Available','Propietary',np.nan,'NA'],'CPSI Only')

# Create Common Items DF
common_items = pd.merge(sl,cpisi,left_on='mutated_cas',right_on='mutated_cas',suffixes=('_sl', '_cpisi'))
common_items = common_items[['ingredient_sl','ingredient_cpisi','mutated_cas']]
common_items.to_csv('common_items.csv',index=False)

# Create FL Only CSV
outer_join_sl = pd.merge(sl,common_items,on='mutated_cas',how='outer', indicator = True)
anti_join_sl = outer_join_sl[~(outer_join_sl._merge == 'both')].drop('_merge', axis = 1)
sl_only = anti_join_sl[['ingredient','cas_number']]
sl_only.to_csv('fl_only.csv',index=False)

# Create CPISI Only CSV
common_items_unique = common_items[['ingredient_cpisi','mutated_cas']]
common_items_unique = common_items_unique.drop_duplicates()
outer_join_cpisi = pd.merge(cpisi,common_items_unique,on='mutated_cas',how='outer', indicator = True)
anti_join_cpisi = outer_join_cpisi[~(outer_join_cpisi._merge == 'both')].drop('_merge', axis = 1)
cpisi_only = anti_join_cpisi[['ingredient','cas_number']]
cpisi_only.to_csv('cpisi_only.csv',index=False)