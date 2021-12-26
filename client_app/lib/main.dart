import 'dart:async';
import 'dart:io';

// import 'package:firebase_analytics/firebase_analytics.dart';
// import 'package:firebase_core/firebase_core.dart';
// import 'package:firebase_crashlytics/firebase_crashlytics.dart';
// import 'package:flutter/foundation.dart' show kDebugMode;
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:path_provider/path_provider.dart';
import 'package:pxm/CustomWidgets/authentication_wrapper.dart';
import 'package:pxm/Helpers/config.dart';
import 'package:pxm/Helpers/constant.dart';
import 'package:pxm/Screens/Home/home.dart';
import 'package:pxm/Screens/Splash/splash.dart';

// Entry Point of the Application
Future<void> main() async {
  // Not all errors are caught by Flutter. Sometimes, errors are instead caught by Zones.
  runZonedGuarded<Future<void>>(
    () async {
      // Initialize Application
      WidgetsFlutterBinding.ensureInitialized();
      // await Firebase.initializeApp();

      // Force disable Crashlytics collection while doing every day development.
      // Temporarily toggle this to true if you want to test crash reporting in your app.
      // await FirebaseCrashlytics.instance
      //     .setCrashlyticsCollectionEnabled(!kDebugMode);

      // Pass all uncaught errors from the framework to Crashlytics.
      // FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterError;

      await Hive.initFlutter();
      await openHiveBox(BOX_NAME_SETTINGS);
      await openHiveBox(BOX_NAME_CACHE, limit: true);

      Paint.enableDithering = true;

      // Run Material App
      runApp(Root());
    },
    (error, stack) {
      // FirebaseCrashlytics.instance.recordError(error, stack);
    },
  );
}

/// Opens a hive box if not opened. If [limit] is true, then it clears the box
/// once it reaches a pre-defined size.
///
/// Credit: @Sangwan5688 (repo: BlackHole)
Future<void> openHiveBox(String boxName, {bool limit = false}) async {
  try {
    if (limit) {
      final box = await Hive.openBox<String>(boxName);
      // clear box if it grows large
      if (box.length > 1000) {
        box.clear();
      }
      await Hive.openBox<String>(boxName);
    } else {
      await Hive.openBox<String>(boxName);
    }
  } catch (e) {
    final Directory dir = await getApplicationDocumentsDirectory();
    final String dirPath = dir.path;
    final File dbFile = File('$dirPath/$boxName.hive');
    final File lockFile = File('$dirPath/$boxName.lock');
    await dbFile.delete();
    await lockFile.delete();
    await Hive.openBox(boxName);
    throw 'Failed to open $boxName Box\nError: $e';
  }
}

// Root App
class Root extends StatefulWidget {
  @override
  _RootState createState() => _RootState();
}

// Root App State
class _RootState extends State<Root> {
  @override
  void initState() {
    super.initState();

    // Add Theme Change Listener
    currentTheme.addListener(() {
      setState(() {});
    });
  }

  @override
  Widget build(BuildContext context) {
    // Set Preferred Orientation to Portrait Mode
    SystemChrome.setPreferredOrientations([
      DeviceOrientation.portraitUp,
      DeviceOrientation.portraitDown,
    ]);

    return AuthenticationWrapper(
      child: MaterialApp(
        title: 'ProjectX-music',
        debugShowCheckedModeBanner: false,
        themeMode: currentTheme.currentThemeMode(),
        theme: currentTheme.lightThemeData,
        darkTheme: currentTheme.darkThemeData,
        // navigatorObservers: [
        //   FirebaseAnalyticsObserver(analytics: FirebaseAnalytics.instance),
        // ],
        routes: {
          ROUTE_NAME_HOME: (_) => HomeScreen(),
          ROUTE_NAME_SPLASH: (_) => SplashScreen(),
        },
      ),
    );
  }
}
