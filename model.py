import altair as alt
import numpy as np
import pandas as pd
import streamlit as st


# theme 1
ExternalRiskEstimate = st.slider('External Risk Estimate', min_value=0, max_value=100, value=50)
MSinceOldestTradeOpen = st.slider('Months Since Oldest Trade Open', min_value=0, max_value=600, value=100)
AverageMInFile = st.slider('Average Months In File', min_value=0, max_value=360, value=60)
pred_creditHistory=  1 / (1 + np.exp(-(8.2710  - 0.1033*ExternalRiskEstimate - 0.0014*MSinceOldestTradeOpen - 0.0060*AverageMInFile)))

# theme 2
MSinceMostRecentTradeOpen = st.slider('Months Since Most Recent Trade Open', min_value=0, max_value=100, value=10)
NumTradesOpeninLast12M = st.slider('Number of Trades Open in Last 12 Months', min_value=0, max_value=20, value=5)
NumInqLast6M = st.slider('Number of Inquiries Last 6 Months', min_value=0, max_value=10, value=2)
NumInqLast6Mexcl7days = st.slider('Number of Inquiries Last 6 Months excluding last 7 days', min_value=0, max_value=10, value=2)
pred_creditFrequency = 1 / (1 + np.exp(-(-0.2177  - 0.0019*MSinceMostRecentTradeOpen + 0.0366*NumTradesOpeninLast12M + 0.3950*NumInqLast6M - 0.2311*NumInqLast6Mexcl7days)))

# theme 3
NumTrades60Ever2DerogPubRec = st.slider('Number of Trades 60+ Ever Derogatory/Public Records', min_value=0, max_value=10, value=1)
NumTrades90Ever2DerogPubRec = st.slider('Number of Trades 90+ Ever Derogatory/Public Records', min_value=0, max_value=10, value=1)
MSinceMostRecentDelq = st.slider('Months Since Most Recent Delinquency', min_value=0, max_value=120, value=30)

MaxDelq2PublicRecLast12M = st.slider('Max Delinquency in Public Records Last 12 Months', min_value=0, max_value=9, value=0, step=1)
for i in range(10):
    # Create variable dynamically and set to 0
    exec(f'MaxDelq2PublicRecLast12M_{i} = 0')
exec(f'MaxDelq2PublicRecLast12M_{MaxDelq2PublicRecLast12M} = 1')

MaxDelqEver = st.slider('Max Delinquency Ever', min_value=1, max_value=9, value=1, step=1)
for i in range(10):
    # Create variable dynamically and set to 0
    exec(f'MaxDelqEver_{i} = 0')
exec(f'MaxDelqEver_{MaxDelqEver} = 1')

pred_negActivity =(0.2638  + 0.1593*NumTrades60Ever2DerogPubRec + 0.0276*NumTrades90Ever2DerogPubRec - 0.0109*MSinceMostRecentDelq +
                   0.0883*MaxDelq2PublicRecLast12M_0 - 0.1328*MaxDelq2PublicRecLast12M_1 + 0.1346*MaxDelq2PublicRecLast12M_2 
                   - 0.1480*MaxDelq2PublicRecLast12M_3 + 0.4049*MaxDelq2PublicRecLast12M_4 + 0.8471*MaxDelq2PublicRecLast12M_5 
                   - 0.1824*MaxDelq2PublicRecLast12M_6 - 0.7832*MaxDelq2PublicRecLast12M_7 + 0.0000*MaxDelq2PublicRecLast12M_8 
                   - 0.0279*MaxDelq2PublicRecLast12M_9 
                   + 0.0000*MaxDelqEver_1 + 0.3853*MaxDelqEver_2 + 0.1126*MaxDelqEver_3 
                   + 0.1996*MaxDelqEver_4 + 0.3377*MaxDelqEver_5 + 0.3033*MaxDelqEver_6 
                   - 1.0809*MaxDelqEver_7 - 0.0569*MaxDelqEver_8 + 0.0000*MaxDelqEver_9)
pred_negActivity = 1 / (1 + np.exp(-pred_negActivity))

# theme 4
NetFractionRevolvingBurden = st.slider('Net Fraction Revolving Burden', min_value=0, max_value=200, value=50)
NetFractionInstallBurden = st.slider('Net Fraction Installment Burden', min_value=0, max_value=200, value=50)
NumRevolvingTradesWBalance = st.slider('Number of Revolving Trades with Balance', min_value=0, max_value=20, value=5)
NumInstallTradesWBalance = st.slider('Number of Installment Trades with Balance', min_value=0, max_value=20, value=5)
NumBank2NatlTradesWHighUtilization = st.slider('Number of Bank/National Trades with High Utilization', min_value=0, max_value=10, value=2)
PercentTradesWBalance = st.slider('Percent of Trades with Balance', min_value=0, max_value=100, value=50)

usage= (-1.4799 + 0.0240 * NetFractionRevolvingBurden + 0.0024 * NetFractionInstallBurden + 0.0087 * NumRevolvingTradesWBalance \
       - 0.0175 * NumInstallTradesWBalance - 0.0974 * NumBank2NatlTradesWHighUtilization + 0.0108 * PercentTradesWBalance) 
usage = 1 / (1 + np.exp(-usage))

# theme 5
NumSatisfactoryTrades = st.slider('Number of Satisfactory Trades', min_value=0, max_value=50, value=20)
NumTotalTrades = st.slider('Total Number of Trades', min_value=0, max_value=50, value=20)
PercentTradesNeverDelq = st.slider('Percent of Trades Never Delinquent', min_value=0, max_value=50, value=20)
PercentInstallTrades = st.slider('Percent of Istanllment Trades', min_value=0, max_value=50, value=20)
stability=(4.7294 - 0.0119 * NumSatisfactoryTrades - 0.0008 * NumTotalTrades - 0.0519 * PercentTradesNeverDelq + 0.0131 * PercentInstallTrades)
stability = 1 / (1 + np.exp(-stability))


# final prediction
final_prediction = -4.6816 + pred_creditHistory* 3.1742 \
    + pred_creditFrequency * 2.1591 \
    + pred_negActivity * 0.3973 \
    + usage * 1.6336 \
    + stability * 1.8478
final_prediction = 1 / (1 + np.exp(-final_prediction))

