package com.hung.searchapp.core;

import android.app.Activity;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.os.Build;
import android.util.Log;

import androidx.annotation.RequiresApi;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class Recorder {
    private static String fileName = null;
    private MediaRecorder recorder = null;

    public Recorder(Activity activity){
        fileName =  activity.getExternalCacheDir().getAbsolutePath();
        fileName += "/audiorecordtest.3gp";
    }

    public void startRecording() {
        recorder = new MediaRecorder();
        recorder.setAudioSource(MediaRecorder.AudioSource.MIC);
        recorder.setOutputFormat(MediaRecorder.OutputFormat.THREE_GPP);
        recorder.setOutputFile(fileName);
        recorder.setAudioEncoder(MediaRecorder.AudioEncoder.AMR_NB);
        try {
            recorder.prepare();
        } catch (IOException e) {
            Log.e("failrecord", "prepare() failed");
        }
        recorder.start();
    }

    public void stopRecording() {
        recorder.stop();
        recorder.release();
        recorder = null;
    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    public byte[] search() {
        MediaPlayer player = new MediaPlayer();
        try {
            return Files.readAllBytes(Paths.get(fileName));
        } catch (IOException e) {
            Log.e("", "prepare() failed");
        }
        return null;
    }

}
