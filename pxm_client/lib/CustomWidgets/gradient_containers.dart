import 'package:flutter/material.dart';
import 'package:pxm/Helpers/config.dart';

class GradientContainer extends StatefulWidget {
  final Widget child;
  final bool? opacity;

  const GradientContainer({required this.child, this.opacity, Key? key})
      : super(key: key);

  @override
  _GradientContainerState createState() => _GradientContainerState();
}

class _GradientContainerState extends State<GradientContainer> {
  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: Theme.of(context).brightness == Brightness.dark
              ? (widget.opacity == true
                  ? currentTheme.getTransBackGradient()
                  : currentTheme.getBackGradient())
              : currentTheme.getLightBackGradient(),
        ),
      ),
      child: widget.child,
    );
  }
}
