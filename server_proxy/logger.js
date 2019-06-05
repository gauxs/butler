'use strict';

var log4js = require('log4js');
log4js.configure({
  appenders: [
    //{ type: 'console' },
    { type: 'file', filename: '/var/log/server_proxy.log', category: 'ServerProxy',
      maxLogSize: 1000000000,
      numBackups: 10,
      compress: true, 
      encoding: 'utf-8',
      mode: 0o0644,
      flags: 'w+',
      layout: {
          type: 'pattern',
          pattern: '[%d{yyyy-MM-dd hh.mm.ss.SSS} PID:%z %p]: %m%n'
      }
    }
  ]
});

var logger = log4js.getLogger('ServerProxy');
logger.setLevel('DEBUG')
Object.defineProperty(exports, "LOG", {value: logger});
