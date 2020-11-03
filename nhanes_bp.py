#code to analyze the data from 99-00 to 17-18 for blood preassure from NHANES considering age and gender.
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
#list of years.

def t_value(var):#function to extract t values between groups.
	var1 = var[0]
	var2 = var[1]
	media_v1 = var1.mean()
	media_v2 = var2.mean()
	std1 = var1.std()
	std2 = var2.std()
	n1 = len(var1)
	n2 = len(var2)
	t_dif = (media_v1 - media_v2 - 0)/(np.sqrt((((n1 - 1) * (std1**2)) + ((n2 - 1) * (std2**2)))/(n1 + n2 - 2)) * np.sqrt((1/n1) + (1/n2)))
	t_value.t_dif = round(t_dif, 2)

def bs(var):#Creation of summary table
	v = np.array(var)
	bs.mean_v = round(v.mean(), 2)
	bs.std_v = round(v.std(), 2)
	bs.n_v = len(v)

def bs_m(var):#Creation of summary table
	bs(var)
	name = 'Male' + str(((10*a) - 10)) + '-' + str(10*a)
	bs_m.df_table = pd.DataFrame({'Group':[name], 'Mean': [bs.mean_v], 'Std': [bs.std_v], 'n': [bs.n_v]},\
		index = pd.MultiIndex.from_tuples([(1, 'Systolic')], names =['ind', 'BP']))
	
def bd_m(var):#Creation of summary table
	bs(var)
	name = 'Male' + str(((10*a) - 10)) + '-' + str(10*a)
	bd_m.df_table = pd.DataFrame({'Group':[name], 'Mean': [bs.mean_v], 'Std': [bs.std_v], 'n': [bs.n_v]},\
		index = pd.MultiIndex.from_tuples([(1, 'Diastolic')], names =['ind', 'BP']))

def bs_f(var):#Creation of summary table
	bs(var)
	name = 'Female' + str(((10*a) - 10)) + '-' + str(10*a)
	bs_f.df_table = pd.DataFrame({'Group':[name], 'Mean': [bs.mean_v], 'Std': [bs.std_v], 'n': [bs.n_v]},\
		index = pd.MultiIndex.from_tuples([(1, 'Systolic')], names =['ind', 'BP']))

def bd_f(var):#Creation of summary table
	bs(var)
	name = 'Female' + str(((10*a) - 10)) + '-' + str(10*a)
	bd_f.df_table = pd.DataFrame({'Group':[name], 'Mean': [bs.mean_v], 'Std': [bs.std_v], 'n': [bs.n_v]},\
		index = pd.MultiIndex.from_tuples([(1, 'Diastolic')], names =['ind', 'BP']))

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

#Grouping data according to gender and age bands of 10 years.
main_list_sistolic_m = []
main_list_sistolic_f = []
main_list_diastolic_m = []
main_list_diastolic_f = []
for a in range(9):
	if a > 0:
		lif =[]
		for hf in range(8):
			yf = 0.02 + (0.0001 * hf)
			lif.append(yf)
		df_hm = df_hd.loc[(df_hd.RIAGENDRx == 'M') & (df_hd.RIDAGEYR >= ((10*a) - 10)) & (df_hd.RIDAGEYR < (10*a)),:]
		df_hf = df_hd.loc[(df_hd.RIAGENDRx == 'F') & (df_hd.RIDAGEYR >= ((10*a) - 10)) & (df_hd.RIDAGEYR < (10*a)),:]
		m_s = np.array(df_hm.BPXSYT) #array of data for male systolic blood preassure(bp)
		bs_m(m_s)#Creation of summary table
		medm_s = np.mean(df_hm.BPXSYT) #mean of male systolic bp
		m_d = np.array(df_hm.BPXDIT) #array of data for male diastolic bp
		bd_m(m_d)#Creation of summary table
		medm_d = np.mean(df_hm.BPXDIT) #mean of male diastolic bp
		f_s = np.array(df_hf.BPXSYT) #array of data for female systolic bp
		bs_f(f_s)#Creation of summary table
		medf_s = np.mean(df_hf.BPXSYT) #mean of female systolic bp
		f_d = np.array(df_hf.BPXDIT) #array of data for female diastolic bp
		bd_f(f_d)#Creation of summary table
		medf_d = np.mean(df_hf.BPXDIT) #mean of female diastolic bp
		llist_s = [m_s, f_s] # list of arrays of systolic bp for t-value between males and females
		llist_m = [m_s, m_d] #list of arrays of male bp for t-value between systolic and diastolic bp
		llist_d = [m_d, f_d] #list of arrays of diastolic bp for t-value between males and females
		llist_f = [f_s, f_d] #list of arrays of female bp for t-value between systolic and diastolic bp
		main_list_sistolic_m.append(m_s) #list of arrays of systolic bp for males over age bands
		main_list_sistolic_f.append(f_s) #list of arrays of systolic bp for females over age bands
		main_list_diastolic_m.append(m_d) #list of arrays of diastolic bp for males over age bands
		main_list_diastolic_f.append(f_d) #list of arrays of diastolic bp for females over age bands
		#plotting graphs on matplotlib and seaborn
		plt.subplot(9, 1, a)
		sns.distplot(m_s, color = '#061191', hist = False, kde_kws = {'shade' : True}, norm_hist = False)
		sns.distplot(f_s, color = '#800404', hist = False, kde_kws = {'shade' : True}, norm_hist = False)
		t_value(llist_s)
		plt.text(210, lif[8 - a], t_value.t_dif, fontsize = 10)
		t_value(llist_m)
		plt.text(190, lif[8 - a], t_value.t_dif, fontsize = 9, color = 'blue')
		t_value(llist_d)
		plt.text(-40, lif[8 - a], t_value.t_dif, fontsize = 10)
		t_value(llist_f)
		plt.text(-20, lif[8 - a], t_value.t_dif, fontsize = 9, color = 'red')
		plt.xlim(0, 80)
		plt.xticks([])
		plt.axvline(medm_s, ls = '--', lw = 1, color = '#061191')
		plt.axvline(medf_s, ls = '--', lw = 1, color = '#800404')
		plt.subplot(9, 1, a)
		sns.distplot(m_d, color = '#656edb', hist = False, kde_kws = {'shade' : True}, norm_hist = False)
		sns.distplot(f_d, color = '#db6060', hist = False, kde_kws = {'shade' : True}, norm_hist = False)
		plt.xlim(-50, 250)
		plt.ylim(0, 0.05)
		plt.xticks([])
		plt.axvline(medm_d, ls = '--', lw = 1, color = '#656edb')
		plt.axvline(medf_d, ls = '--', lw = 1, color = '#db6060')
		plt.axvline(0, lw = 2, color = 'white', zorder = 0)
		plt.axvline(200, lw = 2, color = 'white', zorder = 0)
		plt.axvline(50, lw = 1, color = 'white', zorder = 0)
		plt.axvline(150, lw = 1, color = 'white', zorder = 0)
		plt.axvline(100, lw = 0.5, color = 'white', zorder = 0)

	if a == 1:
		plt.title(('Blood Pressure across age bands and gender'), fontsize= 15)#plotting graphs on matplotlib and seaborn
		df_table_mg = pd.concat([bs_m.df_table, bd_m.df_table])#Creation of summary table
		df_table_fg = pd.concat([bs_f.df_table, bd_f.df_table])#Creation of summary table

	elif a == 2:
		df_table_mg1 = pd.concat([bs_m.df_table, bd_m.df_table])#Creation of summary table
		df_table_mtotal = pd.concat([df_table_mg, df_table_mg1])#Creation of summary table
		df_table_fg1 = pd.concat([bs_f.df_table, bd_f.df_table])#Creation of summary table
		df_table_ftotal = pd.concat([df_table_fg, df_table_fg1])#Creation of summary table
	elif a > 2:
		df_table_mg2 = pd.concat([bs_m.df_table, bd_m.df_table])#Creation of summary table
		df_table_mtotal = pd.concat([df_table_mtotal, df_table_mg2])#Creation of summary table
		df_table_fg2 = pd.concat([bs_f.df_table, bd_f.df_table])#Creation of summary table
		df_table_ftotal = pd.concat([df_table_ftotal, df_table_fg2])#Creation of summary table

			

	plt.xticks(ticks = [0, 50, 100, 150, 200], labels = [0, 50, 100, 150, 200])
	plt.yticks(ticks = [0, 0.01, 0.025, 0.04, 0.05], labels = ['',0.01, 0.025, 0.04,''])
	lio =[]
	for hh in range(8):
		yo = 0.02 + (0.06 * hh)
		lio.append(yo)
	
plt.text(230, 0.47, 'Age bands', fontsize = 15)
plt.text(207, 0.47, 't systolic', fontsize = 12)
plt.text(189, 0.47, 't male', fontsize = 12, color = 'blue')
plt.text(-22, 0.47, 't female', fontsize = 12, color = 'red')
plt.text(-45, 0.47, 't diastolic', fontsize = 12)
plt.text(230, lio[7], '[0 -10 years]')
plt.text(230, lio[6], '[10-20 years]')
plt.text(230, lio[5], '[20-30 years]')
plt.text(230, lio[4], '[30-40 years]')
plt.text(230, lio[3], '[40-50 years]')
plt.text(230, lio[2], '[50-60 years]')
plt.text(230, lio[1], '[60-70 years]')
plt.text(230, lio[0], '[70-80 years]')
plt.text(169, 0.47, 't Age', fontsize = 10, color = 'black')
plt.text(-1, 0.47, 't Age', fontsize = 10, color = 'black')
plt.xlabel('Blood Pressure(mmHg)')

df_table_t = pd.concat([df_table_mtotal, df_table_ftotal], axis = 1)#Creation of summary table
print(df_table_t)

for c in range(7):#plotting graphs on matplotlib and seaborn
	llist_ms = [main_list_sistolic_m[c+1], main_list_sistolic_m[c]]
	llist_md = [main_list_diastolic_m[c+1], main_list_diastolic_m[c]]
	llist_fs = [main_list_sistolic_f[c+1], main_list_sistolic_f[c]]
	llist_fd = [main_list_diastolic_f[c+1], main_list_diastolic_f[c]]
	t_value(llist_ms)
	plt.text(170, lio[6 - c]+ 0.005, t_value.t_dif, fontsize = 8, color = 'blue')
	t_value(llist_md)
	plt.text(0, lio[6 - c]+ 0.005, t_value.t_dif, fontsize = 8, color = 'blue')
	t_value(llist_fs)
	plt.text(170, lio[6 - c] - 0.005, t_value.t_dif, fontsize = 8, color = 'red')
	t_value(llist_fd)
	plt.text(0, lio[6 - c] - 0.005, t_value.t_dif, fontsize = 8, color = 'red')
plt.show()#plotting graphs on matplotlib and seaborn
