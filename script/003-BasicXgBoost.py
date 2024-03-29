import gc
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import pickle
import time
import numpy as np
import warnings
import sys
import xgboost as xgb
from sklearn.model_selection import train_test_split
from xgboost import plot_importance
import config

warnings.filterwarnings('ignore')
plt.style.use('ggplot')


def run():
    np.random.RandomState(config.random_state)
    start_time = time.time()
    my_data_path = pathlib.Path('my-data')

    '''Load'''
    train = pd.DataFrame()

    n = int(100 * config.training_rate)
    numbers = np.random.randint(0, 100, n)

    # Training data
    for i, filepath in enumerate(sorted(
        (my_data_path / f'train_{config.data_suffix}').glob('*.tar.gz'))):

        if i not in numbers:
            continue
        print(filepath)
        df = pd.read_csv(filepath, usecols=config.train_keys,
                         compression='gzip')
        train = pd.concat([train, df])

    print("training data shape:", train.shape)
    gc.collect()

    '''Features'''

    X = train[:]
    y = train['is_attributed']
    X.drop(config.y_keys, axis=1, inplace=True)
    (X_train, X_test,
     y_train, y_test) = train_test_split(X, y, test_size=0.1,
                                         random_state=config.random_state)
    dtrain = xgb.DMatrix(X_train, y_train)
    dvalid = xgb.DMatrix(X_test, y_test)
    del train
    gc.collect()

    '''valid'''

    watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
    model = xgb.train(config.params, dtrain, 200, watchlist, maximize=True,
                      early_stopping_rounds=config.early_stopping_rounds,
                      verbose_eval=5)

    plot_importance(model)
    plt.tight_layout()
    plt.savefig(f"{config.result_path}/importance.png")

    del dtrain, dvalid
    gc.collect()

    if config.is_submit:
        # Test data
        test = pd.DataFrame()
        for filepath in (my_data_path / f'test_{config.data_suffix}').glob(
            '*.tar.gz'):
            df = pd.read_csv(filepath, usecols=config.test_keys,
                             compression='gzip')
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

        sub.to_csv(
            pathlib.Path(config.result_path) / f'submit_{config.name}.csv',
            float_format='%.6f', index=False)

    if config.save_model:
        with open(pathlib.Path(config.result_path) / 'model.pickle', 'wb') as f:
            pickle.dump(model, f)

    end_time = time.time()
    return model.best_score, int(end_time - start_time)
