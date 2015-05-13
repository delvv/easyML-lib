package com.delvv.easymllib;

import java.io.BufferedWriter;
import java.io.EOFException;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.os.AsyncTask;
import android.os.Handler;
import android.util.Log;
import android.widget.Toast;


public class HttpFetcher extends AsyncTask<String, Void, String> {
	public final static String TAG = "HttpFetcher";
    String baseURI = "http://app.delvv.com:8082/";

    public static String GET_DATASOURCE = "get_datasource";
    public static String APPEND_DATA = "append_data";
    public static String GET_MODEL = "get_model";
    public static String TRAIN_MODEL = "train_model";
    public static String PREDICT = "predict";

	Context ctx;
	FetcherCallback cb;

	public HttpFetcher(Context ctx, FetcherCallback cb) {
		this.ctx = ctx;
		this.cb = cb;
        try {
            ApplicationInfo ai = ctx.getPackageManager().getApplicationInfo(ctx.getPackageName(), PackageManager.GET_META_DATA);
            baseURI = ai.metaData.getString("mlapi.url");
        } catch (Exception e) {

        }
	}

	public String convertStreamToString(java.io.InputStream is) {
		try {
			return new java.util.Scanner(is).useDelimiter("\\A").next();
		} catch (java.util.NoSuchElementException e) {
			return "";
		}
	}

	protected String doInBackground(String... args) {
		List<NameValuePair> params = new ArrayList<NameValuePair>();
		String result = null;
		String page = args[0];
		boolean doPost = false;
		boolean isRemote = false;
		URL url;
		if (page.equals(GET_DATASOURCE)) {
            params.add(new BasicNameValuePair("datasource_name", args[1]));
            for (int i=1;i<args.length;i++) {
                params.add(new BasicNameValuePair("col"+(i-1), args[i+1]));
            }
		}

        if (page.equals(APPEND_DATA)) {
            params.add(new BasicNameValuePair("datasource_name", args[1]));
            for (int i=1;i<args.length;i++) {
                params.add(new BasicNameValuePair("col"+(i-1), args[i+1]));
            }
        }


        if (page.equals(GET_MODEL)) {
            params.add(new BasicNameValuePair("model_name", args[1]));
            params.add(new BasicNameValuePair("model_type", args[2]));
            params.add(new BasicNameValuePair("datasource_name", args[3]));
            params.add(new BasicNameValuePair("start", args[4]));
            params.add(new BasicNameValuePair("end", args[5]));
            params.add(new BasicNameValuePair("model_params", args[6]));
        }

        if (page.equals(TRAIN_MODEL)) {
            params.add(new BasicNameValuePair("model_name", args[1]));
        }

        if (page.equals(PREDICT)) {
            params.add(new BasicNameValuePair("model_name", args[1]));
            for (int i=1;i<args.length;i++) {
                params.add(new BasicNameValuePair("col"+(i-1), args[i+1]));
            }
        }


        try {
			if (!doPost) {
				page = page+"?"+getQuery(params);
			}

			String reqURL = baseURI+page;

			if (isRemote) {
				reqURL = page;
			}

			Log.i("Mixpanel , HTTP", reqURL + " doPost: "+ doPost + " isRemote: "+ isRemote);

			url = new URL(reqURL);
			Log.d(TAG, "Calling "+reqURL);
			//			Log.d("Mixpanel", "Calling "+reqURL);

			boolean retry = false;
			// Open the connection
			URLConnection connection;
			HttpURLConnection httpConnection; 
			int responseCode;
			String cookie = LocalPreferences.getCookie(ctx);

			connection = url.openConnection();
			if (cookie!=null && !cookie.equals("")) {
				Log.d(TAG, "Opening connection, setting cookie string to "+cookie);
				connection.setRequestProperty("Cookie", cookie);
			}
			httpConnection = (HttpURLConnection)connection; 
			connection.setConnectTimeout(15000);

			if (doPost) {
				connection.setDoOutput(true);
				connection.setDoInput(true);
				OutputStream os = connection.getOutputStream();
				BufferedWriter writer = new BufferedWriter(
						new OutputStreamWriter(os, "UTF-8"));
				writer.write(getQuery(params));
				writer.close();
				os.close();
			}


			Log.d(TAG, "Getting response code");
			responseCode = httpConnection.getResponseCode(); 
			if (!isRemote) {
				List<String> cookies = httpConnection.getHeaderFields().get("Set-Cookie");
				Log.d(TAG, cookies.get(0));
				for (String c:cookies) {
					Log.d(TAG,"Got cookie: "+c);
					LocalPreferences.setCookie(ctx, c);
				}
			}


			if (responseCode == HttpURLConnection.HTTP_OK) { 
				Log.d(TAG, "Got HTTP_OK");
				InputStream in = httpConnection.getInputStream();
				result = convertStreamToString(in);
			}
		} catch (EOFException e) {
			Log.w("Fetcher", e);
			e.printStackTrace();
			Log.d("HttpFetcher", "postring result: " + result);
			return "CONNECTIONERROR";
		}catch (UnknownHostException e){
			Log.w("Fetcher", "UnknownHostException");
			e.printStackTrace();
			return "CONNECTIONERROR";
		} catch (Exception e) {
			e.printStackTrace();
			//Crashlytics.logException(e);
		}

		return result;
	}

	private String getQuery(List<NameValuePair> params) throws UnsupportedEncodingException
	{
		StringBuilder result = new StringBuilder();
		boolean first = true;

		for (NameValuePair pair : params)
		{
			if (first)
				first = false;
			else
				result.append("&");

			result.append(URLEncoder.encode(pair.getName(), "UTF-8"));
			result.append("=");
			result.append(URLEncoder.encode(pair.getValue(), "UTF-8"));
		}

		return result.toString();
	}

	protected void onPostExecute(String result) {

		Log.d("HttpFetcher", "postring result: " + result);

		if (result!=null && result.equals("CONNECTIONERROR")) {


		}else {
			if (this.cb!=null) {
				this.cb.onPostExecute(result);
			}
		}
	}

	public interface FetcherCallback {
		void onPostExecute(String result);
	}
}

