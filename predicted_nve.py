import keras
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img, load_img
from os import walk
import pandas as pd
import numpy


#loading model
model = load_model('model9_4conv.h5')


#loading test data 
_, _, filenames = next(walk("data/images_nve"))
#print("\n \n filenames",filenames)



#predicting values for image one by one
columns=['RV', 'NRV', 'VE', 'NVE', 'NONE']

pred = numpy.zeros([len(filenames),5], dtype=float)

for i in range(len(filenames)):
    image = 'data/images_nve/' + filenames[i]
    img = load_img(image, target_size=(224, 224))
    x = img_to_array(img) 
    x = x.reshape((1,) + x.shape)
    pred[i] = model.predict(x)
#print("\n \n predicted values",pred)

    results=pd.DataFrame(pred, columns=columns)
    results["imgpath"] = image
    ordered_cols=["imgpath"]+columns
    results=results[ordered_cols]#To get the same column order
    results.to_csv("result_nve.csv",index=False)
