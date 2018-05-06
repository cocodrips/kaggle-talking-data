import gc
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pathlib
import pickle
import time
import warnings
import json
import xgboost as xgb
from sklearn.model_selection import train_test_split
import lightgbm as lgb
import config

warnings.filterwarnings('ignore')
plt.style.use('ggplot')


def run():
    np.random.RandomState(config.random_state)
    start_time = time.time()
    my_data_path = pathlib.Path('my-data')

    models = {
        # 'lightgbm-features-v2-select-5': {'weight': 1, 't': 'lightgbm'},
        'xgboost-features-v2-select-5-0.25': {'weight': 1, 't': 'xgboost'}
    }
    result_path = pathlib.Path('result')
    recipe_path = pathlib.Path('recipe')

    if config.is_submit:
        test = pd.DataFrame()
        for filepath in (my_data_path / f'test_{config.data_suffix}').glob(
            '*.tar.gz'):
            print (f'load: {filepath}')
            df = pd.read_csv(filepath,
                             compression='gzip')
            test = pd.concat([test, df])

        """ test """
        print("test data shape:", test.shape)
        click_id = test['click_id'].astype('int')
        test.drop(['click_id'], axis=1, inplace=True)

        attributed = pd.DataFrame()
        for model_path, param in models.items():
            print('>>>', model_path)
            result = result_path / model_path / 'model.pickle'
            recipe = recipe_path / model_path / f'{model_path}.json'
            with open(result, 'rb') as f:
                model = pickle.load(f)

            with open(recipe, 'r') as f:
                params = json.load(f)

            t = test[params['features']]
            if param.get('t') == 'lightgbm':
                attributed[model_path] = model.predict(t,
                                                       num_iteration=model.best_iteration)
            if param.get('t') == 'xgboost':
                dtest = xgb.DMatrix(t)
                attributed[model_path] = model.predict(dtest,
                                                       ntree_limit=model.best_ntree_limit)

        sub = pd.DataFrame(
            {
                'click_id': click_id,
                'is_attributed': attributed.mean(axis=1)
            }
        )

        sub.to_csv(
            pathlib.Path(config.result_path) / f'submit_{config.name}.csv',
            float_format='%.6f', index=False)

    end_time = time.time()
    return '-', int(end_time - start_time)


if __name__ == '__main__':
    run()
