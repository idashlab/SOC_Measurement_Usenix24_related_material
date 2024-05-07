from statsmodels.regression.linear_model import OLS
from statsmodels.stats.diagnostic import acorr_ljungbox
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json 
import os

# step 1: setup valid input and output; setup global variables
########################################

CONN_INPUT_FILE = f''
RESULTS_FOLDER = f'.'

#########################################
if not os.path.exists(RESULTS_FOLDER):
    os.makedirs(RESULTS_FOLDER)

df = df_cur = pd.read_csv(CONN_INPUT_FILE, header=0, sep='\t', dtype='object')
df = df[['ts','id.orig_h']]

result_list = []
valid_seq_count = 0
total_count = 0

df_summary = pd.DataFrame(columns=['id.orig_h', 'pvalue'])

# step2: generate time interval sequence and calculate p-values.
def acorr_ljungbox_test(seq):
    ols_res = OLS(seq, np.ones(len(seq))).fit()
    return acorr_ljungbox(ols_res.resid, lags=1)['lb_pvalue'].tolist()[0]

df = df.sort_values(['ts']).groupby('id.orig_h')['ts'].apply(list).reset_index(name='ts_seq')
def ts_to_interval_helper(ts_seq):
    rt_list = [0]
    for i in range(1,len(ts_seq)):
        rt_list.append(float(ts_seq[i]) - float(ts_seq[0]))
    return rt_list
df['interval_seq'] = df['ts_seq'].apply(ts_to_interval_helper)

print(f'df interval_seq built finished')

def select_src_basedon_seqlen(interval_seq):
    if len(interval_seq) >= 5:
        return 1
    return 0

df['enough_interval'] = df['interval_seq'].apply(select_src_basedon_seqlen)
total_count += df.shape[0]
valid_seq_count += df['enough_interval'].sum()
df = df[df['enough_interval']==1].reset_index()
df['pvalue'] = df['interval_seq'].apply(acorr_ljungbox_test)
result_list = result_list + df['pvalue'].tolist()

df_needed = df[['id.orig_h', 'pvalue']]
df_summary=  pd.concat([df_summary, df_needed], axis=0)

print(f'Valid IPs have enough datapoints:{valid_seq_count}, total # of IPs : {total_count}.')
print(f'Ratio of valid IPs: {valid_seq_count/total_count}')
with open(f'{RESULTS_FOLDER}/tmp_qvalue_save.json', 'w') as f:
    json.dump(result_list, f)
pvalue_result_list = result_list
print(f'Record mid result for p-value.')


# step3: line plot for distributions (y:number of ips, x:p_value), suggested thresholds: 0.05, 0.6, 1
def plot_line_chart(datapoints, labels, save_path, xylabel=['P_value', 'CDF # of IPs'], bins=100):
    count, bins_count = np.histogram(datapoints, bins)
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    cdf = np.insert(cdf,0,0)
    plt.figure(figsize=(15,10))
    plt.subplots_adjust(bottom=0.19)
    ax = plt.gca()
    ax.set_xlim([-0.02, 1.02])
    ax.set_ylabel(f'{xylabel[1]}', fontsize=42)
    ax.set_xlabel(f'{xylabel[0]}', fontsize=42)
    plt.xticks(fontsize=30)
    plt.yticks(fontsize=30)
    color_list = ['green', 'blue']
    
    ax.plot(bins_count, cdf, color=color_list[0], label=labels[0], linewidth=6)
    ax.set_xticks(np.arange(0,1,0.05), minor=True)
    ax.set_yticks(np.arange(0,1,0.1), minor=True)
    ax.grid('both')
    ax.grid(which='major', alpha=0.6)
    ax.grid(which='minor', alpha=0.25)
    plt.savefig(f'{save_path}', dpi = 200)
    plt.clf()


plot_save_folder = RESULTS_FOLDER
plot_line_chart(pvalue_result_list, ['p-values for manual vs. bot'], f'{plot_save_folder}/hypothesis_test_pvalue_cdf.pdf', bins=100)