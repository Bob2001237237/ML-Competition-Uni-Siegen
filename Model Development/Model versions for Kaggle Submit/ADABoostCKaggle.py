from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
from sklearn.feature_selection import VarianceThreshold
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier



def Run(Xtrain,ytrain,Xtest):
    #make custom randomforest from whch the model starts
    Randomforrest = RandomForestClassifier(random_state=211, n_estimators=100, criterion='entropy', min_samples_split=2)

    ABC= AdaBoostClassifier( estimator= Randomforrest ,n_estimators=100, random_state=5591, learning_rate=1, algorithm='SAMME.R')
    ABC.fit(Xtrain,ytrain)
    pred = ABC.predict(Xtest)

    return pred
#read csv
features = pd.read_csv('train_features.csv')
labels = pd.read_csv('train_label.csv')
testFeatures =pd.read_csv('test_features.csv')


#drop the id
features = features.drop(['Id'], axis=1)
labels = labels.drop(['Id'], axis=1)
testFeatures.drop(inplace=True, labels=['Id','feature_2'], axis=1)

#basic pre prosessing
#features.drop(inplace=True, labels= ['feature_2',], axis=1)




#convert to numpyarray
features=features.to_numpy()
labels=labels.to_numpy().flatten()

#basic preprossesing
selectorVariance= VarianceThreshold()
features = selectorVariance.fit_transform(features)
#for what ever reason this decraees the performance by arround 2.6%
selectorVariance= VarianceThreshold()
features = selectorVariance.fit_transform(features)

result = Run(features,labels,testFeatures)
#export as csv file
#loop that makes the id for the predicited valus
idarr = np.array([])
for i in range(len(result)):
   idarr= np.append(idarr, i)
#make pd dataframe with id as axis 0 and the rusulst as label 1 with the results
return_value=pd.DataFrame({'Id': idarr, 'label': result})
return_value=return_value.astype(int)
print(return_value)
#save it as file
return_value.to_csv('ABC5.csv', columns=['Id', 'label'], index=False)