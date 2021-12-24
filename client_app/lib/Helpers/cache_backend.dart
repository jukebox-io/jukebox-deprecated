import 'package:hive/hive.dart';
import 'package:pxm/Helpers/constant.dart';

/// Used as a backend for caching cacheable requests.
abstract class CacheBackend extends Iterable<String> {
  CacheBackend();

  /// gets XML text from cache, with the given key
  String? getXml(String key);

  /// sets XML text into cache, with the given key
  void setXml(String key, String xmlString);

  /// Create a cache backend
  factory CacheBackend.create() => _HiveCacheBackend();
}

class _HiveCacheBackend extends CacheBackend {
  final dict = Hive.box<String>(BOX_NAME_CACHE);

  @override
  String? getXml(String key) => dict.get(key);

  @override
  Iterator<String> get iterator => dict.keys.map((e) => e as String).iterator;

  @override
  void setXml(String key, String xmlString) {
    dict.put(key, xmlString);
  }
}
