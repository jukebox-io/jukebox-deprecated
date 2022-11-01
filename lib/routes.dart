import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

final routerConfig = GoRouter(
  initialLocation: '/',
  routes: <GoRoute>[
    GoRoute(
      path: '/',
      builder: (context, state) => Scaffold(
        appBar: AppBar(
          title: const Text('xyz'),
        ),
      ),
    ),
  ],
);
