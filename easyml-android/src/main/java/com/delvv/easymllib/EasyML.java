package com.delvv.easymllib;


import android.content.Context;

public class EasyML {
    Context context;

    public EasyML(Context context) {
        this.context = context;
    }

    public int getDataSource(String data_source_name, String... vars) {
        HttpFetcher hf = new HttpFetcher(context, new HttpFetcher.FetcherCallback() {
            @Override
            public void onPostExecute(String result) {

            }
        });
        try {
            String[] args = new String[vars.length+1];
            args[0] = HttpFetcher.GET_DATASOURCE;
            args[1] = data_source_name;
            int i = 2;
            for (String var:vars) {
                args[i++] = var;
            }
            int result = Integer.parseInt(hf.execute(args).get());
            return result;
        } catch (Exception e) {
            return -1;
        }
    }

    public int appendData(String data_source_name, String... sample) {
        HttpFetcher hf = new HttpFetcher(context, new HttpFetcher.FetcherCallback() {
            @Override
            public void onPostExecute(String result) {

            }
        });
        try {
            String[] args = new String[sample.length+1];
            args[0] = HttpFetcher.APPEND_DATA;
            args[1] = data_source_name;
            int i = 2;
            for (String var:sample) {
                args[i++] = var;
            }
            int result = Integer.parseInt(hf.execute(args).get());
            return result;
        } catch (Exception e) {
            return -1;
        }

    }

    public DataSet createDataSet(String data_source_name) {
        DataSet ds = new DataSet(data_source_name);
        ds.start = -1;
        ds.end = -1;
        return ds;
    }


    public DataSet createDataSet(String data_source_name, int start, int end) {
        DataSet ds = new DataSet(data_source_name);
        ds.start = start;
        ds.end = end;
        return ds;
    }

    public Model getModel(String modelName, String modelType, String data_source_name) {
        if (modelType.equalsIgnoreCase("recommender")) {
            Model m = new RecommenderModel(context, data_source_name, modelName);
            m.initialize();
            return m;
        }
        else if (modelType.equalsIgnoreCase("classification")) {
            Model m = new ClassificationModel(context, data_source_name, modelName);
            m.initialize();
            return m;
        }
        else if (modelType.equalsIgnoreCase("numeric")) {
            Model m = new NumericModel(context, data_source_name,  modelName);
            m.initialize();
            return m;
        }
        else return null;
    }


}
