import 'package:flutter/material.dart';
import 'package:pxm/constants.dart';
import 'package:pxm/routes.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: routerConfig,
      title: appTitle,
    );
  }
}
