name = "lightgbm-features-v2-select-6-0.50"
is_submit = True
save_model = True
submit_score = ""
training_rate = 0.50

script = "004-LightGBM"
# script = "003-BasicXgBoost"
data_suffix = "feature_v2"
result_path = f"result/{name}"
recipe = f"recipe/{name}"

categorical_features = ['app',
                        'device',
                        'os',
                        'channel']
features = ['app',
            # 'ip',
            'device',
            'os',
            'channel',
            'hour',
            # 'day',
            'hour_cos',
            'hour_sin',
            'next_1_ip_device_os_click',
            'next_1_ip_app_device_os_click',
            'next_1_ip_app_device_os_channel_click',
            'prev_1_ip_channel_click',
            'prev_1_ip_os_click',
            'count_by_ip',
            'count_by_device_os_app',
            'count_by_device_os',
            'count_ip_day_hour',
            'count_ip_app',
            'count_ip_app_os',
            'app_by_ip',
            'app_by_ip_device_ps',
            'channel_by_app',
            'channel_by_ip',
            'device_by_ip',
            'hour_by_ip_day',
            'os_by_ip_app',
            'cumcount_by_ip',
            'cumcount_by_ip_device_os']
random_state = 124

y_keys = ["attributed_time", "is_attributed"]
train_keys = y_keys + features
test_keys = ["click_id"] + features

n_boost_round = 1500
early_stopping_rounds = 100

params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': 'auc',

    'learning_rate': 0.04,
    # 'is_unbalance': 'true', # replaced with scale_pos_weight argument
    'num_leaves': 31,  # 2^max_depth - 1
    'max_depth': -1,  # -1 means no limit
    'min_child_samples': 30,
    # Minimum number of data need in a child(min_data_in_leaf)
    'max_bin': 255,  # Number of bucketed bin for feature values
    'subsample': 0.6,  # Subsample ratio of the training instance.
    'subsample_freq': 0,  # frequence of subsample, <=0 means no enable
    'colsample_bytree': 0.3,
    # Subsample ratio of columns when constructing each tree.
    'min_child_weight': 5,
    # Minimum sum of instance weight(hessian) needed in a child(leaf)
    'subsample_for_bin': 200000,  # Number of samples for constructing bin
    'min_split_gain': 0,
    # lambda_l1, lambda_l2 and min_gain_to_split to regularization
    'reg_alpha': 0.99,  # L1 regularization term on weights
    'reg_lambda': 0.9,  # L2 regularization term on weights
    'scale_pos_weight': 150
    # because training data is extremely unbalanced 
}

# params = {
#     'eta': 0.3,
#     'tree_method': "hist",
#     'grow_policy': "lossguide",
#     'max_leaves': 1400,
#     'max_depth': 0,
#     'subsample': 0.9,
#     'colsample_bytree': 0.7,
#     'colsample_bylevel': 0.7,
#     'min_child_weight': 0,
#     'alpha': 4,
#     'objective': 'binary:logistic',
#     'scale_pos_weight': 9,
#     'eval_metric': 'auc',
#     'nthread': 8,
#     'random_state': random_state,
#     'silent': True
# }
