import 'package:beamer/beamer.dart';
import 'package:flutter/material.dart';

import './Screens/Home/home.dart';

class JukeBoxApp extends StatelessWidget {
  JukeBoxApp({Key? key}) : super(key: key);

  final routerDelegate = BeamerDelegate(
    locationBuilder: RoutesLocationBuilder(
      routes: {
        '/': (_, __, ___) => const HomeScreen(),
      },
    ),
  );

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: "JukeBox",
      routerDelegate: routerDelegate,
      routeInformationParser: BeamerParser(),
      backButtonDispatcher: BeamerBackButtonDispatcher(
        delegate: routerDelegate,
      ),
    );
  }
}

void main() {
  runApp(JukeBoxApp());
}
