package com.hung.searchapp.api;

import retrofit2.Call;
import retrofit2.http.Body;
import retrofit2.http.GET;
import retrofit2.http.POST;
import retrofit2.http.Query;

public interface APIService {
    @POST("audio/sendaudio")
    Call<TaskResponse> uploadAudio(@Body RequestBody request);

    @GET("audio/request4result")
    Call<TaskResponse> getTaskStatus(@Query("id") String taskId);

}

