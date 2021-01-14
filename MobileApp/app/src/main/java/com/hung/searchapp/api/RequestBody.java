package com.hung.searchapp.api;

import android.util.Base64;

import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class RequestBody {
    @SerializedName("audio")
    @Expose
    public String audioData ;
    public RequestBody(byte[] bytes){
        this.audioData = Base64.encodeToString(bytes, Base64.NO_WRAP);
    }
}
