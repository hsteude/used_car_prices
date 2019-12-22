'''
idea:
prepare data set for modelling through:
- generate new features (e.g. age in years)
- apply tfidf encoding for title string
- encode categorical features through label and one hot encoding
- normalize numerical features
'''


import pandas as pd
import datetime
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler


##############################################################################
# generate age feature
##############################################################################
# df_cars['age_in_days'] = df_cars.build.apply(\
#                lambda x: (datetime.datetime.today() - x).days)

##############################################################################
# tfidf vercorization
##############################################################################
def tfidf_vecotizer(corpus, fit=True):
    tfidf_vectorizer = TfidfVectorizer()
    if fit:
        tfidf_vectorizer.fit(corpus)
        # safe vectorizer
        joblib.dump(tfidf_vectorizer, 'models/tfidf_vectorizer.pkl')
    else:
        tfidf_vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
    TfIdf_mat = tfidf_vectorizer.transform(corpus).todense()
    columns = ['__' + x for x in tfidf_vectorizer.get_feature_names()]
    tfidf_df = \
        pd.DataFrame(TfIdf_mat, columns=columns)
    return tfidf_df


##############################################################################
# label encoding
##############################################################################
def get_categorical_cols(df_cars):
    categ_cols = df_cars.select_dtypes('object').columns.tolist()
    categ_cols.remove('headline')
    df_cat_cols = df_cars.copy()
    df_cat_cols = df_cat_cols[categ_cols]
    return df_cat_cols


# Encoding the variable
def labelencoder(df_cat_cols, fit=True):
    if fit:
        d = defaultdict(LabelEncoder)
        df_cat_cols_enc = df_cat_cols.apply(
            lambda x: d[x.name].fit_transform(x))
        joblib.dump(d, 'models/label_encoder_dict.pkl')
    else:
        d = joblib.load('models/label_encoder_dict.pkl')
        df_cat_cols_enc = df_cat_cols.apply(lambda x: d[x.name].transform(x))
    return df_cat_cols_enc


##############################################################################
# one hot encoding
##############################################################################

def one_hot_enc_arr(df, fit=True):
    '''
    This function:
    - takes pd.df and encodes all colums using one hot encoding
    - returns a numpy array with same or larger number of colums
    - and saves the encoder object to "one_hot_enc.pkl"
    - note: if fit is set to False, it will use the pretrained encoder object
    '''
    if fit == True:
        one_hot_enc = OneHotEncoder()
        one_hot_enc.fit(df.values)
        joblib.dump(one_hot_enc, 'models/one_hot_enc.pkl')
    else:
        one_hot_enc = joblib.load('models/one_hot_enc.pkl')

    arr_ohe = one_hot_enc.transform(df.values).toarray()
    df_ohe = pd.DataFrame(arr_ohe)
    return df_ohe


##############################################################################
# standardization
##############################################################################
def get_numerical_cols(df_cars):
    numeric_cols = df_cars.select_dtypes('int').columns.tolist()
    df_num_cols = df_cars.copy()
    df_num_cols = df_num_cols[numeric_cols]
    df_num_cols = df_num_cols.drop('price', axis=1)
    return df_num_cols


def stand_scaler(df, fit=True):
    '''
    This function:
    - takes a pandas data frame and normalizes all columns using sklear StandardScaler
    - and saves to encoder object to "std_scaler.pkl"
    - note: if fit is set to False, it will use the pretrained encoder object
    '''
    df = df.copy().astype('float')
    if fit == True:
        std_scaler = StandardScaler()
        std_scaler.fit(df.values)
        joblib.dump(std_scaler, 'models/std_scaler.pkl')
    else:
        std_scaler = joblib.load('models/std_scaler.pkl')
    arr_std = std_scaler.transform(df.values)
    df_std = pd.DataFrame(arr_std, columns=df.columns)
    return df_std


##############################################################################
# transformation function
##############################################################################

def preprocess_data(df_cars, fit):
    df_cars = df_cars.copy()
    df_cars['age_in_days'] = df_cars.build.apply(
        lambda x: (datetime.datetime.today() - x).days)

    df_tfidf_headline = tfidf_vecotizer(df_cars.headline)

    df_cat_cols = get_categorical_cols(df_cars)
    df_cat_cols_enc = labelencoder(df_cat_cols, fit)

    df_one_hot = one_hot_enc_arr(df_cat_cols_enc, fit)

    df_num_cols = get_numerical_cols(df_cars)
    df_std = stand_scaler(df_num_cols, fit)

    df_preprossesed = pd.concat(
        [df_std, df_one_hot, df_tfidf_headline], axis=1)
    return df_preprossesed


def main():
    df_cars = pd.read_hdf('data/cars_cleaned.h5')
    fit = True
    X = preprocess_data(df_cars, fit)
    X.to_hdf('data/X.h5',
             key='X',
             mode='w')
    df_cars.price.to_hdf('data/y.h5',
                         key='y',
                         mode='w')


if __name__ == '__main__':
    main()
