package com.example.butlerkamaster.ui.main;

import android.support.design.widget.Snackbar;
import android.util.Log;

import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

public class SocketWorker extends WebSocketListener {
    private static final int NORMAL_CLOSURE_STATUS = 1000;
    String tag = "SocketWorker";
//    @Override
//    public void onOpen(WebSocket webSocket, Response response) {
//        webSocket.send("Hello, it's SSaurel !");
//        webSocket.send("What's up ?");
//        webSocket.send(ByteString.decodeHex("deadbeef"));
//        webSocket.close(NORMAL_CLOSURE_STATUS, "Goodbye !");
//    }
    @Override
    public void onMessage(WebSocket webSocket, String text) {
        Log.i(tag,"Receiving : "+ text);
    }
    @Override
    public void onMessage(WebSocket webSocket, ByteString bytes) {
        Log.i(tag,"Receiving bytes : "+ bytes.hex());
    }
    @Override
    public void onClosing(WebSocket webSocket, int code, String reason) {
        webSocket.close(NORMAL_CLOSURE_STATUS, null);
        Log.i(tag,"Closing : " + code + " / " + reason);
    }
    @Override
    public void onFailure(WebSocket webSocket, Throwable t, Response response) {
        Log.e(tag,"Error : " + t.getMessage());
    }
}
