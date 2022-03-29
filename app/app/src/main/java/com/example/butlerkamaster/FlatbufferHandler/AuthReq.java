package com.example.butlerkamaster.FlatbufferHandler;

import android.util.Log;

import com.example.butlerkamaster.ClientInfoHandler.ClientInfo;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.AuthReqMsg;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.Header;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.Payload;
import com.example.butlerkamaster.FlatbufferDefs.ServerProxy.ProxyMsg;
import com.google.flatbuffers.FlatBufferBuilder;

import java.nio.ByteBuffer;

public class AuthReq {
    private String secretkey = "butler";
    private String destServer = "ButlerServer";

    public byte[] formAuthReqFb(ClientInfo clientObj){
        FlatBufferBuilder builder = new FlatBufferBuilder(1024);
        Log.e("AuthReq", clientObj.getCountry());
        int countryFb = builder.createString(clientObj.getCountry());
        int stateFb = builder.createString(clientObj.getState());
        int cityFb = builder.createString(clientObj.getCity());
        int userNameFb = builder.createString(clientObj.getUsername());
        int destServerFb = builder.createString(destServer);

        // Prepare header
        Header.startHeader(builder);
        Header.addCountry(builder, countryFb);
        Header.addState(builder, stateFb);
        Header.addCity(builder, cityFb);
        Header.addSource(builder, userNameFb);
        Header.addDest(builder, destServerFb);
        int header = Header.endHeader(builder);

        countryFb = builder.createString(clientObj.getCountry());
        stateFb = builder.createString(clientObj.getState());
        cityFb = builder.createString(clientObj.getCity());
        userNameFb = builder.createString(clientObj.getUsername());
        destServerFb = builder.createString(destServer);
        int secretKeyFb = builder.createString(secretkey);
        // Prepare payload - request message
        AuthReqMsg.startAuthReqMsg(builder);
        AuthReqMsg.addCountry(builder, countryFb);
        AuthReqMsg.addState(builder, stateFb);
        AuthReqMsg.addCity(builder, cityFb);
        AuthReqMsg.addSource(builder, userNameFb);
        AuthReqMsg.addDest(builder, destServerFb);
        AuthReqMsg.addSecretkey(builder, secretKeyFb);
        int auth_req_msg = AuthReqMsg.endAuthReqMsg(builder);

        // Prepare ProxyMsg
        ProxyMsg.startProxyMsg(builder);
        // Add header and payload to proxy msg
        ProxyMsg.addHeader(builder, header);

        ProxyMsg.addPayload(builder, auth_req_msg);
        ProxyMsg.addPayloadType(builder, Payload.AuthReqMsg); // Stamp the type for the Union
        int proxy_msg = ProxyMsg.endProxyMsg(builder);

        // Done building ProxyMsg
        builder.finish(proxy_msg);
        byte[] fb = builder.sizedByteArray();
        Log.e("AuthReq", ByteBuffer.wrap(fb).toString());

        return fb;
    }
}
