import config
import json
import pathlib
import sys
from datetime import datetime

sys.path.append('script')


def setup():
    result = pathlib.Path(config.result_path)
    result.mkdir(parents=True, exist_ok=True)

    recipe = pathlib.Path(config.recipe)
    recipe.mkdir(parents=True, exist_ok=True)


def teardown(score, running_time):
    config_data = {}
    for key in dir(config):
        if key.startswith("__"):
            continue

        config_data[key] = eval(f"config.{key}")
    config_data['score'] = score
    config_data['running_time'] = running_time
    config_data['time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    recipe = pathlib.Path(config.recipe)
    with open(recipe / f"{config.name}.json", 'w') as f:
        json.dump(config_data, f)


def main():
    setup()
    script = __import__(config.script)
    score, running_time = script.run()
    teardown(score, running_time)
    print("Finish", config.name)


if __name__ == '__main__':
    main()
