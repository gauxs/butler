'use strict';

var logger = require('./logger.js');
var log = logger.LOG;
var proxy_fb_handle = require('./proxy_fb_handler');
//var redis_conn = require('./redis_connector');
var conn_mgr = require('./connection_mgr');
var flatbuffers = require('../tools/flatbuffers/js/flatbuffers').flatbuffers; 
var ServerProxy = require('../flatbuffer/js_defs/ServerProxy_generated').ServerProxy;
var http = require('http');
var app = require('express')();
var expressWs = require('express-ws');
var server = http.createServer(app);
var expressWs = expressWs(app, server);
var ConnMgr = new conn_mgr.ConnectionManager();

var handle_msg_from_svc = function(channel, enc_msg) {
    try {
        log.info("Received message from server on channel: %s, len: %s",
                    channel, enc_msg.length);
        // Decode the msg using base64 (message from redis is in base64 format)
        var msg = new Buffer(enc_msg, 'base64')
        var buf = new flatbuffers.ByteBuffer(msg);
        var proxy_msg = ServerProxy.ProxyMsg.getRootAsProxyMsg(buf);
        var header = proxy_msg.header();
        var country = header.country();
        var state = header.state();
        var city = header.city();
        var source = header.source();
        log.debug("Message for client: %s", source);
        /* Forward the message to the specific client */
        var conn = ConnMgr.get_conn_from_conn_map(country, state, city, source);
        if (conn == null) {
            log.error("Error: Proxy not connected to client %s. " +
                        "Failed to forward the messaage from server.",
                        source);
            return;
        }
        conn.send(msg);
    }catch (err) {
        log.error("Failed to process message on channel '%s'", channel)
    }
}

var handle_msg_from_client = function(ws, req, msg) {
    log.debug("Received message from client. len: %s", msg.length);
    var buf = new flatbuffers.ByteBuffer(msg);
    var proxy_msg = ServerProxy.ProxyMsg.getRootAsProxyMsg(buf);
    var header = proxy_msg.header();
    var payload_type = proxy_msg.payloadType();
    var payload;
    var country = header.country();
    var state = header.state();
    var city = header.city();
    var source = header.source();
    var dest = header.dest();

    log.info("Received message from client '%s', country '%s', state '%s', city '%s'",
        source, country, state, city);
    if (payload_type == ServerProxy.Payload.AuthReqMsg) {
        var auth_req = proxy_msg.payload(new ServerProxy.AuthReqMsg());
        var secret_key = auth_req.secretkey();
        log.info("Secret key is '%s'", secret_key);
        /* Store the websocket in order to reply back the
        * server message back to client
        */
        if (ConnMgr.check_conn_exists(ws, country, state, city, source)) {
            /* Connection already tracked. Duplicate auth req.
                * Close the old connection and use the new connection. */
            log.info("Connection already authorized. Duplicate auth req recvd.");
            var old_conn = ConnMgr.get_conn_from_conn_map(country, state, city, source);
            if (old_conn != null) {
                if (old_conn.id == ws._ultron.id.toString()) {
                    /* Same connection but duplicate Auth req sent. Ignore the auth req. */
                    return;
                } else {
                    /* The Auth req received on a different websocket but from same client.
                        * Close the old connection and process the new connection request.
                        */
                    log.info("Closing the old connection id '%s' for client '%s', country '%s', state '%s', city '%s'",
                                old_conn.id, source, country, state, city);
                    ConnMgr.close_conn(old_conn.ws);
                }
            }
        }

        // Verify client info
        if (secret_key == null) {
            log.error("Wrong secret key: '%s'", secret_key);
            ws.close();
            return;
        }
        if (secret_key=="butler") {
            /* Client secret key is correct. Send a success.
            */
            var fb = proxy_fb_handle.get_auth_resp_fb(header, true);
            log.info("Sent authentication success response to client country '%s', state '%s', city '%s'",
                    country, state, city);
            ws.send(fb, function (err) {
                if (err) {
                    log.error("Failed to send message to client %s, country" +
                            "'%s', state '%s', city '%s'. Error: %s", source,
                            country, state, city, err.message);
                } else {
                    /* Store the websocket in order to reply back the
                    * server message back to client
                    */
                    ConnMgr.store_conn(ws, country, state, city, source);
                    log.info("Started tracking new connection.");
                }
            });
        } else {
            /* Client provided wrong secret-key */
            var fb = proxy_fb_handle.get_auth_resp_fb(header, false);
            log.info("Sent authentication failure response for conn id");
            ws.send(fb, function (err) {
                if (err) {
                    log.error("Failed to send auth-fail message to client %s, country " +
                            "'%s', state '%s', city '%s'. Error: %s", source,
                            country, state, city, err.message);
                } else {
                    /* un-authorized connection. close the socket */
                    ws.close();
                }
            });
        }
    }else{
        // Check if client already authenticated and
        // if not reject the request and drop the connection
        var conn = ConnMgr.get_conn_using_ws(ws);
        if (conn == null) {
            log.error("Client connection not being tracked. " + 
                        "Possibly not authenticated.");
            log.error("Close the connection for client '%s', country '%s', state '%s', city '%s'.",
                        header.source(), header.country(), header.state(), header.city());
            ws.close();
            return;
        }
        log.info("Received message from client '%s', country '%s', state '%s' city '%s'",
                    header.source(), header.country(), header.state(), header.city());

        var hdr_channel = header.channel();
        var from_svc_channel = hdr_channel + "/from_service"
        var to_svc_channel = hdr_channel + "/to_service"

        /* Subsribe to channel to received messages from service's of server */
        //redis_conn.subscribe_channel(from_svc_channel, handle_msg_from_svc);

        /* Publish the msg on to the channel for controller service.
        * Also encode the msg using base64
        */
        var enc_msg = new Buffer(msg).toString('base64');
        //redis_conn.publish(to_svc_channel, enc_msg);

        log.info("Published client message on redis channel %s.",
                    to_svc_channel);  
    }
}

app.ws('/butler', function(ws, req) {
    ws.on('message', function(msg) {
        log.debug("received client message")
        try {
            handle_msg_from_client(ws, req, msg);
        }
        catch (err) {
            log.error(err.stack)
            ConnMgr.close_conn(ws);
        }
    });

    ws.on('close', function(code, reason) {
        log.error("client websocket closed event triggered...code: %s, reason: %s", code, reason)
        ConnMgr.close_conn(ws);
        log.info("Client connection closed.");
    });
});

app.on('error', function() {
    log.error("Error in websocket")
});

log.info("Listening on port 3907...");
server.listen(3907);
