'''
What needs to be done?
- merge data frame from old data sets
- remove duplicates (id)
- remove features with to little non null values
- remove rows with missing values for key features
- drop unnecessary columns
'''

#import packages
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
import re
import glob


###read data
'''
We read all the files in the directory, that where created by the webscraping
script. We only want unique ids in the data frame. So we discard the old entries
when ids appier in more than one of the data files.
'''
allFiles = glob.glob("data/*[0-9].h5")
allFiles.sort()
allFiles
df_cars = pd.read_hdf(allFiles[-1])
for i in reversed(allFiles[:-1]):
    df_con = pd.read_hdf(i)
    new_ids = list(set(df_con.id.unique().tolist())-set(df_cars.id.unique().tolist()))
    df_cars = pd.concat([df_cars, df_con[df_con.id.isin(new_ids)]])

#df_cars.info()
df_cars = df_cars.dropna(subset=['state_str', 'features_str'])


#split feature string in list
df_cars['features_str'] = df_cars.features_str.apply(lambda x: x.split('\n\n'))
df_cars['state_str'] = df_cars.state_str.apply(lambda x: x.split('\n\n'))

#extract infos from features stings
def extract_colour(list):
    try:
        return list[list.index('Außenfarbe')+1]
    except ValueError:
        return 'unknown'

def extract_body_shape(list):
    try:
        return list[list.index('Karosserieform')+1]
    except ValueError:
        return 'unknown'

def extract_interior(list):
    try:
        return list[list.index('Innenausstattung')+1]
    except ValueError:
        return 'unknown'

def extract_painting(list):
    try:
        return list[list.index('Lackierung')+1]
    except ValueError:
        return 'unknown'

def extract_HU(list):
    try:
        return list[list.index('HU Prüfung')+1]
    except ValueError:
        return 'unknown'

def extract_checkbook(list):
    try:
        return list[list.index('Scheckheftgepflegt')+1]
    except ValueError:
        return 'unknown'

df_cars['colour'] = df_cars.features_str.apply(extract_colour)
df_cars['body_shape'] = df_cars.features_str.apply(extract_body_shape)
df_cars['interior'] = df_cars.features_str.apply(extract_interior)
df_cars['painting'] = df_cars.features_str.apply(extract_painting)
df_cars['HU'] = df_cars.state_str.apply(extract_HU)
df_cars['checkbook'] = df_cars.state_str.apply(extract_checkbook)

#df_cars.head(3)

################################################################################
#now we walk through all the columns, check the unique values check necessary
#cleaning steps
################################################################################

### build
#create time Timestamp
def timestamp_from_string(str):
    try:
        return pd.Timestamp(str)
    except ValueError:
        return None

df_cars['build'] = df_cars.build.apply(timestamp_from_string)
df_cars.build.notnull().sum()
df_cars = df_cars[df_cars.build.notnull()]

###gear
#df_cars.gear.unique()
df_cars.loc[df_cars.gear == '-/- (Getriebeart)','gear'] = 'unknown'
#data = [go.Histogram(x=df_cars.gear)]
#py.iplot(data, filename='basic histogram')
###headline
#we leave this for now --> maybe tfidf later!

###horsepower
#df_cars.horsepower.unique()#run again and decide what to do


def get_horesepower(str):
    try:
        return re.search(r"\((\w+)\s",str).group(1)
    except AttributeError:
        return 'NA'

df_cars.loc[:,'horsepower'] = df_cars.horsepower.apply(get_horesepower)
df_cars = df_cars[df_cars.horsepower != 'NA']
df_cars.loc[:,'horsepower'] = pd.to_numeric(df_cars.horsepower)

#data = [go.Histogram(x=df_cars.horsepower)]
#py.iplot(data, filename='basic histogram')


###id
#is the number of unique id equal to the number of rows?
#len(df_cars) == len(df_cars.id.unique())


###kilometers
df_cars.loc[:,'kilometers'] = df_cars.kilometers.apply(lambda x: x.replace('.',''))
#len(df_cars.kilometers[df_cars.kilometers == '-'])
df_cars = df_cars[df_cars.kilometers != '-']
df_cars.loc[:,'kilometers'] = pd.to_numeric(df_cars.kilometers)
#len(df_cars.kilometers[df_cars.kilometers > 9e5])
df_cars = df_cars[df_cars.kilometers < 9e5]

#data = [go.Histogram(x=df_cars.kilometers,nbinsx = 100)]
#py.iplot(data, filename='basic histogram') ###looks good like its measured in k


###owners
#df_cars.owners.unique()
df_cars.loc[df_cars['owners'] == '-', 'owners'] = 2 #mean of owners (roughly)
df_cars.loc[:,'owners'] = pd.to_numeric(df_cars.owners)


###price
df_cars.loc[:,'price'] = df_cars.price.apply(lambda x: x.replace('.',''))
df_cars.loc[:,'price'] = pd.to_numeric(df_cars.price)
#len(df_cars.price[df_cars.price > 5e6])
df_cars = df_cars[df_cars.price < 8e6]

#data = [go.Histogram(x=df_cars.price,nbinsx = 100)]
#py.iplot(data, filename='basic histogram')


###used
#df_cars.used.unique() ##looks good
#data = [go.Histogram(x=df_cars.used,nbinsx = 200)]
#py.iplot(data, filename='basic histogram')

##scrapeed
#df_cars.scraped.unique()

###colour
#df_cars.colour.unique()
#data = [go.Histogram(x=df_cars.colour,nbinsx = 200)]
#py.iplot(data, filename='basic histogram')



###bodzshape
#df_cars.body_shape.unique()
#data = [go.Histogram(x=df_cars.body_shape)]
#py.iplot(data, filename='basic histogram')

###interior
#df_cars.interior.unique()

#data = [go.Histogram(x=df_cars.interior)]
#py.iplot(data, filename='basic histogram')

###painting
#df_cars.painting.unique()

#data = [go.Histogram(x=df_cars.painting)]
#py.iplot(data, filename='basic histogram')


###HU
#df_cars.HU.unique()

#data = [go.Histogram(x=df_cars.HU)]
#py.iplot(data, filename='basic histogram')

###checkbook
#df_cars.checkbook.unique()




################################################################################
#finally we drop the columns we dont need and write the cleaned df #
# cars_cleaned.h5
################################################################################

drop_columns = ['id','detail_link','state_str','features_str','checkbook',
                'HU','painting']

df_cars_cleaned =  df_cars.drop(drop_columns, axis=1)
df_cars_cleaned = df_cars_cleaned.reset_index(drop=True)
df_cars_cleaned

df_cars_cleaned.to_hdf('data/cars_cleaned.h5',
                 key='df_cars',
                 mode='w')
