'''
Questions
- What are the correlations of the variables? (correlation matrix/ pairsplot)
- What are the mean prices for different groups of offers?
-
'''


# import packages
import pandas as pd
import re
import seaborn
import datetime
import copy

# read data
df_cars = pd.read_hdf('data/cars_cleaned.h5', mode='r')
df_cars.head()
# create numeric feature with ange
df_cars['age_in_days'] = df_cars.build.apply(
    lambda x: (datetime.datetime.today() - x).days)


df_for_pairsplot = df_cars.loc[:, ['price',
                                   'horsepower',
                                   'kilometers',
                                   'age_in_days',
                                   'body_shape']]
body_shapes = df_cars.body_shape.unique()

fig_pairs = seaborn.pairplot(df_for_pairsplot, hue='body_shape',
                             hue_order=body_shapes,
                             vars=df_for_pairsplot.drop(
                                 ['body_shape'], axis=1).columns.values,
                             plot_kws={'alpha': .3},
                             diag_kind='reg')
