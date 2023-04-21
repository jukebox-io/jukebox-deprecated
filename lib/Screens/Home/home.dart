import 'package:flutter/material.dart';

import 'package:jukebox/logging.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: TextButton(
          child: const Text("Click Here"),
          onPressed: () {
            Logger.log("Hello World");
          },
        ),
      ),
    );
  }
}
