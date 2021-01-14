package com.hung.searchapp.api;


public class APIUtils {
    private static volatile APIService service;

    public static APIService getAPIService() {
        if (service == null) {
            synchronized (APIUtils.class) {
                if (service == null) {
                    service = RetrofitClient.getClient().create(APIService.class);
                }
            }
        }
        return service;
    }
}