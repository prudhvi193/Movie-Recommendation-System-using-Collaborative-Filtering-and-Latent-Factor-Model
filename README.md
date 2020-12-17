# Movie Recommendation System implemented using Collaborative Filtering and Latent Factor Models

This project was developed as part of my Master's Course Study in Algorithms and Methods of Big Data Analytics.

Authors: Prudhviraj Sheela, Aman Masipeddi

The main motive of this project is to develop a movie based recommender system using two methods. They are:

a)Item-Item Collaborative Filtering: It is a method of making automatic predictions (filtering) about the interests of a user by collecting preferences or taste information from many users (collaborating).

b)Latent Factor Model using Stochastic Gradient Descent: It means that there exist an unknown low-dimensional representation of users and items where user-item affinity can be modeled accurately.

In the models that are developed we evaluate the Root Mean Sqaure Error (RMSE) score for measuring the performances.

IDE Used: Google Colab Notebook

Language Used: Python

Description about the files:

1)Project-4.pdf: This file contains the steps associated for developing the application and also the intermediate output formats for executing the program.

2)Project-4 Guidelines.pptx: This Powerpoint slide consists on how to 

3)CF.py/CF.ipynb: Python program for collaborative filtering which involves steps associated for finding the similarity metric, calculating similarities of multiple movies using both cosine similarity and adjusted cosine similarity and the final step includes prediciting the rating of given movie 'i' for user 'x'.

4)LF.py/LF.ipynb: Python program for implementing a latent factor model using Stochastic Gradient Descent by optimizing both the matrices 'P' and 'Q' and then we measure its performane by calculating the Root Mean Square Error

5)LF+Biases.py/LF+Biases.ipynb: Python program for implementing Latent Factor Model + Biases model using Stochastic Gradient Descent by optimizing matrices "P for Users", "Q for Items" ,"Biases for User", "Biases for Item" and then we measure its performance by calculating the Root Mean Square Error

6)test_dataset.csv: This CSV file contains test data information about user id and its correspoding movie/item id, rating and movie name.

7)training_dataset.csv: This CSV file contains the main training dataset about user id and its corresponding movie/item id, rating and movie name. This training dataset is used as a reference in evaluating root mean square error.

Output Files: The explanation about the output generated is available in "CF.ipynb" , "LF.ipynb" and "LF+Biases.ipynb" python file which explains clearly on how is the end result obtained. 



