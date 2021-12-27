import 'package:flutter/material.dart';
import 'package:pxm/Services/authentication.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    var userName = AuthService.currentUser(context)?.displayName;
    if (userName == null || userName == '') {
      userName = 'Anonymous';
    }

    userName = userName.split(' ').first.trim();

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Text(
              'Hello ',
              style: TextStyle(
                fontSize: 50,
              ),
            ),
            Text(
              '$userName,',
              style: const TextStyle(
                fontSize: 50,
                color: Colors.green,
              ),
            ),
          ],
        ),
        const SizedBox(height: 50),
        Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton(
              onPressed: () async {
                await AuthService().signOut();
              },
              child: const Text('Log Out'),
            ),
          ],
        ),
      ],
    );
  }
}
