name = "BasicXgBoost"
training_rate = 0.02
script = "003-BasicXgBoost"
data_suffix = "expanded"
result_path = f"result/{name}"
recipe = f"recipe/{name}"
features = ["app",
            "device",
            "channel",
            "os",
            "next_click",
            "prev_click",
            "hour",
            "day",
            "clicks_by_ip"]
y_keys = ["attributed_time", "is_attributed"]
train_keys = y_keys + features
test_keys = ["click_id"] + features

"""
Parameter
"""
