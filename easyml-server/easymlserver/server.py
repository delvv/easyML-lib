from flask import Flask, request
import os, csv
import json
import errno
from easymlserver import itemRecommender

app = Flask(__name__)

data_dir = 'data/'
model_dir = 'model_data/'

model_data = {}

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

@app.route('/get_datasource')
def api_get_datasource():
    try: 
        os.makedirs(data_dir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    dsname = data_dir+request.args['datasource_name']
    i=1
    args = []
    while 'col'+str(i) in request.args:
        args.append(request.args['col'+str(i)])
        i+=1
    app.logger.debug(args)
    if (os.path.exists(dsname+'.csv')):
        #already exists, should read and verify column names
        return str(file_len(dsname+'.csv')-1)
    else:
        #now create csv file with fields col0..colN
        with open(dsname+'.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(args)
            csvfile.flush()
        return str(0)


@app.route('/append_data')
def api_append_data():
    try:
        try: 
            os.makedirs(data_dir)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

        dsname = data_dir+request.args['datasource_name']
        args = []
        i = 1
        while 'col'+str(i) in request.args:
            args.append(request.args['col'+str(i)])
            i+=1
        with open(dsname+'.csv', 'a') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                   quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(args)
            csvfile.flush()
            return json.dumps({'result':'success'})
    except:
        return json.dumps({'result':'failed to append data'})

@app.route('/get_model')
def api_get_model():
    model_name = request.args['model_name']
    model_type = request.args['model_type']
    datasource_name = request.args['datasource_name']
    start = request.args['start']
    end = request.args['end']
    model_params = request.args['model_params']
    if (model_type=='itemRecommender'):
        itemRecommender.get_model(model_name,datasource_name,start,end,model_params)
        model_data[model_name] = (model_type,datasource_name,start,end,model_params)
    return json.dumps({'result':'success'})

@app.route('/train_model')
def api_train_model():
    model_name = request.args['model_name']
    model_type = model_data[model_name][0]
    if (model_type=='itemRecommender'):
        itemRecommender.train_model(model_name)
    return json.dumps({'result':'success'})

@app.route('/predict')
def api_predict():
    model_name = request.args['model_name']
    model_type = model_data[model_name][0]
    if (model_type=='itemRecommender'):
        args = []
        i = 1
        while 'col'+str(i) in request.args:
            args.append(request.args['col'+str(i)])
            i+=1
        if len(args)==2:
            item_id = int(args[0])
            user_id = int(args[1])
            return json.dumps(itemRecommender.predict(model_name,item_id,user_id))
        if len(args)==1:
            isUser = False
            id = args[0]
            if id[0]=='u':
                isUser = True
                id = int(id[1:])
            else:
                id = int(id)
            if not isUser:
                return json.dumps(itemRecommender.get_similar(model_name,id))
            else:
                return json.dumps(itemRecommender.get_recommended(model_name,id))
                

@app.route('/predict_batch')
def api_predict_batch():
    return json.dumps({'error':'Not yet implemented'})

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()
