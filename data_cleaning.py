'''
What needs to be done?
- merge data frame from old data sets
- remove duplicates (id)
- feature generation
    - build: age of car in years and as timestamp
    - headline in bag of words (only for ml approaches not for vizualizations)
    - owners: define NAs (e.g. "-")
'''

#import packages
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np

#drop na rows

#read all the files and merge them and remove duplicates first
df_cars = pd.read_hdf('data/cars_2018-11-12_test.h5', mode='r')
df_cars = df_cars.dropna(subset=['state_str', 'features_str'])

#split feature string in list
df_cars['features_str'] = df_cars.features_str.apply(lambda x: x.split('\n\n'))
df_cars['state_str'] = df_cars.state_str.apply(lambda x: x.split('\n\n'))



def extract_colour(list):
    try:
        return list[list.index('Außenfarbe')+1]
    except ValueError:
        return None

def extract_body_shape(list):
    try:
        return list[list.index('Karosserieform')+1]
    except ValueError:
        return None

def extract_interior(list):
    try:
        return list[list.index('Innenausstattung')+1]
    except ValueError:
        return None

def extract_painting(list):
    try:
        return list[list.index('Lackierung')+1]
    except ValueError:
        return None

def extract_HU(list):
    try:
        return list[list.index('HU Prüfung')+1]
    except ValueError:
        return None

def extract_checkbook(list):
    try:
        return list[list.index('Scheckheftgepflegt')+1]
    except ValueError:
        return None

df_cars['colour'] = df_cars.features_str.apply(extract_colour)
df_cars['body_shape'] = df_cars.features_str.apply(extract_body_shape)
df_cars['interior'] = df_cars.features_str.apply(extract_interior)
df_cars['painting'] = df_cars.features_str.apply(extract_painting)
df_cars['HU'] = df_cars.state_str.apply(extract_HU)
df_cars['checkbook'] = df_cars.state_str.apply(extract_checkbook)

df_cars.head(3)

################################################################################
#now we walk through all the columns, check the unique values check necessary
#cleaning steps
################################################################################

### build
df_cars.build.unique()
#create time Timestamp
def timestamp_from_string(str):
    try:
        return pd.Timestamp(str)
    except ValueError:
        return None

df_cars['build'] = df_cars.build.apply(timestamp_from_string)

###gear
df_cars.gear.unique()
df_cars.loc[df_cars.gear == '-/- (Getriebeart)','gear'] = None

###headline
#we leave this for now --> maybe tfidf later!

###horsepower
df_cars.horsepower.unique()#looks fine to me

###id
#is the number of unique id equal to the number of rows?
len(df_cars) == len(df_cars.id.unique())


###kilometers
data = [go.Histogram(x=df_cars.price)]
py.iplot(data, filename='basic histogram') ###looks good like its measured in k
