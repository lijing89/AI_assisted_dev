import 'dart:async';
import 'package:flutter/foundation.dart';
import 'dart:developer' as dev;

/// 日志工具类
class LogUtil {
  static const String _tag = "[CREAN_LOG]";

  /// 是否允许打印日志
  /// Release模式下默认不打印
  static bool get _enableLog => !kReleaseMode;

  /// 初始化日志工具
  static void init() {
    // 可以在这里进行一些初始化操作
  }

  /// 打印普通日志，默认使用 debug 级别
  static void print(dynamic message, {String? tag}) {
    debug(message, tag: tag);
  }

  /// 打印调试日志 (Debug Level)
  static void debug(dynamic message, {String? tag}) {
    if (_enableLog) {
      _printLog(message, tag: tag, level: Level.debug.value);
    }
  }

  /// 打印信息日志 (Info Level)
  static void info(dynamic message, {String? tag}) {
    if (_enableLog) {
      _printLog(message, tag: tag, level: Level.info.value);
    }
  }

  /// 打印警告日志 (Warning Level)
  static void warning(dynamic message, {String? tag}) {
    if (_enableLog) {
      _printLog(message, tag: tag, level: Level.warning.value);
    }
  }

  /// 打印错误日志 (Error Level)
  /// [error] 错误对象
  /// [stackTrace] 堆栈信息
  static void error(dynamic message, {String? tag, Object? error, StackTrace? stackTrace}) {
    if (_enableLog) {
      _printLog(message, tag: tag, level: Level.error.value);
      if (error != null) {
        debugPrint("\nError: $error");
      }
      if (stackTrace != null) {
        debugPrint("\nStackTrace: $stackTrace");
      }
    }
  }

  /// 通用日志方法，兼容 dart:developer 的 log 签名
  static void log(
    String message, {
    DateTime? time,
    int? sequenceNumber,
    int level = 0,
    String name = '',
    Zone? zone,
    Object? error,
    StackTrace? stackTrace,
  }) {
    if (_enableLog) {
      _printLog(message,
          tag: name.isNotEmpty ? name : null,
          level: level,
          sequenceNumber: sequenceNumber,
          zone: zone);
      if (error != null) {
        debugPrint("\nError: $error");
      }
      if (stackTrace != null) {
        debugPrint("\nStackTrace: $stackTrace");
      }
    }
  }

  /// 内部方法：实际执行日志打印
  static void _printLog(dynamic message,
      {String? tag, int level = 0, int? sequenceNumber, Zone? zone}) {
    final String logTag = tag ?? _tag;
    final DateTime timeStr = DateTime.now();
    //改为log打印
    dev.log(message.toString(),
        name: logTag,
        time: timeStr,
        level: level,
        sequenceNumber: sequenceNumber,
        zone: zone);
  }
}

class Level implements Comparable<Level> {
  final String name;

  /// Unique value for this level. Used to order levels, so filtering can
  /// exclude messages whose level is under certain value.
  final int value;

  const Level(this.name, this.value);

  /// Special key to turn on logging for all levels ([value] = 0).
  static const Level all = Level('ALL', 0);

  /// Special key to turn off all logging ([value] = 2000).
  static const Level off = Level('OFF', 2000);

  /// Key for debug messages ([value] = 500).
  static const Level debug = Level('DEBUG', 500);

  /// Key for informational messages ([value] = 800).
  static const Level info = Level('INFO', 800);

  /// Key for potential problems ([value] = 900).
  static const Level warning = Level('WARNING', 900);

  /// Key for serious failures ([value] = 1000).
  static const Level error = Level('ERROR', 1000);

  static const List<Level> levels = [
    all,
    debug,
    info,
    warning,
    error,
    off,
  ];

  @override
  /// 判断两个日志级别是否相等
  bool operator ==(Object other) => other is Level && value == other.value;

  /// 判断当前级别是否小于另一个级别
  bool operator <(Level other) => value < other.value;

  /// 判断当前级别是否小于或等于另一个级别
  bool operator <=(Level other) => value <= other.value;

  /// 判断当前级别是否大于另一个级别
  bool operator >(Level other) => value > other.value;

  /// 判断当前级别是否大于或等于另一个级别
  bool operator >=(Level other) => value >= other.value;

  @override
  /// 比较两个日志级别的大小，用于排序
  int compareTo(Level other) => value - other.value;

  @override
  /// 获取日志级别的哈希码
  int get hashCode => value;

  @override
  /// 返回日志级别的名称
  String toString() => name;
}