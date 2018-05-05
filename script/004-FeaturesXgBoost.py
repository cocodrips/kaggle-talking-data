import gc
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import pickle
import time
import warnings
import sys
import xgboost as xgb
import lightgbm as lgb
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
    n = 100 * config.training_rate

    # Training data
    for filepath in sorted(
        (my_data_path / f'train_{config.data_suffix}').glob('*.tar.gz')):
        if i % 5 == 0:
            print(f">>> load {i}")
        if i >= n:
            break
        print(filepath)
        df = pd.read_csv(filepath,
                         usecols=config.train_keys,
                         compression='gzip')
        train = pd.concat([train, df])
        i += 1

    print("training data shape:", train.shape)


    '''Features'''
    y = train['is_attributed']
    X = train[:]
    X.drop(config.y_keys, axis=1, inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=0.1,
                                                        random_state=42)
    dtrain = xgb.DMatrix(X_train, y_train)
    dvalid = xgb.DMatrix(X_test, y_test)
    del train
    del X_train, X_test, y_train, y_test
    gc.collect()

    lgb_params = {
        'boosting_type': 'gbdt',
        'objective': 'binary',
        'metric': 'auc',
        'learning_rate': 0.04,
        #'is_unbalance': 'true',  #because training data is unbalance (replaced with scale_pos_weight)
        'num_leaves': 31,  # we should let it be smaller than 2^(max_depth)
        'max_depth': -1,  # -1 means no limit
        'min_child_samples': 20,  # Minimum number of data need in a child(min_data_in_leaf)
        'max_bin': 255,  # Number of bucketed bin for feature values
        'subsample': 0.6,  # Subsample ratio of the training instance.
        'subsample_freq': 0,  # frequence of subsample, <=0 means no enable
        'colsample_bytree': 0.3,  # Subsample ratio of columns when constructing each tree.
        'min_child_weight': 5,  # Minimum sum of instance weight(hessian) needed in a child(leaf)
        'subsample_for_bin': 200000,  # Number of samples for constructing bin
        'min_split_gain': 0,  # lambda_l1, lambda_l2 and min_gain_to_split to regularization
        'reg_alpha': 0.99,  # L1 regularization term on weights
        'reg_lambda': 0.9,  # L2 regularization term on weights
        'nthread': 8,
        'verbose': 1,
    }

    xgtrain = lgb.Dataset(dtrain[predictors].values, label=dtrain[target].values,
                          feature_name=predictors,
                          categorical_feature=categorical_features
                          )
    xgvalid = lgb.Dataset(dvalid[predictors].values, label=dvalid[target].values,
                          feature_name=predictors,
                          categorical_feature=categorical_features
                          )
    del dtrain
    del dvalid
    
    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    model = xgb.train(params, dtrain, 200, watchlist, maximize=True,
                      early_stopping_rounds=25, verbose_eval=5)

    plot_importance(model)
    plt.tight_layout()
    plt.savefig(f"{config.result_path}/importance.png")

    del dtrain, dvalid
    gc.collect()

    click_id = test['click_id'].astype('int')
    test.drop(['click_id'], axis=1, inplace=True)
    dtest = xgb.DMatrix(test)

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
