'use strict';
var flatbuffers = require('./flatbuffers').flatbuffers;
var ServerProxy = require('../flatbuffer_schema/js_defs/ServerProxy_generated').ServerProxy;

exports.get_auth_resp_fb = function(header, is_success) {
    // Start Flatbuffer builder
    var builder = new flatbuffers.Builder(1024);

    var source = builder.createString(header.dest());
    var dest = builder.createString(header.source());
    var country = builder.createString(header.country());
    var state = builder.createString(header.state());
    var city = builder.createString(header.city());

    // Build header
    ServerProxy.Header.startHeader(builder);
    ServerProxy.Header.addCountry(builder, country);
    ServerProxy.Header.addState(builder, state);
    ServerProxy.Header.addCity(builder, city);
    ServerProxy.Header.addSource(builder, source);
    ServerProxy.Header.addDest(builder, dest);

    var header = ServerProxy.Header.endHeader(builder);
    ServerProxy.AuthRespMsg.startAuthRespMsg(builder);
    ServerProxy.AuthRespMsg.addCountry(builder, country);
    ServerProxy.AuthRespMsg.addState(builder, state);
    ServerProxy.AuthRespMsg.addCity(builder, city);
    ServerProxy.AuthRespMsg.addSource(builder, source);
    ServerProxy.AuthRespMsg.addDest(builder, dest);
    if (is_success) {
        ServerProxy.AuthRespMsg.addStatus(builder, ServerProxy.AUTH_STATUS.SUCCESS);
    } else {
        ServerProxy.AuthRespMsg.addStatus(builder, ServerProxy.AUTH_STATUS.FAILURE);
    }
    var auth_resp_msg = ServerProxy.AuthRespMsg.endAuthRespMsg(builder);

    // Start building ProxyMsg
    ServerProxy.ProxyMsg.startProxyMsg(builder);
    // Add header and payload to proxy msg
    ServerProxy.ProxyMsg.addHeader(builder, header);
    ServerProxy.ProxyMsg.addPayloadType(builder, ServerProxy.Payload.AuthRespMsg); // Stamp the type for the Union
    ServerProxy.ProxyMsg.addPayload(builder, auth_resp_msg);

    var proxy_msg = ServerProxy.ProxyMsg.endProxyMsg(builder);

    // Done building ProxyMsg
    builder.finish(proxy_msg);

    var fb = builder.asUint8Array();
    return fb;
}
