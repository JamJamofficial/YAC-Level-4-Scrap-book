// import 'package:flutter/material.dart';

// void main() {
//   runApp(const MyApp());
// }

// class MyApp extends StatelessWidget {
//   const MyApp({super.key});

//   // This widget is the root of your application.
//   @override
//   Widget build(BuildContext context) {
//     return MaterialApp(
//       title: 'Flutter Demo',
//       theme: ThemeData(
//         // This is the theme of your application.
//         //
//         // TRY THIS: Try running your application with "flutter run". You'll see
//         // the application has a purple toolbar. Then, without quitting the app,
//         // try changing the seedColor in the colorScheme below to Colors.green
//         // and then invoke "hot reload" (save your changes or press the "hot
//         // reload" button in a Flutter-supported IDE, or press "r" if you used
//         // the command line to start the app).
//         //
//         // Notice that the counter didn't reset back to zero; the application
//         // state is not lost during the reload. To reset the state, use hot
//         // restart instead.
//         //
//         // This works for code too, not just values: Most code changes can be
//         // tested with just a hot reload.
//         colorScheme: .fromSeed(seedColor: Colors.deepPurple),
//       ),
//       home: const MyHomePage(title: 'YAC App'),
//     );
//   }
// }

// class MyHomePage extends StatefulWidget {
//   const MyHomePage({super.key, required this.title});

//   // This widget is the home page of your application. It is stateful, meaning
//   // that it has a State object (defined below) that contains fields that affect
//   // how it looks.

//   // This class is the configuration for the state. It holds the values (in this
//   // case the title) provided by the parent (in this case the App widget) and
//   // used by the build method of the State. Fields in a Widget subclass are
//   // always marked "final".

//   final String title;

//   @override
//   State<MyHomePage> createState() => _MyHomePageState();
// }

// class _MyHomePageState extends State<MyHomePage> {
//   int _counter = 0;

//   void _incrementCounter() {
//     setState(() {
//       // This call to setState tells the Flutter framework that something has
//       // changed in this State, which causes it to rerun the build method below
//       // so that the display can reflect the updated values. If we changed
//       // _counter without calling setState(), then the build method would not be
//       // called again, and so nothing would appear to happen.
//       _counter++;
//     });
//   }

//   @override
//   Widget build(BuildContext context) {
//     // This method is rerun every time setState is called, for instance as done
//     // by the _incrementCounter method above.
//     //
//     // The Flutter framework has been optimized to make rerunning build methods
//     // fast, so that you can just rebuild anything that needs updating rather
//     // than having to individually change instances of widgets.
//     return Scaffold(
//       appBar: AppBar(
//         // TRY THIS: Try changing the color here to a specific color (to
//         // Colors.amber, perhaps?) and trigger a hot reload to see the AppBar
//         // change color while the other colors stay the same.
//         backgroundColor: Theme.of(context).colorScheme.inversePrimary,
//         // Here we take the value from the MyHomePage object that was created by
//         // the App.build method, and use it to set our appbar title.
//         title: Text(widget.title),
//       ),
//       body: Center(
//         // Center is a layout widget. It takes a single child and positions it
//         // in the middle of the parent.
//         child: Column(
//           // Column is also a layout widget. It takes a list of children and
//           // arranges them vertically. By default, it sizes itself to fit its
//           // children horizontally, and tries to be as tall as its parent.
//           //
//           // Column has various properties to control how it sizes itself and
//           // how it positions its children. Here we use mainAxisAlignment to
//           // center the children vertically; the main axis here is the vertical
//           // axis because Columns are vertical (the cross axis would be
//           // horizontal).
//           //
//           // TRY THIS: Invoke "debug painting" (choose the "Toggle Debug Paint"
//           // action in the IDE, or press "p" in the console), to see the
//           // wireframe for each widget.
//           mainAxisAlignment: .center,
//           children: [
//             const Text('You have pushed the button this many times:'),
//             Text(
//               '$_counter',
//               style: Theme.of(context).textTheme.headlineMedium,
//             ),
// const Text('You have pushed the button this many times:'),
// Text(
//               '$_counter',
//               style: Theme.of(context).textTheme.headlineMedium,
//             ),
//           ],
//         ),
//       ),
//       floatingActionButton: FloatingActionButton(
//         onPressed: _incrementCounter,
//         tooltip: 'Increment',
//         child: const Icon(Icons.add),
//       ),
//     );
//   }
// }


import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(MaterialApp(
    title: 'Mood Tracker',
    theme: ThemeData(primarySwatch: Colors.deepPurple),
    home: MoodTrackerApp(),
  ));
}

class MoodTrackerApp extends StatefulWidget {
  @override
  _MoodTrackerAppState createState() => _MoodTrackerAppState();
}

class _MoodTrackerAppState extends State<MoodTrackerApp> {
  // Use 10.0.2.2 for Android Emulator, 127.0.0.1 for iOS Simulator
  final String baseUrl = 'http://localhost:8000'; 
  
  bool _isLoading = true;
  String _latestMood = "Loading...";
  String _latestEmoji = "⏳";
  List<dynamic> _moodHistory = [];

  @override
  void initState() {
    super.initState();
    _fetchData();
  }

  // Fetch both the latest mood and the history from the backend
  Future<void> _fetchData() async {
    setState(() => _isLoading = true);
    try {
      final latestRes = await http.get(Uri.parse('$baseUrl/mood/latest'));
      final historyRes = await http.get(Uri.parse('$baseUrl/mood/history'));

      if (latestRes.statusCode == 200 && historyRes.statusCode == 200) {
        final latestData = jsonDecode(latestRes.body);
        final historyData = jsonDecode(historyRes.body);

        setState(() {
          _latestMood = latestData['mood'];
          _latestEmoji = latestData['emoji'];
          _moodHistory = historyData;
        });
      }
    } catch (e) {
      print("Error fetching data: $e");
      setState(() {
        _latestMood = "Error connecting to server";
        _latestEmoji = "⚠️";
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  // Send a new mood to the backend
  Future<void> _recordMood(String mood, String emoji) async {
    // Optimistic UI update
    setState(() {
      _latestMood = mood;
      _latestEmoji = emoji;
      _isLoading = true;
    });

    try {
      final url = Uri.parse('$baseUrl/mood');
      await http.post(
        url,
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"mood": mood, "emoji": emoji}),
      );
      // Re-fetch data to update the history list
      await _fetchData(); 
    } catch (e) {
      print("Error saving mood: $e");
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Failed to save mood to server')),
      );
      setState(() => _isLoading = false);
    }
  }

  // Helper widget to build mood buttons
  Widget _buildMoodButton(String mood, String emoji, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 4.0),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(backgroundColor: color),
        onPressed: () => _recordMood(mood, emoji),
        child: Text('$emoji $mood', style: TextStyle(color: Colors.white)),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Mood Tracker'),
        actions: [
          IconButton(
            icon: Icon(Icons.refresh),
            onPressed: _fetchData, // Manual refresh button
          )
        ],
      ),
      body: Column(
        children: [
          // Top Section: Latest Mood Display
          Container(
            padding: EdgeInsets.all(32),
            width: double.infinity,
            color: Colors.deepPurple.shade50,
            child: Column(
              children: [
                Text(
                  'Current Mood',
                  style: TextStyle(fontSize: 18, color: Colors.grey.shade700),
                ),
                SizedBox(height: 10),
                _isLoading 
                    ? CircularProgressIndicator()
                    : Text(
                        '$_latestEmoji $_latestMood',
                        style: TextStyle(fontSize: 40, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
              ],
            ),
          ),
          
          // Middle Section: Control Panel
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Wrap(
              alignment: WrapAlignment.center,
              spacing: 8.0,
              runSpacing: 8.0,
              children: [
                _buildMoodButton('Happy', '😁', Colors.green),
                _buildMoodButton('Calm', '😌', Colors.blue),
                _buildMoodButton('Stressed', '😫', Colors.orange),
                _buildMoodButton('Sad', '😢', Colors.grey.shade700),
              ],
            ),
          ),
          Divider(),
          
          // Bottom Section: History List
          Expanded(
            child: _moodHistory.isEmpty
                ? Center(child: Text('No mood history yet.'))
                : ListView.builder(
                    itemCount: _moodHistory.length,
                    itemBuilder: (context, index) {
                      final item = _moodHistory[index];
                      return ListTile(
                        leading: Text(item['emoji'], style: TextStyle(fontSize: 24)),
                        title: Text(item['mood']),
                        trailing: Text(item['timestamp'] ?? ''),
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }
}