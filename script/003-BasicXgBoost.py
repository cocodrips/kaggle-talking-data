import gc
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import pickle
import time
import warnings
import sys
import xgboost as xgb
from sklearn.model_selection import train_test_split
from xgboost import plot_importance
import config

warnings.filterwarnings('ignore')
plt.style.use('ggplot')


def run():
    start_time = time.time()
    my_data_path = pathlib.Path('my-data')

    '''Load'''
    train = pd.DataFrame()
    i = 0
    n = 70 * config.training_rate

    # Training data
    for filepath in sorted(
        (my_data_path / f'train_{config.data_suffix}').glob('*.tar.gz')):
        if i % 5 == 0:
            print(f">>> load {i}")
        if i >= n:
            break
        print(filepath)
        df = pd.read_csv(filepath, usecols=config.train_keys,
                         compression='gzip')
        train = pd.concat([train, df])
        i += 1

    n = 30 * config.training_rate
    i = 0
    for filepath in sorted(
        (my_data_path / f'valid_{config.data_suffix}').glob('*.tar.gz')):

        if i % 5 == 0:
            print(f">>> load {i}")
        if i >= n:
            break
        print(filepath)
        df = pd.read_csv(filepath, usecols=config.train_keys,
                         compression='gzip')
        train = pd.concat([train, df])
        i += 1

    print("training data shape:", train.shape)

    '''valid'''
    valid = pd.DataFrame()
    start = n
    i = 0
    n = start + (100 * config.valid_rate)    
    # Training data
    for filepath in sorted(
        (my_data_path / f'valid_{config.data_suffix}').glob('*.tar.gz')):
        if i < start:
            i+= 1
            continue
        if i % 5 == 0:
            print(f">>> load {i}")
        if i >= n:
            break
        print(filepath)
        df = pd.read_csv(filepath, usecols=config.train_keys,
                         compression='gzip')
        valid = pd.concat([valid, df])
        i += 1

    print("valid data shape:", train.shape)

    '''Features'''

    X = train[:]
    X.drop(config.y_keys, axis=1, inplace=True)
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1,
    #                                                     random_state=42)
    dtrain = xgb.DMatrix(X, train['is_attributed'])
    del train
    gc.collect()

    '''valid'''
    X = valid[:]
    print(X.columns, valid.columns)
    X.drop(config.y_keys, axis=1, inplace=True)
    dvalid = xgb.DMatrix(X, valid['is_attributed'])
    del valid
    gc.collect()

    params = {
        'eta': 0.3,
        'tree_method': "hist",
        'grow_policy': "lossguide",
        'max_leaves': 1400,
        'max_depth': 0,
        'subsample': 0.9,
        'colsample_bytree': 0.7,
        'colsample_bylevel': 0.7,
        'min_child_weight': 0,
        'alpha': 4,
        'objective': 'binary:logistic',
        'scale_pos_weight': 9,
        'eval_metric': 'auc',
        'nthread': 8,
        'random_state': config.random_state,
        'silent': True
    }

    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    model = xgb.train(params, dtrain, 200, watchlist, maximize=True,
                      early_stopping_rounds=25, verbose_eval=5)

    plot_importance(model)
    plt.tight_layout()
    plt.savefig(f"{config.result_path}/importance.png")

    del dtrain, dvalid
    gc.collect()

    # Test data
    test = pd.DataFrame()
    for filepath in (my_data_path / f'test_{config.data_suffix}').glob(
        '*.tar.gz'):
        df = pd.read_csv(filepath, usecols=config.test_keys, compression='gzip')
        test = pd.concat([test, df])

    """ test """
    print("test data shape:", test.shape)
    click_id = test['click_id'].astype('int')
    test.drop(['click_id'], axis=1, inplace=True)
    dtest = xgb.DMatrix(test)

    del test
    gc.collect()

    sub = pd.DataFrame(
        {
            'click_id': click_id,
            'is_attributed': model.predict(dtest,
                                           ntree_limit=model.best_ntree_limit)
        }
    )

    sub.to_csv(pathlib.Path(config.result_path) / f'submit_{config.name}.csv',
               float_format='%.6f', index=False)

    with open(pathlib.Path(config.result_path) / 'model.pickle', 'wb') as f:
        pickle.dump(model, f)

    end_time = time.time()
    return model.best_score, int(end_time - start_time)
