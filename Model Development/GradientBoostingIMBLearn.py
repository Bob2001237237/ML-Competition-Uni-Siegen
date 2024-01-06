from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, confusion_matrix
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, LeaveOneOut
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import scale
from joblib import dump, load
from sklearn.utils import resample
from imblearn.under_sampling import ClusterCentroids,CondensedNearestNeighbour, EditedNearestNeighbours, RepeatedEditedNearestNeighbours,AllKNN, InstanceHardnessThreshold, NearMiss, NeighbourhoodCleaningRule, OneSidedSelection
from imblearn.combine import SMOTEENN
from imblearn.over_sampling import RandomOverSampler, SMOTENC,ADASYN,SVMSMOTE,KMeansSMOTE,BorderlineSMOTE
def Run(Xtrain,ytrain,Xtest,ytest):


    # scale
    #scale(X)

    #define model parameters
    GBmodel= GradientBoostingClassifier(n_estimators=100,learning_rate=0.1,max_depth=10, random_state=211,verbose=False,
                                        loss='log_loss', criterion='friedman_mse')


    # split the data
    #Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.1, random_state=211)
    #scale(Xtrain)
    #scale(Xtest)
    GBmodel.fit(Xtrain, ytrain)
    print(GBmodel.feature_importances_)


    #make Prediction
    pred =GBmodel.predict(Xtest)
    tn, fp, fn, tp = confusion_matrix(ytest, pred).ravel()
    print('tn: ', tn, 'tp: ', tp, 'fn: ', fn, 'fp: ', fp)
    #1 dump(GBmodel, 'Model versions for Kaggle Submit/GBmodel6_wo_f2_downsamp_IMBLearn_NearMiss')
    score = f1_score(ytest, pred, average='macro')
    scores = cross_val_score(GBmodel, Xtrain, ytrain, cv=5, scoring='f1_macro')
    print(scores)
    print("%0.2f F1-Macro with a standard deviation of %0.2f" % (scores.mean(), scores.std()))

    return score

#read csv
features = pd.read_csv('train_features.csv')
labels = pd.read_csv('train_label.csv')


#drop the id
features = features.drop(['Id'], axis=1)
labels = labels.drop(['Id'], axis=1)


#drop features without information

features.drop(['feature_2'], axis=1, inplace=True)

#resample using imbalanced learn
#cluster removal

'''cc = ClusterCentroids(random_state=42)
features, labels = cc.fit_resample(features, labels)'''
labels=labels.to_numpy().flatten()

features, test_features, labels ,test_labels = train_test_split(features,labels, test_size=0.2, random_state=213)
#up and down sampling

bsm = BorderlineSMOTE(random_state=42)
X_res, y_res = bsm.fit_resample(features, labels)
features =X_res
labels = y_res
labels = pd.DataFrame(labels)

print(features)
print('1: ', labels.value_counts()[1])
print('0: ', labels.value_counts()[0])
print(np.unique(test_labels, return_counts=True))



#convert to numpyarray
features=features.to_numpy()
labels=labels.to_numpy().flatten()


#print(Run(features, labels))
print('validation score: ', Run(features, labels, test_features, test_labels))