'use strict';

var log4js = require('log4js');
log4js.configure({
  appenders: {
    //{ type: 'console' },
    infoLog : { type: 'file',
      filename: '/var/log/server_proxy.log',
      //category: 'ServerProxy',
      maxLogSize: 1000000000,
      type: 'file',
      level: 'trace',
      maxLevel: 'error',
      appender: 'infoLog',
      layout: {
          type: 'pattern',
          pattern: '[%d{yyyy-MM-dd hh.mm.ss.SSS} PID:%z %p]: %m%n'
      }
    }
  },
  categories: {
    default: {
      appenders: ['infoLog'],
      level: 'trace'
    }
  }
});

var logger = log4js.getLogger('ServerProxy');
//logger.setLevel('DEBUG')
Object.defineProperty(exports, "LOG", {value: logger});
