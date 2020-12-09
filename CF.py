# -*- coding: utf-8 -*-
"""CF (Project-4/Group-12).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HkKfDyiYLN3TR9MfEPZhO57cMTgDqUbl

## ***Project-4 / Group-12***

#### ***Name : Prudhviraj Sheela | OSU CWID : A20228857***

#### ***Name : Aman Masipeddi | OSU CWID : A20198116***

***Item-Item Collaborative Filtering (CF)***
"""

# Required dependencies and packages for the Item-Item Collaborative Filtering Program
import random
import numpy as np
import pandas as pd
import math
from random import randrange
from numpy.linalg import norm
from math import sqrt
from sklearn.metrics import mean_squared_error

"""***Loading of input data files and creation of dataframes*** 

"""

input_train = '/content/training_dataset.csv' # Loading the input training file
input_test = '/content/test_dataset.csv' # Loading the input test file
train_data = pd.read_csv(input_train) # Creating a data frame for the input training data loaded
test_data = pd.read_csv(input_test) # Creating a data frame for the input test data loaded

# In below step we create a utility matrix and obtain all the initial variables necessary for computation
util_mat = train_data.pivot_table(index='user_id', columns='item_id', values='rating') # Creating a pivot table using the values available in the train_data
users_mean = [0 for a in range(util_mat.shape[0])] # Creating intial users means to 0's that are later reevaluated while finding adjusted cosine similarity
util_mat_cossim = util_mat.copy().values # Duplicates a copy of values for initial cosine similarity utility matrix
util_mat_adjcossim= util_mat.copy().values # Duplicates a copy of values for adjusted cosine similarity utility matrix
items = list(util_mat.columns) # Holds the list of items or movies of the training data
users= list(util_mat.index) # Holds the list of all users of the training data

"""***Calculating Average Rating associated for each User ID***"""

# In the below step we obtain the user's mean associated for each index value which is used if there are any unknown ratings or 'nan' then it is assigned as a default average rating value for that particular user
for i in range(0, util_mat.shape[0]): # Iterates through all the number of users
  item = 0 # Stores the updated item value associated with the user
  count = 0 # Keeps track of the iterations satisfied
  for j in range(len(items)): # Iterates through all the item id's associated for corresponding user
      if not math.isnan(util_mat_cossim[i][j]): # Checks if there is no null object for the associated rating and if the condition is satisfies item is computed
          item = item + util_mat_cossim[i][j] # The item is computed for each user mean value
          count += 1 # Incrementing the count
  if count !=0: # Checks if the count is not zero and updates the associated users mean to its average mean
    users_mean[i] = item / count

"""***Cosine Similarity and Adjusted Cosine Similarity Utility Matrices Computation***"""

for a in range(0, util_mat.shape[0]): # Iterates through all the number of users
    for b in range(len(items)): # Iterates through all the item id's associated for corresponding user
      if not math.isnan(util_mat_cossim[a][b]): # Checks if there is no null object for the associated user and item's rating value
        util_mat_cossim[a][b]=util_mat_cossim[a][b] # Once the condition is satisfies the cosine similarity utility matrix is update
        util_mat_adjcossim[a][b]=util_mat_adjcossim[a][b]- users_mean[a] # Once the condition is satisfies the cosine similarity utility matrix is updated by subtracting with the row's mean
      else: # This condition executes if there exists a null value
        util_mat_cossim[a][b]=0 # It assigns zero if there exists a nan values for the associated cosine similarity utility matrix
        util_mat_adjcossim[a][b]=0 # It assigns zero if there exists a nan values for the associated adjusted cosine similarity utility matrix

"""***Calculating the score for similar items***"""

def item_sim(util_mat, a, b):
  return (np.dot(util_mat[:,a],util_mat[:,b])/(norm(util_mat[:,a])*norm(util_mat[:,b]))) # We return this similarity to top_sim_items function

"""***Obtaining movies that are atleast 50% similar***"""

def top_sim_items(util_mat,items,user_index,item_index):
  cor=0.05 # Similarity correlation factor
  top_items_list = []
  for a in range(len(items)): # Iterating through all the items/movies in the list
    if a!=item_index and util_mat[user_index][a] !=0: # Checks if the similarity is not equal to zero and if the item and item's index are not equal
      top_items_list.append((item_sim(util_mat,item_index,a),a)) # If the condition satisfies we find the item similarity associated and append it to the top items
  top_items_list.sort(reverse=True) # We sort it in descending order for holding the higher similarity items at the top
 
  # In the below evaluation we find atleast 50% similar items to the value of N from the items top list and check with the correlation factor
  result=[]
  for b in top_items_list:
    if b[0]>=cor: # If the similarity scores is greater than or equal to 50% then we append it to result list which has the final top items 
      result.append(b)
    else: # If the similarity score does not satisfy we just skip it
      continue 
  return result[:25] # As an additional point to the question I have reported the top 25 items which have 50% similarity and can provide higher predicted ratings

"""***Predicting Ratings associated for Cosine Similarity and Adjusted Cosine Similarity Matrices***"""

# Below is the function for predicting ratings for cosine similairty utility matrix
def predict_rating_cossim(util_mat,items,user_mean, user, item):
  use_index = users.index(user) # Storing the index of that particular user
  if item in items:
    ite_index = items.index(item) # Storing the index of that particular item
    topsim = top_sim_items(util_mat, items, use_index, ite_index) # Obtains the top elements that satisfy the correlation factor
    value1 = 0 # Stores the numerator value for the rating (Rxi) formula
    value2 = 0 # Stores the denominator value for the rating (Rxi) formula
    for a in topsim:
      value1 += a[0] * util_mat[use_index][a[1]] # Multplying each top similarity score with the utility matrix original rating
      value2 += a[0] # Stores the top similarity score
    rates = value1 / value2 # This gives the adjusted cosine similarity rating value (Rxi) for the associated user and customer 
    rates = rates 
  else:
    rates = user_mean[use_index] # If the rating does not exist we defaulty give the mean rating associated for that user
  return rates

# Below is the function for predicting ratings for adjusted cosine similairty utility matrix
def predict_rating_adjcossim(util_mat,items,user_mean, user, item):
  use_index = users.index(user) # Storing the index of that particular user
  if item in items:
    ite_index = items.index(item) # Storing the index of that particular item
    topsim = top_sim_items(util_mat, items, use_index, ite_index) # Obtains the top elements that satisfy the correlation factor
    value1 = 0 # Stores the numerator value for the rating (Rxi) formula
    value2 = 0 # Stores the denominator value for the rating (Rxi) formula
    for a in topsim:
      value1 += a[0] * util_mat[use_index][a[1]] # Multplying each top similarity score with the utility matrix original rating
      value2 += a[0] # Stores the top similarity score
    rates = value1 / value2 # This gives the adjusted cosine similarity rating value (Rxi) for the associated user and customer 
    rates = rates + user_mean[use_index] # The overall mean is added for the associated user index to the rating
  else:
    rates = user_mean[use_index] # If the rating does not exist we defaulty give the mean rating associated for that user
  return rates

"""***Rating Predictions and Model Evaluation with Test Data***"""

users_id = test_data["user_id"] # Stores the values of test data users
items_id = test_data["item_id"] # Stores the values of test data items/users
act_ratings = test_data["rating"].values # Stores the values of test data rating
cossim_predictions = [] # Stored the adjusted cosine similarity predicted ratings
for a in range(len(users_id)): # Iterates through each user of the test data and finds its rating from below function parsed
  cossim_predictions.append(predict_rating_cossim(util_mat_cossim,items,users_mean,users_id[i], items_id[i])) # Appends each users predicted rating to the list

users_id = test_data["user_id"] # Stores the values of test data users
items_id = test_data["item_id"] # Stores the values of test data items/users
act_ratings = test_data["rating"].values # Stores the values of test data rating
adjcossim_predictions = [] # Stores the adjusted cosine similarity predicted ratings
for i in range(len(users_id)): # Iterates through each user of the test data and finds its rating from below function parsed
  adjcossim_predictions.append(predict_rating_adjcossim(util_mat_adjcossim,items,users_mean,users_id[i], items_id[i])) # Appends each users predicted rating to the list

"""***RMSE Calculation for Cosine Similarity and Adjusted Cosine Similarity Predicted Ratings with the Actual Ratings***"""

def RMSE(y_actual, y_predicted): # This function calculates the associated RMSE value between actual and predicted ratings
  rms = sqrt(mean_squared_error(y_actual, y_predicted)) 
  return round(rms,4)
rmse_cos_sim = RMSE(act_ratings, cossim_predictions) # RMSE value is obtained on passing actual and predicted ratings to the function
print("RMSE obtained for Cosine Similarity is",rmse_cos_sim)

rmse_adj_cos_sim = RMSE(act_ratings, adjcossim_predictions) # RMSE value is obtained on passing actual and predicted ratings to the function
print("RMSE obtained for Adjusted Cosine Similarity is",rmse_adj_cos_sim)

"""***Comparing the RMSE Scores obtained for Cosine Similarity and Adjusted Cosine Similarity:***

a) RMSE for Cosine Similarity = 1.1743

b) RMSE for Adjusted Cosine Similarity = 0.8821

--> On observing the RMSE values obtained for both the similarity metrics it is clear that Adjusted Cosine Similarity has a lower root mean square error (RMSE) value compared to Cosine Similarity. 

--> So,it is clear that adjusted cosine similarity evaluates the model with accurate ratings since each user rating is subtracted from the average ratings for the pair of items provided.

--> Hence we conclude that Adjusted Cosine Similarity could be a better metric for evaluating models like Item-Item Collabrative Filtering.


"""