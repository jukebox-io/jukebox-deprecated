import 'package:flutter/material.dart';

final ValueNotifier<bool> playerExpanded = ValueNotifier(false);

class MiniPlayer extends StatefulWidget {
  const MiniPlayer({Key? key}) : super(key: key);

  @override
  _MiniPlayerState createState() => _MiniPlayerState();
}

class _MiniPlayerState extends State<MiniPlayer> {
  @override
  Widget build(BuildContext context) {
    return const SizedBox();
  }
}
