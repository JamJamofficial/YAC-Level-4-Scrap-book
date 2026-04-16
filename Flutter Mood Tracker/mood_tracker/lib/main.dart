import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: MoodScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

class MoodScreen extends StatefulWidget {
  const MoodScreen({super.key});

  @override
  State<MoodScreen> createState() => _MoodScreenState();
}

class _MoodScreenState extends State<MoodScreen> {
  String currentMood = "Loading...";

  @override
  void initState() {
    super.initState();
    fetchMood();
  }

  Future<void> fetchMood() async {
    try {
      final response = await http.get(Uri.parse('http://10.0.2.2:8000/mood'));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);

        setState(() {
          currentMood = data['mood'];
        });
      } else {
        setState(() {
          currentMood = "Error loading mood";
        });
      }
    } catch (e) {
      setState(() {
        currentMood = "Server not reachable";
      });
    }
  }

  // 🔹 POST mood to backend
  Future<void> sendMood(String mood) async {
    try {
      await http.post(
        Uri.parse('http://10.0.2.2:8000/mood'),
        headers: {"Content-Type": "application/json"},
        body: jsonEncode({"mood": mood}),
      );

      fetchMood(); // refresh after sending
    } catch (e) {
      print("Error sending mood: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Mood Tracker"), centerTitle: true),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text("Last recorded mood:", style: TextStyle(fontSize: 18)),

              const SizedBox(height: 10),

              Text(
                currentMood,
                style: const TextStyle(
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 40),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => sendMood("Happy"),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 20),
                  ),
                  child: const Text("😊 Happy", style: TextStyle(fontSize: 20)),
                ),
              ),

              const SizedBox(height: 15),

              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: () => sendMood("Sad"),
                  style: ElevatedButton.styleFrom(
                    padding: const EdgeInsets.symmetric(vertical: 20),
                  ),
                  child: const Text("😢 Sad", style: TextStyle(fontSize: 20)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
