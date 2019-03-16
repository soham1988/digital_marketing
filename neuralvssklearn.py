#Install this stuff first, Tensorflow and Keras, the official Python wrapper
#for Tensorflow
#!pip install keras
#!pip install tensorflow

import pandas as pd 
import numpy as np

#This are some keras imports; uses tensorflow
from keras.preprocessing.text import Tokenizer # First i'm importing the tokenizer to split the texts;
from keras.models import Sequential # Keras sequential approach to neural nets;
from keras.optimizers import Adagrad # Keras optimizer
from keras.layers import Dense # Some neural network layers;


#some sklearn stuff we need
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LassoLarsCV
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

#let's snooze those super annoying sklearn convergence issues
import warnings


#Reading CSV file with pandas;
data = pd.read_csv("trainingdata.csv", encoding="latin-1")

#As we went over in class, using get_dummies to convert categoricial variables
#to 0,1 variables (aka one hot variables)

one_hot = pd.get_dummies(data,columns=["match type","brand"])


#Getting textdata from specific column, converting it into a numpy ndarray
#this is required by the tokenizer we're about to use
text_data = one_hot[["userpost"]].values.reshape(1,-1)[0]

#Using keras to tokenize userposts into array of values;
#https://keras.io/preprocessing/text/#tokenizer
#This tokenizer will follow some rules to determine when to split the text or not;
#This is useful because we're also going to one hot encode each word;
#I'm limiting the amount of words to a specific group, these are going to be the more representative of the data;
#The reason why I don't take every possible word is because of memory and performance;

tokenizer = Tokenizer(num_words=1000)

#figuring out what our 1000 words are
tokenizer.fit_on_texts(text_data) #Fitting data;


#creating a numpy arrary with the tokenized matrix for each post
#(aka actually applying our tokenizer to each piece of text)
wordmatrix = tokenizer.texts_to_matrix(text_data)

#adding in other predictors. dropping out stuff that isn't predictors
otherpredictors = one_hot.drop('Brand Mention?', axis=1)
otherpredictors = otherpredictors.drop('userpost', axis=1)

#converting predictors to numpy array, the required format
#sucks, but we lose the variable names here
otherpredictorsmatrix = otherpredictors.values

#just adding all of our predictors together
X = np.concatenate((wordmatrix, otherpredictorsmatrix), axis=1)

#this is the variable we're goint to try and predict
y = data[["Brand Mention?"]] #Getting the label as y;


#let's initialize the model!
model = Sequential()

#https://keras.io/getting-started/sequential-model-guide/

#first, the Keras model needs to know the number of columns in the model
dimensions = X.shape[1]


#adding our first layer
model.add(Dense(64,input_dim=dimensions,activation="relu")) # * Input layer *

#I tried adding a hidden layer
#to see if the problem was very complex
#A neural network with 4 hidden layers would solve for very non-linear patterns;
#it's not a very complex problem, so it actually makes the model worse
#Also it's not a good idea to have more hidden layers than needed, it will take more time to get same result;

model.add(Dense(64*2,activation="relu")) # * Hidden Layer *

#In the output layer we're getting the result out of the neural network;
#Since we're trying to predict if it's true or not we'll output only one value;
#Note that in this case, it does not matter whether one use Sigmoid or Softamx activation function;
#This both activation functions I'll output a probability value representing if it's true or not;
model.add(Dense(1, activation="softmax")) # * Output Layer *
    
model.summary()

#two key parameters here learning rate == lr
#and the name of the optimizer itself
#https://medium.com/octavian-ai/which-optimizer-and-learning-rate-should-i-use-for-deep-learning-5acb418f9b2
optimizer = Adagrad(lr=.1) #Preparing optimizer;

#Actually getting the model all ready to run
model.compile(loss="mse", optimizer=optimizer, metrics=["mse", "accuracy"]) # Compiling model for use;

#running the model
model.fit(X,y,batch_size=X.shape[0],epochs=5, shuffle=True,validation_split=0.4)#Training data;

#------------------------------------------------------------------------------


#let's try some sklearn models, really we can use any listed here:
#http://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model
#any of the linear models here would likely work well

#fist, let's suppress those annoying sklearn warnings
warnings.filterwarnings('ignore')


#sklearn likes np arrays, not data frames, so let's do values,
#X is already good
predictors = X
target = data["Brand Mention?"].values

#sklearn does not split up test/train data like Keras, so...
pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, target, test_size=.4, random_state=123)    


#http://scikit-learn.org/stable/modules/classes.html#module-sklearn.linear_model
linearmodel = LinearRegression()
linearmodel = linearmodel.fit(pred_train,tar_train)


#mean squared error
train_error = mean_squared_error(tar_train, model.predict(pred_train))
print ('Linear training data MSE')
print(train_error)

test_error = mean_squared_error(tar_test, model.predict(pred_test))
print ('Linear test data MSE')
print(test_error)
print('\n')

#http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html#sklearn.linear_model.ElasticNetCV
elasticmodel = ElasticNetCV(cv=10, random_state=0)
elasticmodel = elasticmodel.fit(pred_train,tar_train)

#mean squared error
train_error = mean_squared_error(tar_train, model.predict(pred_train))
print ('Elastic training data MSE')
print(train_error)

test_error = mean_squared_error(tar_test, model.predict(pred_test))
print ('Elastic test data MSE')
print(test_error)
print('\n')


#http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsCV.html#sklearn.linear_model.LassoLarsCV
lassomodel = LassoLarsCV(cv=10)
lassomodel = lassomodel.fit(pred_train,tar_train)


#mean squared error
train_error = mean_squared_error(tar_train, model.predict(pred_train))
print ('LASSO training data MSE')
print(train_error)

test_error = mean_squared_error(tar_test, model.predict(pred_test))
print ('LASSO test data MSE')
print(test_error)
print('\n')
