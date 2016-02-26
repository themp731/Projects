import pandas as pd
import json
import itertools
import seaborn as sb
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from os import system 

data = pd.read_csv("assets/dataset/stumbleupon.tsv", sep='\t')
data['title'] = data.boilerplate.map(lambda x: json.loads(x).get('title', ''))
data['body'] = data.boilerplate.map(lambda x: json.loads(x).get('body', ''))
data.head()

#Getting only non-string data
data_iter = data[['alchemy_category_score','avglinksize','commonlinkratio_1'\
                  ,'commonlinkratio_2','commonlinkratio_3','commonlinkratio_4','compression_ratio','embed_ratio',\
                  'framebased','frameTagRatio','hasDomainLink','html_ratio','image_ratio','is_news',
                  'lengthyLinkDomain','linkwordscore', 'news_front_page','non_markup_alphanum_characters',\
                  'numberOfLinks','numwords_in_url','parametrizedLinkRatio','spelling_errors_ratio','label']]
data_iter["is_news"][data_iter["is_news"]=="?"]=0
data_iter["alchemy_category_score"][data_iter["alchemy_category_score"]=="?"]=0
data_iter["news_front_page"][data_iter["news_front_page"]=="?"]=0
data_cols=list(data_iter.columns)
#I can do the full length of tags, but it will take forever, so I'm being lazy and only doing a few.
combo_len = range(1,3)

#Creating a combination of the different features of different lengths
feature_list = []
for j in combo_len:
    for i in itertools.combinations(data_cols[:-1],j):
        feature_list.append(list(i))

#Get the model from list we provide 
def make_model(features):
    model = DecisionTreeClassifier()
    X = data_iter[features].dropna()
    y = data_iter['label']
    fitted = model.fit(X,y)
    score = get_score(fitted,X,y,features)
    return score

#Get the Score
def get_score(model,X,y,features):
    scores=cross_val_score(model, X, y, scoring='roc_auc', cv=5)
    #print "For the variables: ",features
    #print "Average AUC: ",scores.mean()
    #print "---------------------"
    return scores.mean()

def get_vars(feat_list):
	topscore=0
	best_feat=0
	for k in feat_list:
		new_score = make_model(k)
		if new_score > topscore:
			topscore = new_score
			best_feat = k
	print "The Best Score Is:  ",topscore
	print "With variables: ",best_feat
	return best_feat

best_X = data_iter[get_vars(feature_list)]
best_y = data_iter['label']
model = DecisionTreeClassifier(min_samples_leaf=5,max_depth=6,criterion="gini")
best_model = model.fit(best_X,best_y)
get_score(best_model,best_X,best_y,best_feat)

def build_tree_image(model,X):
    dotfile = open("tree.dot", 'w')
    export_graphviz(model,
                              out_file = dotfile,
                              feature_names = X.columns)
    dotfile.close()
    system("dot -Tpng tree.dot -o tree.png")
    
build_tree_image(best_model,best_X)