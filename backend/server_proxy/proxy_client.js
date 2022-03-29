var flatbuffers = require('../tools/flatbuffers/js/flatbuffers').flatbuffers;
var ServerProxy = require('../flatbuffer/js_defs/ServerProxy_generated').ServerProxy;
var proxy_fb_handle = require('./proxy_fb_handler');

var WebSocket = require('ws');
var ws = new WebSocket('ws://127.0.0.1:3907/butler');

ws.on('open', function() {
    var fb = proxy_fb_handle.get_auth_req_fb("gaux", "some_service", "india", "karnataka", "bengaluru", "butler")
    ws.send(fb);
    console.log("Sent auth req fb msg...");
});

ws.on('message', function(data, flags) {
    console.log("received msg from proxy server")
    var buf = new flatbuffers.ByteBuffer(data);
    var proxy_msg = ServerProxy.ProxyMsg.getRootAsProxyMsg(buf);
    var header = proxy_msg.header();
    var payload_type = proxy_msg.payloadType();
    console.log("recvd msg with payload type: %s", payload_type)
    console.log("payload type : %s", payload_type)
    if (payload_type == ServerProxy.Payload.OvlSecureTunnel_SyncTunDefMsg) {
        console.log("Received tunnels cfg ....")
        return;
    } else if (payload_type == ServerProxy.Payload.AuthRespMsg) {
        var auth_resp_msg = proxy_msg.payload(new ServerProxy.AuthRespMsg());
        if (auth_resp_msg.status() == ServerProxy.AUTH_STATUS.SUCCESS) {
            console.log("Client Authenticated!");
        } else {
            console.log("Client not authorized!");
            ws.close();
            return;
        }
    }
});

ws.on('error', function(error) {
    console.log("error received..."+error.toString());
});

ws.on('close', function(data, flags) {
    console.log("Connection closed with server...");
});

