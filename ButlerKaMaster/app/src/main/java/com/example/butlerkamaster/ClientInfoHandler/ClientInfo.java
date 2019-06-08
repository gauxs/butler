package com.example.butlerkamaster.ClientInfoHandler;

public class ClientInfo {
    private String country;
    private String state;
    private String city;
    private String username;

    private static final ClientInfo ourInstance = new ClientInfo();

    public static ClientInfo getInstance() {
        return ourInstance;
    }

    private ClientInfo(){
    }

    public void setCountry(String country) {
        this.country = country;
    }

    public String getCountry() {
        return country;
    }

    public void setState(String state) {
        this.state = state;
    }

    public String getState() {
        return state;
    }


    public void setCity(String city) {
        this.city = city;
    }

    public String getCity() {
        return city;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getUsername() {
        return username;
    }
}
