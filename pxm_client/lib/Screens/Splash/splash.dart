import 'package:flutter/material.dart';
import 'package:pxm/CustomWidgets/gradient_containers.dart';

class SplashScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GradientContainer(
      child: Scaffold(
        backgroundColor: Colors.transparent,
        body: Center(
          child: SizedBox.fromSize(
            size: MediaQuery.of(context).size * 0.30,
            child: Image.asset('assets/icon.png'),
          ),
        ),
        bottomNavigationBar: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: const [Text('https://github.com/ProjectX-music')],
        ),
      ),
    );
  }
}
