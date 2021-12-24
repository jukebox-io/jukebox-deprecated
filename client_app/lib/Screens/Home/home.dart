import 'package:flutter/material.dart';
import 'package:material_design_icons_flutter/material_design_icons_flutter.dart';
import 'package:pxm/CustomWidgets/back_button_handler.dart';
import 'package:pxm/CustomWidgets/gradient_containers.dart';
import 'package:pxm/CustomWidgets/mini_player.dart';
import 'package:pxm/Helpers/config.dart';
import 'package:pxm/Screens/Home/home_page.dart';
import 'package:pxm/Screens/MoreItems/more_items.dart';
import 'package:pxm/Screens/Playlist/playlist.dart';
import 'package:salomon_bottom_bar/salomon_bottom_bar.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _selectedIndex = ValueNotifier<int>(0);
  final pageController = PageController();

  @override
  Widget build(BuildContext context) {
    return GradientContainer(
      child: BackButtonHandler(
        onBackPressed: () {
          if (_selectedIndex.value == 0) return true;
          _onItemTapped(0);
          return false;
        },
        child: Scaffold(
          resizeToAvoidBottomInset: false,
          backgroundColor: Colors.transparent,
          body: SafeArea(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  Expanded(
                    child: PageView(
                      controller: pageController,
                      onPageChanged: (index) {
                        _selectedIndex.value = index;
                      },
                      children: <Widget>[
                        const HomePage(),
                        const PlaylistScreen(),
                        Center(
                          child: TextButton(
                            onPressed: () {
                              currentTheme.switchTheme(
                                isDark: currentTheme.currentThemeMode() ==
                                    ThemeMode.light,
                              );
                            },
                            child: const Text('Press'),
                          ),
                        ),
                        const MoreItemsScreen(),
                      ],
                    ),
                  ),
                  const MiniPlayer(),
                ],
              ),
            ),
          ),
          bottomNavigationBar: SafeArea(
            child: ValueListenableBuilder(
              valueListenable: _selectedIndex,
              builder: (BuildContext context, int value, Widget? child) {
                return AnimatedContainer(
                  duration: const Duration(microseconds: 100),
                  height: 60 *
                      (MediaQuery.of(context).size.height - value) /
                      (MediaQuery.of(context).size.height - 76),
                  child: SalomonBottomBar(
                    currentIndex: value,
                    onTap: (index) {
                      _onItemTapped(index);
                    },
                    items: <SalomonBottomBarItem>[
                      SalomonBottomBarItem(
                        icon: const Icon(
                          Icons.home_rounded,
                          size: 30,
                        ),
                        title: const Text('Home'),
                        selectedColor: Theme.of(context).colorScheme.secondary,
                      ),
                      SalomonBottomBarItem(
                        icon: const Icon(
                          MdiIcons.playlistPlay,
                          size: 30,
                        ),
                        title: const Text('Playlist'),
                        selectedColor: Theme.of(context).colorScheme.secondary,
                      ),
                      SalomonBottomBarItem(
                        icon: const Icon(
                          Icons.my_library_music_rounded,
                          size: 30,
                        ),
                        title: const Text('Your Library'),
                        selectedColor: Theme.of(context).colorScheme.secondary,
                      ),
                      SalomonBottomBarItem(
                        icon: const Icon(
                          Icons.apps_rounded,
                          size: 30,
                        ),
                        title: const Text('More'),
                        selectedColor: Theme.of(context).colorScheme.secondary,
                      ),
                    ],
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }

  void _onItemTapped(int index) {
    _selectedIndex.value = index;
    pageController.animateToPage(
      index,
      duration: const Duration(milliseconds: 400),
      curve: Curves.ease,
    );
  }

  @override
  void dispose() {
    pageController.dispose();
    super.dispose();
  }
}
