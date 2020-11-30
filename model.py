from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

import statsmodels.api as sm
import pandas as pd

games_final = pd.read_csv('data/master_games_cleaned.csv')

games_final = games_final.fillna(0)

X_set = games_final.loc[:, games_final.columns != 'did_home_win']
y_set = games_final.loc[:, games_final.columns == 'did_home_win']

X_scaled = preprocessing.scale(X_set)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_set, test_size=0.3, random_state=0)

logreg = LogisticRegression()
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))