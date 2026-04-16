Future<void> runSequentialTasks() async {
  print("Starting task sequence...");

  await Future.delayed(Duration(seconds: 3));
  print("3-second setup complete.");

  String details = await fetchDetails();
  print(details);

  print("All tasks finished.");
}

Future<String> fetchDetails() => Future.value('Details Loaded.');
