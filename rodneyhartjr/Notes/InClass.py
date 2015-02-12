# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 19:51:20 2015

@author: rodneyhartjr
"""

from __future__ import division

import pandas
import sqlite3

import statsmodels.formula.api as smf

conn = sqlite3.connect('/Users/admin/documents/SQLite/lahman2013.sqlite')

sql = """select yearID, sum(R) as total_runs, sum(H) as total_hits, sum(SB) as stolen_bases, sum(SO) as strikeouts, sum(IBB) as total_intentional_walks
from Batting 
where yearID > 1954
and yearid < 2005
group by yearID
order by yearID ASC"""

df = pandas.read_sql(sql, conn)
conn.close()

df.dropna(inplace = True)

est = smf.ols(formula='total_runs ~ total_hits', data=df).fit()

print est.summary()

print est.rsquared

df['yhat'] = est.predict(df)

plt = df.plot(x='total_hits', y='total_runs', kind ='scatter')
plt.plot(df.total_hits, df.yhat, color='blue', linewidth=3)

df['residuals'] = df.total_runs - df.yhat

plt = df.plot(x='total_runs', y='residuals', kind='scatter')

RMSE = (((df.residuals) ** 2).mean() ** (1/2))

percent_avg_dev = RMSE / df.total_runs.mean()

print 'average deviation: {0}%'.format(round(percent_avg_dev*100, 1))


plt = df.plot(x='stolen_bases', y='total_runs', kind='scatter')

sb_est = smf.ols(formula='total_runs ~ stolen_bases', data=df).fit()
print sb_est.summary()

print sb_est.rsquared

df['sb_yhat'] = sb_est.predict(df)

plt = df.plot(x='stolen_bases', y='total_runs', kind='scatter')
plt.plot(df.stolen_bases, df.sb_yhat, color='blue', linewidth=3)

df['sb_residuals'] = df.total_runs - df.sb_yhat

plt = df.plot(x='total_runs', y='sb_residuals', kind='scatter')

RMSE_sb = (((df.residuals) ** 2).mean() ** (1/2))

print RMSE_sb
print RMSE

sn_percent_avg_dev = RMSE_sb / df.total_runs.mean()

print 'average deviation: {0}%'.format(round(sb_percent_avg_dev*100, 1))

df['post_1995'] = 0
df.post_1995[df.yearID>1995] = 1

df['from_1985_to_1995'] = 0
df.from_1985_to_1995[(df.yearID>1985) & (df.yearID<=1995)] = 1

bin_est = smf.ols(formula='total_runs ~ from_1985_to_1995 + post_1995', data=df).fit()
print bin_est.summary

df['binary_yhat'] = bin_est.predict(df)
plt = df.plot(x='yearID', y='total_runs', kind='scatter')
plt.plot(df.yearID, df.binary_yhat, color='blue', linewidth=3)

large_est = smf.ols(formula='total_runs ~ total_hits + stolen_bases + from_1985_to_1995 + post_1995', data=df).fit()
print large_est.summary()

large_rsquared = large_est.rsquared
print large_rsquared
print est.rsquared

df['large_yhat'] = large_est.predict(df)
df['large_residuals'] = df.total_runs - df.large_yhat

RMSE_large = (((df.large_residuals) ** 2).mean() ** (1/2))

print 'average deviation for large qeuation: {0}'.format(round(RMSE_large,4))

print 'average deviation for just hits: {0}'.format(round(RMSE, 4))

plt = df.plot(x='yearID', y='total_runs', kind='scatter')
plt.plot(df.yearID, df.yhat, color='blue', linewidth=3)
plt.plot(df.yearID, df.large_yhat, color='red', linewidth=3)

conn = sqlite3.connect('/Users/admin/documents/SQLite/lahman2013.sqlite')

sql = """select yearID, sum(R) as total_runs, sum(H) as total_hits, sum(SB) as stolen_bases, sum(SO) as strikeouts, sum(IBB) as total_intentional_walks
from Batting 
Where
yearid >= 2005
group by yearID
order by yearID ASC"""

df_post_2005 = pandas.read_sql(sql, conn)
conn.close()

df_post_2005['post_1995'] = 1
df_post_2005['from_1985_to_1995'] = 0

df_post_2005['yhat'] = est.predict(df_post_2005)
df_post_2005['large_yhat'] = large_est.predict(df_post_2005)

df_post_2005['hits_residuals'] = df_post_2005.total_runs - df_post_2005.yhat
df_post_2005['large_residuals'] = df_post_2005.total_runs - df_post_2005.large_yhat

RMSE_large = (((df_post_2005.large_residuals) ** 2).mean() ** (1/2))
RMSE_hits = (((df_post_2005.hits_residuals) ** 2).mean() ** (1/2))

print 'average deviation for large qeuation: {0}'.format(round(RMSE_large,4))

print 'average deviation for just hits: {0}'.format(round(RMSE_hits, 4))

plt = df_post_2005.plot(x='yearID', y='total_runs', kind='scatter')
plt.plot(df_post_2005.yearID, df_post_2005.yhat, color='blue', linewidth=3)
plt.plot(df_post_2005.yearID, df_post_2005.large_yhat, color='red', linewidth=3)
