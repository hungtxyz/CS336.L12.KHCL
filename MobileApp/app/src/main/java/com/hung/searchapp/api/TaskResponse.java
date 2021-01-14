package com.hung.searchapp.api;


import com.google.gson.annotations.Expose;
import com.google.gson.annotations.SerializedName;

public class TaskResponse {
    @SerializedName("song_name")
    @Expose
    public String songName;

    @SerializedName("status")
    @Expose
    public Boolean status;

    @SerializedName("task_id")
    @Expose
    public String taskId;

    public TaskResponse() {

    }

    public String getSongName() {
        return this.songName;
    }

    public TaskStatus getStatus() {
        if (!this.status) {
            return TaskStatus.PROCESSING;
        } else {
            return TaskStatus.SUCCESS;
        }
    }

    public String getTaskId() {
        return this.taskId;
    }

    public enum TaskStatus {
        PROCESSING,
        SUCCESS
    }


}
