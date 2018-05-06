import gc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib
import pickle
import time
import warnings
from sklearn.model_selection import train_test_split
import lightgbm as lgb
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
    X.drop(config.y_keys, axis=1, inplace=True)
    y = train['is_attributed']
    (X_train, X_test,
     y_train, y_test) = train_test_split(X, y,
                                         test_size=0.1,
                                         random_state=config.random_state)
    del train
    gc.collect()


    xgtrain = lgb.Dataset(X_train, label=y_train,
                          categorical_feature=config.categorical_features
                          )

    xgtrain_small = lgb.Dataset(X_train[:100000], label=y_train[:100000],
                                categorical_feature=config.categorical_features
                                )
    xgvalid = lgb.Dataset(X_test, label=y_test,
                          categorical_feature=config.categorical_features
                          )
    del X_train, X_test, y_train, y_test
    gc.collect()

    evals_results = {}

    bst1 = lgb.train(config.params,
                     xgtrain,
                     valid_sets=[xgtrain_small, xgvalid],
                     valid_names=['train_small', 'valid'],
                     evals_result=evals_results,
                     num_boost_round=config.n_boost_round,
                     early_stopping_rounds=config.early_stopping_rounds,
                     verbose_eval=5)

    print("\nModel Report")
    print("bst1.best_iteration: ", bst1.best_iteration)
    print("auc:",
          evals_results['valid']['auc'][bst1.best_iteration - 1])

    bst, best_iteration = (bst1, bst1.best_iteration)
    print('{}sec: model training time'.format(int(time.time() - start_time)))

    del xgtrain, xgvalid

    lgb.plot_importance(bst, max_num_features=300)
    plt.tight_layout()
    plt.savefig(f"{config.result_path}/importance.png")

    gc.collect()

    # Test data

    if config.is_submit:
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
        is_attributed = bst.predict(test, num_iteration=best_iteration)

        del test
        gc.collect()

        sub = pd.DataFrame(
            {
                'click_id': click_id,
                'is_attributed': is_attributed
            }
        )

        sub.to_csv(
            pathlib.Path(config.result_path) / f'submit_{config.name}.csv',
            float_format='%.6f', index=False)

    if config.save_model:
        with open(pathlib.Path(config.result_path) / 'model.pickle', 'wb') as f:
            pickle.dump(bst, f)

    end_time = time.time()
    return bst.best_score['valid']['auc'], int(end_time - start_time)
