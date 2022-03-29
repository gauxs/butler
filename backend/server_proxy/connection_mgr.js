'use strict';

var logger = require('./logger.js');
var log = logger.LOG;
var ProxyConnection = function(ws, country, state, city, username) {
    this.ws = ws; // Websocket related to client connection
    this.id = ws._ultron.id.toString();
    /* XXX: Store the ultron is as conn ID
     * When websocket close event is triggered, the ws._ultron is set to null.
     * Hence store the id as a new property 'conn_id'.
     */
    this.ws["conn_id"] = this.id
    this.country = country.toString();
    this.state = state.toString();
    this.city = city.toString();
    this.username = username.toString();
    this.send = function(msg) {
        log.info("sending message on conn id %s " +
                 "(client '%s', country '%s', state '%s', ",
                 "city '%s')",
                 this.id, this.username, this.country, this.state,
                 this.city)
        this.ws.send(msg, function (err) {
            if (err) {
                log.error("Failed to message on conn id %s " +
                "(client '%s', country '%s', state '%s', ",
                "city '%s')",
                this.id, this.username, this.country, this.state,
                this.city)
            }
        });
    };
}


exports.ConnectionManager = function() {
    /* XXX: Make this class Singleton */
    this.id_to_conn_map = {};
    this.user_conn_map = {};

    this.get_conn_from_conn_map = function(country, state, city, username) {
        if (country in this.user_conn_map) { 
            if (state in this.user_conn_map[country]) {
                if (city in this.user_conn_map[country][state]) {
                    if (username in this.user_conn_map[country][state]) {
                        return this.user_conn_map[country][state][city][username]
                    }
                }
            }
        }
        return null;
    }

    this.get_conns_for_site = function(country, state) {
        if (country in this.user_conn_map) {
            if (state in this.user_conn_map[country]) {
                return this.user_conn_map[country][state]
            }
        }
        return null;
    }

    this.get_conn_id_from_ws = function(ws) {
        if (ws.hasOwnProperty("conn_id")) {
            return ws.conn_id.toString()
	    }

        if (ws._ultron != null) {
             return ws._ultron.id.toString();
        }
        return null;
    }

    this.get_conn_using_ws = function(ws) {
        var id = this.get_conn_id_from_ws(ws);
        if (id == null) {
            return null;
        }
        if (id in this.id_to_conn_map) {
            return this.id_to_conn_map[id]
        }
        return null;
    }

    this.check_conn_exists = function(ws, country, state, city, username) {
        var id = this.get_conn_id_from_ws(ws);
        if (id == null) {
            return false;
        }
        var is_id_exists = id in this.id_to_conn_map;
        if (is_id_exists) {
            log.info("Connection with ID (%s) already exists.", id)
            return true;
        }

        if (this.user_conn_map[country] !== undefined) {
            if (state in this.user_conn_map[country]) {
                if (city in this.user_conn_map[country][state]) {
                    if (username in this.user_conn_map[country][state][city]) {
                        log.info("Client with serial (%s) from site (%s) already connected.",
                                serial, state);
                        return true;
                    }
                }
            }
        }
        return false;
    }

    this.store_conn = function(ws, country, state, city, username) {
        if (!(country in this.user_conn_map)) {
            this.user_conn_map[country] = {};
        }
        if (!(state in this.user_conn_map[country])) {
            this.user_conn_map[country][state] = {};
        }
        if (!(city in this.user_conn_map[country][state])) {
            this.user_conn_map[country][state][city] = {};
        }
        if (!(username in this.user_conn_map[country][state][city])) {
            this.user_conn_map[country][state][city][username] = {};
        }
        if (username in this.user_conn_map[country][state][city]) {
            log.error("Connection already exists for client: %s country: '%s', state: '%s', city: '%s'.",
                      username, country, state, city)
            old_conn = this.user_conn_map[country][state][city][username]
            if (old_conn) {
                this.close_conn(old_conn.ws)
            }
        }
        var conn = new ProxyConnection(ws, country, state, city, username);
        this.id_to_conn_map[conn.id] = conn;
        this.user_conn_map[country][state][city][username] = conn;
        log.info("Connection stored for client '%s', country '%s', state '%s', city '%s'.",
                  username, country, state, city)
    }

    this.close_conn = function(ws) {
        var id = this.get_conn_id_from_ws(ws);
        if (id == null) {
            log.error('Failed to close connection. Could not find connection id in conntrack.')
            return;
        }
        if (id in this.id_to_conn_map) {
            var conn = this.id_to_conn_map[id];
            var country = conn.country;
            var state = conn.state;
            var city = conn.city;
            var username = conn.username;
            if (country in this.user_conn_map) {
                if (state in this.user_conn_map[country]) {
                    if (city in this.user_conn_map[country][state]) {
                        if (username in this.user_conn_map[country][state][city]) {
                            delete this.user_conn_map[country][state][city][username];
                            log.info("Removed connection stored for client '%s', country '%s', state '%s'",
                                        " city '%s'.", username, country, state, city)
                        }
                    }
                    // For a given country and state, no city exists
                    // then remove user to conn map entry for city
                    if (Object.keys(this.user_conn_map[country][state]).length == 0) {
                        delete this.user_conn_map[country][state];
                    }
                }
            }
            // Stop tracking the conn if closed.
            delete this.id_to_conn_map[id];
            log.info("Removed client conn (%s) entry from id-to-conn map.", id);
            ws.close()
            log.info("Closed websocket after removing the old connection entry.");
        }
    }
}
