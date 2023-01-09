import glob
import re
import os
import PIL
from PIL import Image
import pandas as pd


PATH = os.getenv('INSTA_FOLDER_PATH')


def find_new_photos():
    return sorted(glob.glob(PATH + '\*.jpg'), key=os.path.getmtime)


def change_names():
    # rename the files so that none of them overlap
    for index, row in df.iterrows():
        temp_name = '\\' + str(index)
        os.rename(df.at[index, 'photo_path'], PATH + temp_name)
        df.at[index, 'photo_path'] = PATH + temp_name
    # checking index of last added photo
    indexes_of_added_photos = []
    for file in glob.glob(PATH + '\\Added\\insta_*.jpg'):
        indexes_of_added_photos.append(int(re.findall(r'\d+', file)[0]))
    last_index = max(indexes_of_added_photos)
    # changing names of new photos
    for index, row in df.iterrows():
        new_name = '\\insta_%d.jpg' % (last_index + 1)
        os.rename(df.at[index, 'photo_path'], PATH + new_name)
        df.at[index, 'photo_path'] = PATH + new_name
        last_index += 1


def what_resolution_it_is():
    # adding resolution and ratio to dataframe
    x = []
    y = []
    ratio = []
    for photo in df['photo_path']:
        x.append(PIL.Image.open(photo).size[0])
        y.append(PIL.Image.open(photo).size[1])
        ratio.append(round(x[-1] / y[-1], 2))
    df['x'] = x
    df['y'] = y
    df['ratio'] = ratio


def add_white_stripes_if_needed():
    # checking if photos have different ratio
    if df.ratio.nunique() != 1:
        # if they have various ratio add white stripes, so they mutual fit instagram ratio
        for index, row in df.iterrows():
            if df.at[index, 'ratio'] != 0.80:
                photo = Image.open(df.at[index, 'photo_path'])
                new = Image.new(mode='RGB', size=(1080, 1350), color='white')
                new.paste(photo, (0, (1350 - photo.size[1])//2))
                new.save(df.at[index, 'photo_path'])


if __name__ == '__main__':
    df = pd.DataFrame(find_new_photos(), columns=['photo_path'])
    change_names()
    what_resolution_it_is()
    add_white_stripes_if_needed()
