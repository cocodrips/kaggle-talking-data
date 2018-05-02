base_X_keys = ['ip', 'app', 'device', 'os', 'channel', 'click_time']
train_columns = base_X_keys + ['is_attributed']
test_columns = base_X_keys + ['click_id']
dtypes = {
    'ip': 'uint32',
    'app': 'uint16',
    'device': 'uint16',
    'os': 'uint16',
    'channel': 'uint16',
    'is_attributed': 'uint8',
    'click_id': 'uint32'
}
