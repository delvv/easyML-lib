package com.delvv.easymllib;

/**
 * Created by raefer on 5/3/15.
 */
public class DataSet {

    String dataSourceName;
    int start;
    int end;

    DataSet(String dsName) {
        dataSourceName = dsName;
    }

    public int getNumValues() {
        return (end-start+1);
    }

    public DataSet getSubset(int start, int end) {
        DataSet ds = new DataSet(dataSourceName);
        ds.start = start;
        ds.end = end;
        return ds;
    }
}
