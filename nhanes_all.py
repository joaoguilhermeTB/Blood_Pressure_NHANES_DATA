#code to analyze the data from 99-00 to 17-18 for blood preassure from NHANES.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
pd.set_option('display.max_columns', 12, 'display.max_colwidth', 3, 'display.expand_frame_repr', False, 'display.max_rows', 200)

demo_list = ['DEMO_99_00.XPT', 'DEMO_B_01_02.XPT', 'DEMO_C_03_04.XPT', 'DEMO_D_05_06.XPT', 'DEMO_E_07_08.XPT',\
 'DEMO_F_09_10.XPT', 'DEMO_G_11_12.XPT', 'DEMO_H_13_14.XPT', 'DEMO_I_15_16.XPT', 'DEMO_J_17_18.XPT'] #list of demographic XPT files data
bpx_list = ['BPX_99_00.XPT', 'BPX_B_01_02.XPT', 'BPX_C_03_04.XPT', 'BPX_D_05_06.XPT', 'BPX_E_07_08.XPT','BPX_F_09_10.XPT',\
 'BPX_G_11_12.XPT', 'BPX_H_13_14.XPT', 'BPX_I_15_16.XPT', 'BPX_J_17_18.XPT'] #list of cardiovascular XPT files data
year = ['1999-2000', '2001-2002', '2003-2004', '2005-2006', '2007-2008', '2009-2010','2011-2012', '2013-2014', '2015-2016', '2017-2018']

for tt in range(len(demo_list)):#Loop to read data files across nhanes years
	df_d = pd.read_sas(demo_list[tt])#demographic data 
	df_bpx = pd.read_sas(bpx_list[tt])#Cardiovascular data

	#SEQN column represents the respondent sequence number, RIAGENDR column reprensents the gender of respondents and RIDAGEYR represents
	#the age of respondents.
	#BPXSY and BPXDI represents the systolic and diastolic blood preassure respectively. 1, 2 or 3 represents the sequence of the measures
	df_d = df_d.loc[:,('SEQN','RIAGENDR', 'RIDAGEYR')]
	df_bpx = df_bpx.loc[:,('SEQN', 'BPXSY1', 'BPXSY2', 'BPXSY3', 'BPXDI1', 'BPXDI2', 'BPXDI3')]
	df_bpx['BPXSYT'] = round(((df_bpx.BPXSY1 + df_bpx.BPXSY2 + df_bpx.BPXSY3)/3), 1)#Mean value of the systolic blood preassure measures
	df_bpx['BPXDIT'] = round(((df_bpx.BPXDI1 + df_bpx.BPXDI2 + df_bpx.BPXDI3)/3), 1)#Mean value of the diastolic blood preassure measures
	df_bpx = df_bpx.loc[:, ('SEQN','BPXSYT', 'BPXDIT')]
	df_bpx = df_bpx.dropna()
	df_d['RIAGENDRx'] = df_d.RIAGENDR.replace({1: 'M', 2: 'F'})
	#Joining data from the dataframe with demographic and cardiovascular data, based on the SEQN column.
	df_h = pd.merge(df_bpx, df_d, how = 'left') 
	df_h = df_h.dropna()
	df_h['Year'] = year[tt]

	#Joining data from different nhanes years in on single dataframe
	if tt == 0:
		df_hd = df_h
	else:
		df_hd = pd.concat([df_hd, df_h])

#All the data with no age or gender filter.
sys_t = np.array(df_hd.BPXSYT)
dia_t = np.array(df_hd.BPXDIT)
sys_mean = np.mean(sys_t)
dia_mean = np.mean(dia_t)
sys_median = np.median(sys_t)
dia_median = np.median(dia_t)
sys_std = np.std(sys_t)
dia_std = np.std(dia_t)

#Plotting graph
sns.distplot(sys_t, color = '#000000')
sns.distplot(dia_t, color = '#545328')
plt.axvline(sys_mean, ls = '-', lw = 1, color = '#000000')
plt.axvline(dia_mean, ls = '-', lw = 1, color = '#545328')
plt.axvline(sys_median, ls = '--', lw = 1, color = '#000000')
plt.axvline(dia_median, ls = '--', lw = 1, color = '#545328')
plt.xlabel('Blood Pressure(mmHg)')
plt.ylabel('Frequency')
plt.title(('Diastolic and Systolic Blood Pressure'), fontsize= 15)
plt.text(175, 0.027, 'Systolic BP')
plt.text(175, 0.025, ('Mean:' + str(round(sys_mean, 2))))
plt.text(175, 0.023, ('Median:' + str(sys_median)))
plt.text(10, 0.027, 'Diastolic BP', color = '#545328')
plt.text(10, 0.025, ('Mean:' + str(round(dia_mean, 2))), color = '#545328')
plt.text(10, 0.023, ('Median:'+ str(dia_median)), color = '#545328')
plt.text(175, 0.021, ('Std:' + str(round(sys_std, 2))))
plt.text(10, 0.021, ('Std:'+ str(round(dia_std, 2))), color = '#545328')


var1 = sys_t
var2 = dia_t
media_v1 = var1.mean()
media_v2 = var2.mean()
std1 = var1.std()
std2 = var2.std()
n1 = len(var1)
n2 = len(var2)
t_dif = (media_v1 - media_v2 - 0)/(np.sqrt((((n1 - 1) * (std1**2)) + ((n2 - 1) * (std2**2)))/(n1 + n2 - 2)) * np.sqrt((1/n1) + (1/n2)))
t_dif = round(t_dif, 2)
plt.text(190, 0.03, ('t =' + str(t_dif)), fontsize = 15)

plt.show()
