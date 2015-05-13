import recsys.algorithm
from recsys.algorithm.factorize import SVD

recsys.algorithm.VERBOSE = True
data_dir = 'data/'
model_dir = 'model_data/'

models = {}
model_data = {}

def get_model(model_name,datasource_name,start,end,model_params):
    if not os.path.exists(model_dir+model_name):
        #do something
        pass
    else:
        if not model_name in models:
            models[model_name] = SVD(filename=model_dir+model_name)
            model_data[model_name] = (datasource_name,start,end,model_params)

def train_model(model_name):
    datasource_name = model_data[model_name][0]
    k = 100    
    svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True, post_normalize=True, savefile=model_dir+datasource_name)    

def predict(model_name,item_id,user_id):
    MIN_RATING = 0.0
    MAX_RATING = 5.0
    return models[model_name].predict(item_id,user_id,MIN_RATING,MAX_RATING)

def get_similar(model_name,item_id):
    return models[model_name].similar(item_id)

def get_recommended(model_name,user_id):
    return models[model_name].recommend(user_id, is_row=False)
    
