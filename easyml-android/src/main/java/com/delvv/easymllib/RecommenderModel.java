package com.delvv.easymllib;

import android.content.Context;

import java.util.Arrays;

/**
 * Created by raefer on 5/12/15.
 */
public class RecommenderModel implements Model {

    Context context;
    String data_source_name;
    String modelName;
    int modelId;

    public RecommenderModel(Context context, String data_source_name, String modelName) {
        this.data_source_name = data_source_name;
        this.modelName = modelName;
        this.context = context;
    }

    public int initialize() {
        String params = "";
        HttpFetcher hf = new HttpFetcher(context, new HttpFetcher.FetcherCallback() {
            @Override
            public void onPostExecute(String result) {

            }
        });
        try {
            int result = Integer.parseInt(hf.execute(HttpFetcher.GET_MODEL, modelName, "itemRecommender", data_source_name, params).get());
            modelId = result;
            return result;
        } catch (Exception e) {
            return -1;
        }
    }

    public Model getLocalModel() {
        return null;
    }

    public void train(DataSet ds) {
        HttpFetcher hf = new HttpFetcher(context, new HttpFetcher.FetcherCallback() {
            @Override
            public void onPostExecute(String result) {

            }
        });
        try {
            String result = hf.execute(HttpFetcher.TRAIN_MODEL, modelName, ""+ds.start, ""+ds.end).get();
        } catch (Exception e) {
            //log
        }
    }

    public String predict(String[] parameters) {
        HttpFetcher hf = new HttpFetcher(context, new HttpFetcher.FetcherCallback() {
            @Override
            public void onPostExecute(String result) {

            }
        });
        try {
            String[] args = concat(new String[] {HttpFetcher.PREDICT, modelName}, parameters);
            String result = hf.execute(args).get();
            return result;
        } catch (Exception e) {
            return "ERROR";
        }
    }

    public static <T> T[] concat(T[] first, T[] second) {
        T[] result = Arrays.copyOf(first, first.length + second.length);
        System.arraycopy(second, 0, result, first.length, second.length);
        return result;
    }
}