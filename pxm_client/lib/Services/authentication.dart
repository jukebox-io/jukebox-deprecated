// import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

// import 'package:google_sign_in/google_sign_in.dart';
import 'package:provider/provider.dart';

class User {
  String get displayName => 'demo user';
}

class AuthService {
  // final FirebaseAuth _auth = FirebaseAuth.instance;

  // auth change user stream
  Stream<User?> get authUserStream {
    // return _auth.authStateChanges();
    return const Stream.empty();
  }

  static User? currentUser(BuildContext context) => Provider.of<User?>(context);

  // sign in anon
  Future<User?> signInAnon() async {
    try {
      // final userCredential = await _auth.signInAnonymously();
      // return userCredential.user;
    } catch (e) {
      return null;
    }
  }

  // sign in with google
  Future<User?> signInWithGoogle() async {
    try {
      // Trigger the authentication flow
      // final googleUser = await GoogleSignIn().signIn();

      // Obtain the auth details from the request
      // final googleAuth = await googleUser?.authentication;

      // Create a new credential
      // final credential = GoogleAuthProvider.credential(
      //   accessToken: googleAuth?.accessToken,
      //   idToken: googleAuth?.idToken,
      // );

      // Once signed in, return the UserCredential
      // final userCredential = await _auth.signInWithCredential(credential);
      // return userCredential.user;
    } catch (e) {
      return null;
    }
  }

// sign in with email and password

// register with email and password

  // sign out
  Future<void> signOut() async {
    try {
      // await _auth.signOut();
    } catch (e) {
      return;
    }
  }
}
