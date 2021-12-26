import 'package:html_unescape/html_unescape.dart';
import 'package:pxm/Helpers/constant.dart';
import 'package:pxm/Services/request.dart';
import 'package:xml/xml.dart';

/// Base Class for LastFM Models
abstract class _BaseObject {
  String wsPrefix;

  _BaseObject({required this.wsPrefix});

  /// Performs a request call to the server
  Future<XmlDocument> _request(
    String methodName, {
    bool cacheable = false,
    Map<String, String>? params,
  }) async {
    params ??= _getParams();

    return LastFMRequest(methodName, params: params)
        .execute(cacheable: cacheable);
  }

  /// Returns the most common set of parameters between all objects.
  Map<String, String> _getParams() => {};

  @override
  // ignore: hash_and_equals
  int get hashCode {
    final values = _getParams().values;

    return (runtimeType.toString() +
            (_getParams().keys.toList() + values.toList()).join().toLowerCase())
        .hashCode;
  }

  Future<String?> _extractCdataFromRequest(
    String methodName,
    String tagName,
    Map<String, String> params,
  ) async {
    final doc = await _request(methodName, cacheable: true, params: params);

    final firstChild = doc.findAllElements(tagName).first.firstChild;

    return firstChild?.text.trim();
  }

  /// Returns the published date of the wiki.
  /// Only for Album/Track.
  Future<String?> getWikiPublishedDate() async => getWiki('published');

  /// Returns the summary of the wiki.
  /// Only for Album/Track.
  Future<String?> getWikiSummary() async => getWiki('summary');

  /// Returns the content of the wiki.
  /// Only for Album/Track.
  Future<String?> getWikiContent() async => getWiki('content');

  /// Returns a section of the wiki.
  /// Only for Album/Track.
  /// section can be "content", "summary" or
  /// "published" (for published date)
  Future<String?> getWiki(String section) async {
    final doc = await _request('$wsPrefix.getInfo');

    if (doc.findAllElements('wiki').isEmpty) return null;

    final node = doc.findAllElements('wiki').first;
    return _extract(node, section);
  }
}

/// Class to hold the common properties of both Album & Track class
abstract class _Opus extends _BaseObject {
  late Artist artist;
  late String title;
  late Map<String, dynamic> info;

  /// Create an opus instance.
  ///       Parameters:
  ///       -------------------------------
  ///       artist: An artist name or an Artist object.
  ///       title: The album or track title.
  ///       ws_prefix: 'album' or 'track'
  _Opus(
    artist,
    String title, {
    required String wsPrefix,
    Map<String, dynamic>? info,
  }) : super(wsPrefix: wsPrefix) {
    info ??= {};

    if (artist is Artist) {
      this.artist = artist;
    } else {
      this.artist = Artist(artist.toString());
    }

    // ignore: prefer_initializing_formals
    this.title = title;
    // ignore: prefer_initializing_formals
    this.info = info;
  }

  @override
  String toString() => '${artist.name} - $title';

  @override
  // ignore: hash_and_equals
  bool operator ==(Object other) {
    if (other is _Opus && runtimeType == other.runtimeType) {
      final a = title.toLowerCase();
      final b = other.title.toLowerCase();
      final c = artist.name.toLowerCase();
      final d = other.artist.name.toLowerCase();
      return (a == b) && (c == d);
    } else {
      return false;
    }
  }

  @override
  Map<String, String> _getParams() => {'artist': artist.name, wsPrefix: title};

  /// Returns the associated Artist object.
  Future<Artist> getArtist() async => Future.value(artist);

  /// Returns the artist or track title.
  Future<String> getTitle({bool properlyCapitalized = false}) async {
    if (properlyCapitalized) {
      title = _extract(
        await _request('$wsPrefix.getInfo', cacheable: true),
        'name',
      )!;
    }
    return title;
  }

  /// Returns the album or track title (alias to getTitle()).
  Future<String> getName({bool properlyCapitalized = false}) =>
      getTitle(properlyCapitalized: properlyCapitalized);

  /// Returns a URI to the cover image
  /// size can be one of:
  ///      SIZE_EXTRA_LARGE
  ///      SIZE_LARGE
  ///      SIZE_MEDIUM
  ///      SIZE_SMALL
  Future<String?> getCoverImage({int size = SIZE_EXTRA_LARGE}) async {
    if (!info.containsKey('image')) {
      info['image'] = _extractAll(
        await _request('$wsPrefix.getInfo', cacheable: true),
        'image',
      );
    }
    return (info['image']! as List<String?>).elementAt(size);
  }
}

/// An album.
class Album extends _Opus {
  Album(artist, String title, {Map<String, dynamic>? info})
      : super(artist, title, wsPrefix: 'album', info: info);

  Future<List<Track>> getTracks() async =>
      _extractTracks(await _request('$wsPrefix.getInfo', cacheable: true));
}

/// A Last.fm track.
class Track extends _Opus {
  Track(artist, String title, {Map<String, dynamic>? info})
      : super(artist, title, wsPrefix: 'track', info: info);

  /// Returns the corrected track name.
  Future<String?> getCorrection() async =>
      _extract(await _request('$wsPrefix.getCorrection'), 'name');

  /// Returns the track duration.
  Future<num> getDuration() async {
    final doc = await _request('$wsPrefix.getInfo', cacheable: true);

    return _number(_extract(doc, 'duration'));
  }

  /// Returns True if the track is available at Last.fm.
  Future<bool> isStreamable() async {
    final doc = await _request('$wsPrefix.getInfo', cacheable: true);

    return _extract(doc, 'streamable') == '1';
  }

  /// Returns True if the full track is available for streaming.
  Future<bool> isFullTrackAvailable() async {
    final doc = await _request('$wsPrefix.getInfo', cacheable: true);
    // ignore: ignore_typo
    return doc.findAllElements('streamable').first.getAttribute('fulltrack') ==
        '1';
  }

  /// Returns the album object of this track.
  Future<Album?> getAlbum() async {
    if (info.containsKey('album') && info['album'] != null) {
      return Album(artist, info['album'] as String);
    }

    final doc = await _request('$wsPrefix.getInfo', cacheable: true);

    final album = doc.findAllElements('album');

    if (album.isEmpty) return null;

    final node = doc.findAllElements('album').first;
    return Album(_extract(node, 'artist'), _extract(node, 'title')!);
  }
}

/// An artist.
class Artist extends _BaseObject {
  late String name;
  late Map<String, dynamic> info;

  Artist(this.name, {Map<String, dynamic>? info}) : super(wsPrefix: 'artist') {
    info ??= {};
    // ignore: prefer_initializing_formals
    this.info = info;
  }

  @override
  String toString() => name;

  @override
  // ignore: hash_and_equals
  bool operator ==(Object other) {
    if (other is Artist && runtimeType == other.runtimeType) {
      return name.toLowerCase() == other.name.toLowerCase();
    } else {
      return false;
    }
  }

  @override
  Map<String, String> _getParams() => {wsPrefix: name};

  /// Returns the name of the artist.
  /// If properly_capitalized was asserted then the name would be downloaded
  /// overwriting the given one.
  Future<String> getName({bool properlyCapitalized = false}) async {
    if (properlyCapitalized) {
      name = _extract(
        await _request('$wsPrefix.getInfo', cacheable: true),
        'name',
      )!;
    }
    return name;
  }

  /// Returns the corrected artist name.
  Future<String?> getCorrection() async =>
      _extract(await _request('$wsPrefix.getCorrection'), 'name');

  /// Returns True if the artist is streamable.
  Future<bool> isStreamable() async {
    final doc = await _request('$wsPrefix.getInfo', cacheable: true);

    return _number(_extract(doc, 'streamable')) != 0;
  }

  /// Returns a section of the bio.
  /// section can be "content", "summary" or
  /// "published" (for published date)
  Future<String?> getBio(String section, {String? language}) async {
    final params = _getParams();
    if (language != null) params['lang'] = language;

    return _extractCdataFromRequest(
      '$wsPrefix.getInfo',
      section,
      params,
    );
  }

  /// Returns the date on which the artist's biography was published.
  Future<String?> getBioPublishedDate() => getBio('published');

  /// Returns the summary of the artist's biography.
  Future<String?> getBioSummary({String? language}) =>
      getBio('summary', language: language);

  /// Returns the content of the artist's biography.
  Future<String?> getBioContent({String? language}) =>
      getBio('content', language: language);
}

/// An abstract class. Use one of its derivatives.
abstract class _Search extends _BaseObject {
  final String _wsPrefix;
  Map<String, String> searchTerms;
  int _lastPageIndex = 0;

  _Search({required String wsPrefix, required this.searchTerms})
      : _wsPrefix = wsPrefix,
        super(wsPrefix: wsPrefix);

  @override
  Map<String, String> _getParams() {
    final Map<String, String> params = {};
    params.addAll(searchTerms);
    return params;
  }

  /// Returns the total count of all the results.
  Future<String?> getTotalResultCount() async {
    final doc = await _request('$_wsPrefix.search', cacheable: true);
    return _extract(doc, 'totalResults');
  }

  /// Returns the node of matches to be processed
  Future<XmlElement> _retrievePage(int pageIndex) async {
    final params = _getParams();
    params['page'] = pageIndex.toString();
    final doc =
        await _request('$_wsPrefix.search', cacheable: true, params: params);

    return doc.findAllElements('${_wsPrefix}matches').first;
  }

  Future<XmlElement> _retrieveNextPage() async {
    _lastPageIndex++;
    return _retrievePage(_lastPageIndex);
  }
}

/// Search for an album by name.
class AlbumSearch extends _Search {
  AlbumSearch(String albumName)
      : super(wsPrefix: 'album', searchTerms: {'album': albumName});

  /// Returns the next page of results as a sequence of Album objects.
  Future<List<Album>> getNextPage() async {
    final masterNode = await _retrieveNextPage();

    final List<Album> seq = [];
    for (final node in masterNode.findAllElements('album')) {
      seq.add(
        Album(
          _extract(node, 'artist'),
          _extract(node, 'name')!,
          info: {'image': _extractAll(node, 'image')},
        ),
      );
    }
    return seq;
  }
}

/// Search for an artist by artist name.
class ArtistSearch extends _Search {
  ArtistSearch(String artistName)
      : super(wsPrefix: 'artist', searchTerms: {'artist': artistName});

  /// Returns the next page of results as a sequence of Artist objects.
  Future<List<Artist>> getNextPage() async {
    final masterNode = await _retrieveNextPage();

    final List<Artist> seq = [];
    for (final node in masterNode.findAllElements('artist')) {
      final artist = Artist(
        _extract(node, 'name')!,
        info: {'image': _extractAll(node, 'image')},
      );
      seq.add(artist);
    }
    return seq;
  }
}

/// Search for a track by track title. If you don't want to narrow the results
/// down by specifying the artist name, set it to empty string.
class TrackSearch extends _Search {
  TrackSearch(String artistName, String trackTitle)
      : super(
          wsPrefix: 'track',
          searchTerms: {'track': trackTitle, 'artist': artistName},
        );

  /// Returns the next page of results as a sequence of Track objects.
  Future<List<Track>> getNextPage() async {
    final masterNode = await _retrieveNextPage();

    final List<Track> seq = [];
    for (final node in masterNode.findAllElements('track')) {
      final track = Track(
        _extract(node, 'artist'),
        _extract(node, 'name')!,
        info: {'image': _extractAll(node, 'image')},
      );
      seq.add(track);
    }
    return seq;
  }
}

/// Extracts a value from the xml string
String? _extract(XmlNode node, String name, {int index = 0}) {
  final nodes = node.findAllElements(name).toList(growable: false);

  if (nodes.isNotEmpty) {
    if (nodes[index].firstChild != null) {
      return _unescapeHtmlEntity(nodes[index].firstChild!.text.trim());
    }
  }
}

/// Extracts all the values from the xml string. returning a list.
List<String?> _extractAll(XmlNode node, String name, {int? limitCount}) {
  final List<String?> seq = [];

  for (int i = 0; i < node.findAllElements(name).length; i++) {
    if (seq.length == limitCount) break;
    seq.add(_extract(node, name, index: i));
  }
  return seq;
}

/// Extracts Artist Information from Xml docs
// ignore: unused_element
List<Artist> _extractArtist(XmlDocument doc) {
  final List<Artist> seq = [];

  for (final node in doc.findAllElements('track')) {
    final name = _extract(node, 'name')!;
    seq.add(Artist(name));
  }
  return seq;
}

/// Extracts Album Information from Xml docs
// ignore: unused_element
List<Album> _extractAlbum(XmlDocument doc) {
  final List<Album> seq = [];

  for (final node in doc.findAllElements('track')) {
    final name = _extract(node, 'name')!;
    final artist = _extract(node, 'name', index: 1)!;
    seq.add(Album(artist, name));
  }
  return seq;
}

/// Extracts Track Information from Xml docs
List<Track> _extractTracks(XmlDocument doc) {
  final List<Track> seq = [];

  for (final node in doc.findAllElements('track')) {
    final name = _extract(node, 'name')!;
    final artist = _extract(node, 'name', index: 1)!;
    seq.add(Track(artist, name));
  }
  return seq;
}

/// Returns a number as represented by the string, or zero
num _number(String? string) => num.tryParse(string ?? '0') ?? 0;

/// Decodes HTML escape sequences
String _unescapeHtmlEntity(String string) {
  return HtmlUnescape().convert(string);
}
