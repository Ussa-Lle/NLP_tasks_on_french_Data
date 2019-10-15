import pandas as pd 
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier 
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Two simple ways to classify texts using features that we extracted with the sdcript "Extacting_features.py"
# and the 2nd way by only vectorizing the texts 
# ____________________________________________________________________________________
#SVM with extracetd features 

# _____________________________________________________________________________________


#CSV file contains a "Text" column and other columns as features, and the "text_type column is the class"
data=pd.read_csv("data_Corpus.csv",sep=",",encoding='utf-8')

y=data.text_type
X=data.drop("text_type",axis=1)
X=X.drop("Text",axis=1)


X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2) 


clf = svm.SVC(gamma='scale')
clf.fit(X_train,y_train)

print(clf.score(X_test,y_test))

joblib.dump(clf, 'saved_model_SVM.pkl') # a simple way to save model espacially if your model took a lot of time to train 
 




#____________________________________________________________________________________
#RandomForest by vectorizing texts

# ______________________________________________________________________________________

# CVS file that contains two columns texts and the class 

texts = pd.read_csv("E:\\Project_OOP\\data_norm_.csv", sep=",", names=['Text', 'text_type'])


X = texts.Text
y = texts.text_type




X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2) 

vect = CountVectorizer()

vect.fit(X_train)
X_train_dtm = vect.transform(X_train)

X_train_dtm = vect.fit_transform(X_train)

X_test_dtm = vect.transform(X_test)

clf = RandomForestClassifier (n_estimators=50)


clf.fit(X_train_dtm, y_train)


y_pred_class = clf.predict(X_test_dtm)

# print(y_pred_class)

print(metrics.accuracy_score(y_test, y_pred_class))
print(metrics.confusion_matrix(y_test, y_pred_class))

