package com.delvv.easymllib;

/**
 * Created by raefer on 5/3/15.
 */
public interface Model {

    public int initialize();
    public void train(DataSet ds);

}
