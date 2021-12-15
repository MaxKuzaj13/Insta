import requests
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
from datetime import datetime
import ast
from PIL import Image
import os
import json


def import_env():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    api_key_value = os.environ.get('api_key')
    return api_key_value


def collect_df(i):
    url = f'https://pixabay.com/api/?key={api_key}&q=girl+sexy&per_page=200&image_type=photo'
    r = requests.get(url + f'&page={i}')
    return pd.DataFrame(r.json()['hits'])


def append_df():
    df_out = pd.DataFrame()
    for i in range(1, 5):
        if i == 1:
            df_out = collect_df(i)
        else:
            try:
                df_app = collect_df(i)
                df_out = df_out.append(df_app)
            except ValueError:
                break
    return df_out


def read_downloaded_id():
    try:
        with open('downloaded.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            dictionary = json.loads(data)
    except FileNotFoundError:
        print('No file found')
        dictionary = {}
    return dictionary


def pars_dowloaded(d):
    downloaded_list = str(d.values()).replace("dict_values(['[", "")\
        .replace("[", "").replace("]", "").replace(")","").replace("'", "")
    try:
        downloaded_id = list(set(ast.literal_eval(downloaded_list)))
    except SyntaxError:
        downloaded_id = []
    return downloaded_id


def save_now_downloaded():
    now_time = datetime.now()
    dic[now_time.strftime("%Y_%m_%d_%H_%M_%S")] = str(list(df_filtered_new['id'].head(limit)))
    json_object = json.dumps(dic, indent=3, sort_keys=True)
    with open('downloaded.json', 'w') as f:
        json.dump(json_object, f, ensure_ascii=False)
    return now_time


def iterate_and_save_photos(df_filtered_new):
    for id_el in range(len(df_filtered_new)):
        print(df_filtered_new['id'][id_el])
        url = df_filtered_new['largeImageURL'][id_el]
        f_ext = os.path.splitext(url)[-1]
        try:
            path = os.path.join('img/', now.strftime("%Y_%m_%d"))
            os.makedirs(path)
        except FileExistsError:
            pass
        image = Image.open(requests.get(url, stream=True).raw)
        # image watermark size
        size = (100, 100)
        position_width = image.size[0] - size[0]
        position_height = image.size[1] - size[1]
        crop_image = Image.open('watermark_img/logo_square.png')
        # to keep the aspect ratio in intact
        crop_image.thumbnail(size)
        # add watermark
        copied_image = image.copy()
        # base image
        copied_image.paste(crop_image, (position_width, position_height))
        f_name = 'img/' + now.strftime("%Y_%m_%d") + '/img_' + str(df_filtered_new['id'][id_el]) + '{}'.format(
            f_ext)
        copied_image.save(f_name)


if __name__ == "__main__":
    print("Init")
    limit = 10
    api_key = import_env()
    df = append_df()
    df_sorted = df.sort_values(by=['likes', 'downloads'], ascending=[False, False],
                               na_position='first').reset_index().drop(['index'], axis=1)
    dic = read_downloaded_id()
    downloaded = pars_dowloaded(dic)
    df_filtered_new = df_sorted[~df_sorted.id.isin(downloaded)]
    df_filtered_new = df_filtered_new.reset_index().drop(['index'], axis=1).head(limit)
    now = save_now_downloaded()
    iterate_and_save_photos(df_filtered_new)
    print('Finished')
else:
    print("Executed when imported")
