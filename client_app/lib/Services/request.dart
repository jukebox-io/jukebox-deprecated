import 'dart:convert';

import 'package:crypto/crypto.dart';
import 'package:http/http.dart' as _http;
import 'package:meta/meta.dart' show nonVirtual;
import 'package:package_info/package_info.dart';
import 'package:pxm/Helpers/cache_backend.dart';
import 'package:pxm/Helpers/constant.dart';
import 'package:xml/xml.dart';

// ignore: non_constant_identifier_names
final _BASEURL = Uri.parse('https://projectx-music-backend.herokuapp.com');

abstract class BaseRequest extends _http.Request {
  BaseRequest({
    String method = HTTP_METHOD_GET,
    required String path,
  }) : super(method, _BASEURL.resolve(path));

  @nonVirtual
  @override
  Future<_http.StreamedResponse> send() async {
    // Resolve Headers
    headers['User-Agent'] =
        'project-x-music/${(await PackageInfo.fromPlatform()).version}';

    // Execute Actual Response
    final response = await super.send();

    if ([500, 502, 503, 504].contains(response.statusCode)) {
      throw Exception(
        'Connection to the API failed with HTTP code ${response.statusCode}',
      );
    }

    return response;
  }
}

/// Representing an abstract web service operation.
class LastFMRequest extends BaseRequest {
  late final Map<String, String> params;
  static final cache = CacheBackend.create();

  LastFMRequest(String methodName, {Map<String, String>? params})
      : super(method: HTTP_METHOD_GET, path: 'lastfm/api') {
    this.params = params ?? {};
    this.params['method'] = methodName;

    headers['Content-type'] = 'application/x-www-form-urlencoded';
    headers['Accept-Charset'] = 'utf-8';

    encoding = Encoding.getByName('utf-8')!;
    bodyFields = this.params;
  }

  /// The cache key is a string of concatenated sorted names and values.
  String _getCacheKey() {
    final keys = params.keys.toList();
    keys.sort();

    var cacheKey = '';

    for (final key in keys) {
      if (!<String>[].contains(key)) cacheKey += key + params[key]!;
    }

    return sha1.convert(utf8.encode(cacheKey)).toString();
  }

  /// Returns a xml file object of the cached response.
  Future<String> _getCachedResponse() async {
    if (!_isCached()) {
      final response = await _downloadResponse();
      cache.setXml(_getCacheKey(), response);
    }

    return cache.getXml(_getCacheKey())!;
  }

  /// Returns True if the request is already in cache.
  bool _isCached() => cache.contains(_getCacheKey());

  /// Returns a xml file object of the response from the server.
  Future<String> _downloadResponse() async {
    final streamResponse = await send();
    final response = await _http.Response.fromStream(streamResponse);

    _checkResponseForErrors(response.body);
    return response.body;
  }

  /// Execute Request to Get Response as Xml Object
  Future<XmlDocument> execute({bool cacheable = false}) async {
    String response;
    if (cacheable) {
      response = await _getCachedResponse();
    } else {
      response = await _downloadResponse();
    }
    return XmlDocument.parse(response.replaceAll('opensearch:', ''));
  }

  /// Checks the response for errors and raises one if any exists.
  void _checkResponseForErrors(String response) {
    final doc = XmlDocument.parse(response.replaceAll('opensearch:', ''));

    var e = doc.findAllElements('lfm').first;

    if (e.getAttribute('status') != 'ok') {
      e = doc.findAllElements('error').first;
      final status = e.getAttribute('code');
      final details = e.firstChild?.text.trim();
      throw Exception('$status: $details');
    }
  }
}
