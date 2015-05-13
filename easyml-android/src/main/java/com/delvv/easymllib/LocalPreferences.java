package com.delvv.easymllib;

import android.content.Context;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.preference.PreferenceManager;

public class LocalPreferences
{

    static final String PREF_COOKIE = "cookie";

    public static void setCookie(Context ctx, String cookie)
    {
        Editor editor = getSharedPreferences(ctx).edit();
        editor.putString(PREF_COOKIE,cookie);
        editor.commit();
    }

    public static String getCookie(Context ctx)
    {
        return getSharedPreferences(ctx).getString(PREF_COOKIE,"");
    }

    public static SharedPreferences getSharedPreferences(Context ctx) 
    {
        return PreferenceManager.getDefaultSharedPreferences(ctx);
    }

}