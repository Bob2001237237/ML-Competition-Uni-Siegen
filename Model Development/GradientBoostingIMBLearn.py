from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import scale
from joblib import dump, load
from sklearn.utils import resample, compute_sample_weight
from imblearn.under_sampling import ClusterCentroids,CondensedNearestNeighbour, EditedNearestNeighbours, RepeatedEditedNearestNeighbours,AllKNN, InstanceHardnessThreshold, NearMiss, NeighbourhoodCleaningRule, OneSidedSelection
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import RandomOverSampler, SMOTENC,ADASYN,SVMSMOTE,KMeansSMOTE,BorderlineSMOTE, SMOTE
import itertools
def Run(Xtrain,ytrain,Xtest,ytest,weights):

    #define model parameters
    GBmodel = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=10, random_state=211,
                                         verbose=False,
                                         loss='log_loss', criterion='friedman_mse')
    print(weights)

    '''for i in range(len(weights)):
        if (weights[i] > 1):
            weights[i] = weights[i] * 2'''

    used_weight = []
    for i in ytrain:
        if ytrain[i] is 0:
            used_weight.append(weights[1])
        else:
            used_weight.append((weights[0]))
    # split the data
    GBmodel.fit(Xtrain, ytrain, used_weight)
    # split the data
    GBmodel.fit(Xtrain, ytrain, used_weight)

    pred = GBmodel.predict(Xtest)
    #make Prediction
    #1 dump(GBmodel, 'Model versions for Kaggle Submit/GBmodel6_wo_f2_downsamp_IMBLearn_NearMiss')
    scores = cross_val_score(GBmodel, Xtrain, ytrain, cv=5, scoring='f1_macro', n_jobs=-1)
    #print(scores)
    print('scores: ', scores,"%0.2f F1-Macro with a standard deviation of %0.2f" % (scores.mean(), scores.std()))
    print('f1_macro scroe on test data',f1_score(pred,ytest, average='macro'))


#read csv
features = pd.read_csv('train_features.csv')
labels = pd.read_csv('train_label.csv')

#drop the id
features = features.drop(['Id'], axis=1)
labels = labels.drop(['Id'], axis=1)


#drop features without information

features.drop(['feature_2'], axis=1, inplace=True)


features ,Xtest, labels, ytest =train_test_split(features,labels, test_size=0.2, random_state=221)


#resample using imbalanced learn
labels=labels.to_numpy().flatten()

#up and down sampling
weights = compute_sample_weight(class_weight='balanced', y=labels)

smo = SMOTE(random_state=42, n_jobs=-1)
X_res, y_res = smo.fit_resample(features, labels)
features =X_res
labels = y_res
labels = pd.DataFrame(labels)



labels = labels.to_numpy().flatten()

Run(features, labels,Xtest,ytest, weights)
