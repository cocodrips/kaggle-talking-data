name = "BasicXgBoost-features-valid-brend-all"
training_rate = 0.4
valid_rate = 0.2
script = "003-BasicXgBoost"
data_suffix = "features"
result_path = f"result/{name}"
recipe = f"recipe/{name}"
features = [
    'app_count',
    'os_count',
    'device_count',
    'channel_count',
    'next_1_ip_app_device_os_click',
    'next_2_ip_app_device_os_click',
    'prev_1_ip_app_device_os_click',
    'prev_2_ip_app_device_os_click',
    'next_1_ip_app_device_os_channel_click',
    'next_2_ip_app_device_os_channel_click',
    'prev_1_ip_app_device_os_channel_click',
    'prev_2_ip_app_device_os_channel_click',
    'next_1_ip_device_os_click',
    'next_2_ip_device_os_click',
    'prev_1_ip_device_os_click',
    'prev_2_ip_device_os_click',
    'clicks_ip_device_os_app',
    'clicks_ip_device_os',
    'clicks_ip_device_os_app_hour',
    'clicks_ip_device_os_channel',
    'day',
    'hour_cos',
    'hour_sin',
]
random_state = 42

y_keys = ["attributed_time", "is_attributed"]
train_keys = y_keys + features
test_keys = ["click_id"] + features

# name = "BasicXgBoost"
# training_rate = 0.02
# script = "003-BasicXgBoost"
# data_suffix = "expanded"
# result_path = f"result/{name}"
# recipe = f"recipe/{name}"
# features = ["app",
#             "device",
#             "channel",
#             "os",
#             "next_click",
#             "prev_click",
#             "hour",
#             "day",
#             "clicks_by_ip"]
# y_keys = ["attributed_time", "is_attributed"]
# train_keys = y_keys + features
# test_keys = ["click_id"] + features
# 
# """
# Parameter
# """
