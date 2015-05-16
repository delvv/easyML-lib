import recsys.algorithm
from recsys.algorithm.factorize import SVD
import os

recsys.algorithm.VERBOSE = True
data_dir = 'data/'
model_dir = 'model_data/'

models = {}
model_data = {}

def get_model(model_name,datasource_name,start,end,model_params):
    if not model_name in model_data:
        model_data[model_name] = (datasource_name,start,end,model_params) 
    if not os.path.exists(model_dir+model_name):
        #initialize model with new data
        svd = SVD()
        svd.load_data(filename=data_dir+datasource_name+'.csv', sep=',', format={'col':0, 'row':1, 'value':2, 'ids': int})
        models[model_name] = svd
    else:
        if not model_name in models:
            models[model_name] = SVD(filename=model_dir+model_name)


def train_model(model_name):
    #datasource_name = model_data[model_name][0]
    svd = models[model_name]
    k = 100    
    try:
        os.makedirs(model_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile=model_dir+model_name)

def predict(model_name,item_id,user_id):
    MIN_RATING = 0.0
    MAX_RATING = 5.0
    return models[model_name].predict(item_id,user_id,MIN_RATING,MAX_RATING)

def get_similar(model_name,item_id):
    return models[model_name].similar(item_id)

def get_recommended(model_name,user_id):
    return models[model_name].recommend(user_id, is_row=False)
    
