# 💻 Shopping #
Write an AI to predict whether online shopping customers will complete a purchase.
```
$ python shopping.py shopping.csv
Correct: 4088
Incorrect: 844
True Positive Rate: 41.02%
True Negative Rate: 90.55%
```
## 🔸 Understanding ##
First, open up `shopping.csv`, the data set provided to you for this project. There are about 12,000 user sessions represented in this spreadsheet: represented as one row for each user session. The first six columns measure the different types of pages users have visited in the session: the `Administrative`, `Informational`, and `ProductRelated` columns measure how many of those types of pages the user visited, and their corresponding `_Duration` columns measure how much time the user spent on any of those pages. The `BounceRates`, `ExitRates`, and `PageValues` columns measure information from Google Analytics about the page the user visited. `SpecialDay` is a value that measures how close the date of the user’s session is to a special day (like Valentine’s Day or Mother’s Day). `Month` is an abbreviation of the month the user visited. `OperatingSystems`, `Browser`, `Region`, and `TrafficType` are all integers describing information about the user themself. `VisitorType` will take on the value `Returning_Visitor` for returning visitors and some other string value for non-returning visitors. `Weekend` is `TRUE` or `FALSE` depending on whether or not the user is visiting on a weekend.

Perhaps the most important column, though, is the last one: the `Revenue` column. This is the column that indicates whether the user ultimately made a purchase or not: `TRUE` if they did, `FALSE` if they didn’t. This is the column that we’d like to learn to predict (the “label”), based on the values for all of the other columns (the “evidence”). 

Next, take a look at `shopping.py`. The main function loads data from a CSV spreadsheet by calling the `load_data` function and splits the data into a training and testing set. The `train_model` function is then called to train a machine learning model on the training data. Then, the model is used to make predictions on the testing data set. Finally, the `evaluate` function determines the sensitivity and specificity of the model, before the results are ultimately printed to the terminal.

## 🟢 Acknowledgements ##
Data set provided by [Sakar, C.O., Polat, S.O., Katircioglu, M. et al. Neural Comput & Applic (2018)](https://link.springer.com/article/10.1007/s00521-018-3523-0)
