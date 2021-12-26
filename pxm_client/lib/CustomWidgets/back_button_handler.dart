import 'package:flutter/material.dart';

class BackButtonHandler extends StatelessWidget {
  final Widget child;
  final bool Function()? onBackPressed;

  const BackButtonHandler({
    Key? key,
    this.onBackPressed,
    required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        if (onBackPressed == null) {
          return true;
        }
        return onBackPressed!();
      },
      child: child,
    );
  }
}
