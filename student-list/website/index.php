<html>
    <head>
        <title>POZOS</title>
    </head>

    <body>
        <h1>Student Checking App</h1>
        <ul>
            <form action="" method="POST">
                <label>Enter student name:</label><br />
                <br />
                <label>Username:</label><br />
                <input type="text" name="username" placeholder="Username" required/>
                <br /><br />
                <label>Password:</label><br />
                <input type="password" name="password" placeholder="Password" required/>
                <br /><br />
                <button type="submit" name="submit">List Student</button>
            </form>

            <?php
              if ($_SERVER['REQUEST_METHOD'] == "POST" && isset($_POST['submit'])) {
                  $username = $_POST['username'];
                  $password = $_POST['password'];

                  $context = stream_context_create(array(
                      "http" => array(
                          "header" => "Authorization: Basic " . base64_encode("$username:$password"),
                      )
                  ));

                  $url = 'http://api:5000/pozos/api/v1.0/get_student_ages';
                  $response = file_get_contents($url, false, $context);

                  if ($response === false) {
                      echo "<p style='color:red;'>Error fetching data from API</p>";
                  } else {
                      $list = json_decode($response, true);
                      echo "<p style='color:red; font-size: 20px;'>This is the list of the student with age</p>";
                      if (isset($list["student_ages"])) {
                          foreach ($list["student_ages"] as $key => $value) {
                              echo "- $key is $value years old <br>";
                          }
                      } else {
                          echo "<p style='color:red;'>No student ages found or API response structure is invalid</p>";
                      }
                  }
              }
            ?>
        </ul>
    </body>
</html>

