/*
 * Copyright (c) 2023 JukeBox Developers - All Rights Reserved
 * This file is part of the JukeBox Music App and is released under the "MIT License Agreement"
 * Please see the LICENSE file that should have been included as part of this package
 */

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
