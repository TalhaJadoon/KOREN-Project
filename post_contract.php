<!DOCTYPE html>
<html lang="en">	
	<head>
		<meta http-equiv="content-type" content="text/html; charset=UTF-8">
	    <meta charset="utf-8">
	    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	    <meta name="description" content="">
	    <meta name="author" content="">
	    <link rel="icon" href="content/svg/policy-icon.png">

	    <title>Intent System</title>

	    <!-- Bootstrap core CSS -->
	    <link href="css/bootstrap.css" rel="stylesheet">

	    <!-- Custom styles for this template -->
	    <link href="css/form-validation.css" rel="stylesheet">

	    <link rel="stylesheet" type="text/css" href="font-awesome-4.7.0/css/font-awesome.min.css">
	</head>

	<body class="bg-light">
		<?php

			$servername = "127.0.0.1";
            $username = "root";
            $password = "";
            $dbname = "catalog";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);

            if($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }
            else{

				$services = $_POST['services'];
				$qos = $_POST['qos'];
				$nodes = $_POST['nodes'];
				
				$loopQueryOk = true;
				$customQueryOk = true;

				if(isset($_POST['services'])){
					$sql =	"INSERT INTO `intent` " 
	            		.		"(`servicename`, `QoSType`, `ClientNodeName`) " 
	            		.	"VALUES " 
	            		.		"('".$services."','" .$qos."','" .$nodes."')";
	              	$result = $conn->query($sql);

	              	if ($result === TRUE) {
					    //echo "New record created successfully";
					    $loopQueryOk = true;
					} else{
						$loopQueryOk = false;
						echo	'<div class="container">'
					    	.		'<div class="row">' 
					    	.			'<div class="col-md-10 offset-1">'
					    	.				'<div class="alert alert-danger" role="alert" style="margin-top: 100px;">'
							.					'<h4 class="alert-heading"><i class="fa fa-exclamation-circle"></i> Error</h4>'
							.					'<ul><li>' 
							.						$conn->error
							.					'</li></ul>'
							.					'<hr>'
							.					'<p class="mb-0">' 
							.						'<ul><a href="index.php" class="alert-link">' 
							.							'<i class="fa fa-arrow-circle-left"></i> Go back' 
							.						'</a></ul>' 
							.					'</p>'
							.				'</div>'
							.			'</div>'
							.		'</div>'
							.	'</div>';
					}
				}

            $conn->close();
            $call = curl_init("http://127.0.0.1:5000/InsertflowsDB");
            $result=curl_exec ($call);
            curl_close($call);


            	if($loopQueryOk && $customQueryOk){
            		header('Location: index.php');
            	} else{
            		// do nothing
            	}
            	
            }

		?>
	</body>
</html>