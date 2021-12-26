// import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pxm/Screens/Authentication/authentication.dart';
import 'package:pxm/Services/authentication.dart';

class AuthenticationWrapper extends StatelessWidget {
  final Widget? child;

  const AuthenticationWrapper({required this.child, Key? key})
      : super(key: key);

  @override
  Widget build(BuildContext context) => StreamProvider<User?>.value(
        value: AuthService().authUserStream,
        initialData: null,
        child: _Wrapper(homeScreen: child ?? Container()),
      );
}

class _Wrapper extends StatelessWidget {
  final Widget homeScreen;
  const _Wrapper({required this.homeScreen, Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (AuthService.currentUser(context) == null) {
      return const AuthenticationScreen();
    }
    return homeScreen;
  }
}
