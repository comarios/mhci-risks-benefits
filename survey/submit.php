<?php
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Create a unique identifier for the file name using the prolific id or the timestamp
    $identifier = isset($_POST['prolific-id']) && !empty($_POST['prolific-id']) ? $_POST['prolific-id'] : time();

    // Set path to store the answers
    $folderPath = ''; // PLEASE REPLACE THIS EMPTY STRING WITH YOUR SERVER PATH
    $fileName = 'annotation_' . $identifier . '.json'; 
    $filePath = $folderPath . $fileName;

    // Sort the POST data alphabetically by keys
    ksort($_POST);

    // Convert POST data to JSON format
    $jsonData = json_encode($_POST);

    // Save the JSON data to the file on the server
    file_put_contents($filePath, $jsonData);

    // Optionally, send a response back to the client
    echo "Data saved to file: " . $fileName;
}
?>