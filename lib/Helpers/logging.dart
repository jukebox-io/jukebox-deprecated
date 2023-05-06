/*
 * Copyright (c) 2023 JukeBox Developers - All Rights Reserved
 * This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
 * Please see the LICENSE file that should have been included as part of this package
 */

import 'package:flutter/cupertino.dart';

enum Level {
  verbose,
  debug,
  info,
  warning,
  error,
  fatal,
}

class Logger {
  static final Map<String, Logger> _loggers = <String, Logger>{};
  static Level level = Level.warning;

  String? className;

  Logger._internal(this.className);

  static Logger getLogger([String name = "Default"]) =>
      _loggers.putIfAbsent(name, () => Logger._internal(name));

  void verbose(dynamic message, [dynamic error, StackTrace? stackTrace]) =>
      log(Level.verbose, message, error, stackTrace);

  void debug(dynamic message, [dynamic error, StackTrace? stackTrace]) =>
      log(Level.debug, message, error, stackTrace);

  void info(dynamic message, [dynamic error, StackTrace? stackTrace]) =>
      log(Level.info, message, error, stackTrace);

  void warning(dynamic message, [dynamic error, StackTrace? stackTrace]) =>
      log(Level.warning, message, error, stackTrace);

  void error(dynamic message, [dynamic error, StackTrace? stackTrace]) =>
      log(Level.error, message, error, stackTrace);

  void fatal(dynamic message, [dynamic error, StackTrace? stackTrace]) =>
      log(Level.fatal, message, error, stackTrace);

  void log(Level level, dynamic message,
      [dynamic error, StackTrace? stackTrace]) {
    final time = DateTime.now();

    // Should Log
    bool shouldLog = false;
    assert(() {
      shouldLog = level.index >= Logger.level.index;
      return true;
    }());
    if (!shouldLog) {
      return; // skip logging
    }

    // Print Log
    debugPrint("$time ${level.name.toUpperCase().padRight(7)} [$className] $message");
  }
}

void testLogger() {
  Logger.level = Level.verbose;
  final logger = Logger.getLogger();
  logger.verbose('You don\'t always want to see all of these');
  logger.debug('Logs a debug message');
  logger.info('Public Function called');
  logger.warning('This might become a problem');
  logger.error('Something has happened');
  logger.fatal('Oh my God');
}
