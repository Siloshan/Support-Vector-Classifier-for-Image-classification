# -*- coding: utf-8 -*-
"""Svc_classifire.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NiW6Qml982fdaz1w3HcE_P8miAX1quxS
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
from skimage.io import imread
from skimage.transform import resize
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import os
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

from google.colab import drive
drive.mount('/content/drive')

! pip install kaggle

! mkdir ~/.kaggle

! cp '/content/drive/MyDrive/Colab Notebooks/My_work/kaggle.json' ~/.kaggle/

! chmod 600 ~/.kaggle/kaggle.json

#! kaggle datasets download -d prasoonkottarathil/face-mask-lite-dataset

#! unzip /content/face-mask-lite-dataset.zip

df = pd.DataFrame(columns=['image_path','Lable', 'flatten'])

def load_data_to_data_frame():
  images_with_mask=0
  images_with_mask_limit=20
  images_without_mask=0
  images_without_mask_limit=20
  

  for dirname, _, filenames in os.walk('/content/face-mask-lite-dataset'):
  #for dirname, _, filenames in os.walk('/kaggle/input/facemask-detection-dataset-20000-images'):
    for filename in filenames:
      path=os.path.join(dirname, filename)
      #print(path)
      if '/without_mask'in path:
        if images_without_mask<images_without_mask_limit:
          images_without_mask=images_without_mask+1
          print("images_without_mask"+str(images_without_mask))
            #path=os.path.join(dirname, filename)
            #print(os.path.join(dirname, filename))
          img = imread(path) 
          img = resize(img, (15, 15)) 
          new_row = {'image_path': path, 'Lable': 'without_mask', 'flatten': img.flatten()} 
          # Use the loc method to add the new row to the DataFrame
          df.loc[len(df)] = new_row
      if '/with_mask'in path:
        if images_with_mask<images_with_mask_limit:    
          images_with_mask=images_with_mask+1
          print("images_with_mask"+str(images_with_mask))
            #path=os.path.join(dirname, filename)
            #print(os.path.join(dirname, filename))
          img = imread(path) 
          img = resize(img, (15, 15)) 
          new_row = {'image_path': path, 'Lable': 'with_mask', 'flatten': img.flatten()} 
          # Use the loc method to add the new row to the DataFrame
          df.loc[len(df)] = new_row
      #if (images_without_mask>=images_without_mask_limit):
        #if (images_with_mask>=images_with_mask_limit):
          #break
          #break
  #print(df.head)

load_data_to_data_frame()

df.shape

df.head(50)



from sklearn import preprocessing
lable_encoder_df_lable= preprocessing.LabelEncoder()

lable_encoder_df_lable.fit(df['Lable'])

df['Category_label']=lable_encoder_df_lable.transform(df['Lable'])

df_train,df_test=train_test_split(df, test_size=0.2,shuffle=True)

df.head()

classifier = SVC()

parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

grid_search = GridSearchCV(classifier, parameters)
#x_train = df_train['flatten'].tolist()

grid_search.fit(df_train['flatten'].tolist(), df_train['Category_label'])

best_estimator = grid_search.best_estimator_

y_prediction = best_estimator.predict(df_test['flatten'].tolist())

score = accuracy_score(y_prediction, df_test['Category_label'])

print('{}% of samples were correctly classified'.format(str(score * 100)))

pickle.dump(best_estimator, open('./model.p', 'wb'))

"""Load and predic pick file"""

pickled_model = pickle.load(open('/content/model.p', 'rb'))

img = imread('/content/2.png') 
img = resize(img, (15, 15)) 
#img_latten= img.flatten()
df_P = pd.DataFrame(columns=['flatten'])
new_row = {'flatten': img.flatten()} 
df_P.loc[len(df_P)] = new_row
pickled_model.predict(df_P['flatten'].tolist())[0]