import 'package:flutter/material.dart';
import 'package:hive/hive.dart';
import 'package:pxm/Helpers/constant.dart';

class _Theme with ChangeNotifier {
  var _isDark = true;
  // Hive.box(BOX_NAME_SETTINGS).get('darkMode', defaultValue: true) as bool;

  final darkThemeData = ThemeData.dark();
  final lightThemeData = ThemeData.light();

  List<Color> getBackGradient() => [
        Colors.grey[900]!,
        Colors.grey[900]!,
        Colors.black,
      ];

  List<Color> getTransBackGradient() => [
        Colors.grey[900]!.withOpacity(0.8),
        Colors.grey[900]!.withOpacity(0.9),
        Colors.black.withOpacity(1),
      ];

  List<Color> getLightBackGradient() => [
        const Color(0xfff5f9ff),
        Colors.white,
      ];

  void switchTheme({required bool isDark}) {
    _isDark = isDark;
    Hive.box(BOX_NAME_SETTINGS)
        .put('darkMode', isDark)
        .whenComplete(() => notifyListeners());
  }

  ThemeMode? currentThemeMode() => _isDark ? ThemeMode.dark : ThemeMode.light;
}

final currentTheme = _Theme();
