package com.hung.searchapp;

import androidx.annotation.NonNull;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.hung.searchapp.api.APIUtils;
import com.hung.searchapp.api.RequestBody;
import com.hung.searchapp.api.TaskResponse;
import com.hung.searchapp.core.Recorder;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class MainActivity extends AppCompatActivity {
    enum Action{
        RECORD,
        STOP,
        SEARCH,
    }
    private static final int REQUEST_RECORD_AUDIO_PERMISSION = 200;
    private boolean permissionToRecordAccepted = false;
    private final String [] permissions = {Manifest.permission.RECORD_AUDIO};
    Action btnAction = Action.RECORD;
    private String serverTaskId = null;
    private static final String TAG = "MaiNActivity";
    private final Handler mHandler = new Handler(Looper.getMainLooper());
    TextView textView = null;
    TextView text = null;
    MainView mainView = null;
    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == REQUEST_RECORD_AUDIO_PERMISSION) {
            permissionToRecordAccepted = grantResults[0] == PackageManager.PERMISSION_GRANTED;
        }
        if (!permissionToRecordAccepted ) finish();

    }


    static class MainView{
        enum BtnStatus{
            RECORD,
            STOP,
            SEARCH,
        }
        FloatingActionButton recordButton;
        RelativeLayout loadingPanel;
        TextView textView;
        ImageView logoView;
        MainView(FloatingActionButton  btn, RelativeLayout layout, TextView textView, ImageView imageView) {
            this.recordButton = btn;
            this.loadingPanel = layout;
            this.textView = textView;
            this.logoView = imageView;

        }

        public void changeBtn(BtnStatus step){
            switch (step){
                case STOP:
                    this.recordButton.setImageResource(R.drawable.ic_baseline_stop_24);
                    break;
                case RECORD:
                    this.recordButton.setImageResource(R.drawable.ic_baseline_fiber_manual_record_24);
                    break;
                case SEARCH:
                    this.recordButton.setImageResource(R.drawable.ic_baseline_search_24);
                    break;
                default:
                    break;
            }
        }
        public void hideLoadingPanel(boolean hide){
            if(hide){
                loadingPanel.setVisibility(View.GONE);
                recordButton.setClickable(true);
            }
            else {
                loadingPanel.setVisibility(View.VISIBLE);
                recordButton.setClickable(false);
            }
        }
        public void blurBackground(boolean isBlur){
            if (isBlur) {
                logoView.setAlpha((float) 0.2);
                recordButton.setAlpha((float) 0.2);
            }
            else{
                logoView.setAlpha((float) 1.0);
                recordButton.setAlpha((float) 1.0);
            }
        }

    }

    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // app code
        textView = findViewById(R.id.nameView);
        text = findViewById(R.id.text);

        View linearLayout = findViewById(R.id.linearLayout);
        ImageView imageView = findViewById(R.id.imageView);

        FloatingActionButton button = findViewById(R.id.recordBtn);

        ActivityCompat.requestPermissions(this, permissions, REQUEST_RECORD_AUDIO_PERMISSION);
        mainView= new MainView(
                button,
                findViewById(R.id.loadingPanel),
                textView,
                imageView);


        Recorder recorder = new Recorder(this);

        mainView.recordButton.setOnClickListener((v)->{
            switch (btnAction){
                case RECORD:
                    textView.setText("");
                    MainActivity.this.text.setVisibility(View.GONE);
                    recorder.startRecording();
                    mainView.changeBtn(MainView.BtnStatus.STOP);
                    btnAction = Action.STOP;
                    break;
                case STOP:
                    recorder.stopRecording();
                    mainView.changeBtn(MainView.BtnStatus.SEARCH);
                    btnAction = Action.SEARCH;
                    break;
                case SEARCH:
                    mainView.hideLoadingPanel(false);
                    mainView.blurBackground(true);
                    byte[] bytes = recorder.search();
                    uploadAudio(bytes, mainView);
                    mainView.changeBtn(MainView.BtnStatus.RECORD);
                    btnAction = Action.RECORD;
                    break;
            }
        });
    }
    private void uploadAudio(byte[] bytes, MainView mainView) {
        RequestBody request = new RequestBody(bytes);
        APIUtils.getAPIService().uploadAudio(request).enqueue(new Callback<TaskResponse>() {
            @Override
            public void onResponse(Call<TaskResponse> call, Response<TaskResponse> response) {
                TaskResponse taskResponse = response.body();
                if (taskResponse != null) {
                    serverTaskId = taskResponse.getTaskId();
//                    mHandler.post(MainActivity.this::checkStatus);




                    Log.d("--------------", "taskID = " + serverTaskId);
                    mHandler.post(MainActivity.this::checkStatus);
                }
            }

            @Override
            public void onFailure(Call<TaskResponse> call, Throwable t) {
                Log.d("--------------", String.valueOf(t));
            }
        });
    }

    private void checkStatus() {
        if (isFinishing() || isDestroyed() || serverTaskId == null) {
            return;
        }

        Log.i(TAG, "Checking status...");

        APIUtils.getAPIService().getTaskStatus(serverTaskId).enqueue(new Callback<TaskResponse>() {
            @Override
            public void onResponse(Call<TaskResponse> call, Response<TaskResponse> response) {
                if (isFinishing() || isDestroyed()) {
                    return;
                }

                TaskResponse taskResponse = response.body();
                if (taskResponse != null) {
                    Log.i(TAG, "Success = " + (taskResponse.getStatus() != TaskResponse.TaskStatus.PROCESSING));


                    if (taskResponse.getStatus() == TaskResponse.TaskStatus.PROCESSING) {
                        mHandler.postDelayed(MainActivity.this::checkStatus, 1000);


                    } else {

                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                MainActivity.this.mainView.blurBackground(false);
                                MainActivity.this.mainView.hideLoadingPanel(true);
                                MainActivity.this.text.setVisibility(View.VISIBLE);
                                Log.d(TAG+"songname is", taskResponse.getSongName());
                                MainActivity.this.textView.setText(taskResponse.getSongName());
                            }
                        });
                    }
                }
            }

            @Override
            public void onFailure(Call<TaskResponse> call, Throwable t) {
                //TODO: What if error occurs
                Log.e(TAG, t.getLocalizedMessage());
                mHandler.postDelayed(MainActivity.this::checkStatus, 1000);
            }
        });
    }



}