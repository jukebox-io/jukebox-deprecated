import 'package:flutter/material.dart';
import 'package:jukebox/Helpers/logging.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: TextButton(
          onPressed: testLogger,
          child: Text(
            "Click Here",
            style: TextStyle(fontSize: 50),
          ),
        ),
      ),
    );
  }
}
