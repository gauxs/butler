package com.example.butlerkamaster.ClientRequestHandler;

import android.util.Log;

import com.example.butlerkamaster.ClientInfoHandler.ClientInfo;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.Header;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.ProxyMsg;
import com.example.butlerkamaster.FlatbufferHandler.AuthReq;

import java.nio.ByteBuffer;

public class ClientRequest {

    public byte[] formAuthReqMsg(String country, String state, String city,
                               String username, String secretKey){
        if(country.isEmpty()){
            country = "india";
        }
        if(state.isEmpty()){
            state = "karnataka";
        }
        if(city.isEmpty()){
            city = "bengaluru";
        }
        if(username.isEmpty()){
            username = "gaux";
        }
        if(secretKey.isEmpty()){
            secretKey = "butler";
        }
        ClientInfo clientObj = ClientInfo.getInstance();
        clientObj.setCountry(country);
        clientObj.setState(state);
        clientObj.setCity(city);
        clientObj.setUsername(username);

        AuthReq ar = new AuthReq();
        byte[] ret = ar.formAuthReqFb(clientObj);
        ProxyMsg proxy_msg = ProxyMsg.getRootAsProxyMsg(ByteBuffer.wrap(ret));
        Header header = proxy_msg.header();
        Log.e("ClientRequest",header.country());
        return ret;
    }
}
