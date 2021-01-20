<html lang="en"><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" href="content/svg/policy-icon.png">

    <title>DNA *IBN: AI Driven Networking for KOREN*</title>

    <!-- Bootstrap core CSS -->
    <link href="css/bootstrap.css" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="css/form-validation.css" rel="stylesheet">

    <link rel="stylesheet" type="text/css" href="font-awesome-4.7.0/css/font-awesome.min.css">
  </head>

  <body class="" style="background-color: #b3b3ff !important;">

    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <a class="navbar-brand" href="#">
        DNA *IBN: AI Driven Networking for KOREN*&emsp;&emsp;&emsp;&emsp;
      </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item active">
            <a class="nav-link" href="#">Normal-Portal <span class="sr-only">(current)</span></a>
          </li>

          <li class="nav-item">
            <a class="nav-link" href="ML.php">ML-Portal</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="contracts.php">Intent-Status</a>
          </li>
        </ul>
      </div>
    </nav>

    <div class="container">
      <div class="py-5 text-center">
        <img class="d-block mx-auto mb-4" src="content/svg/portal-logo.png" alt="" width="72" height="72">
        <h2>Intent Reservation</h2>
        <p class="lead">Specify User Requirements</p>
      </div>

      <div class="row">
        <div class="col-md-4 order-md-2 mb-4">
          <?php

            $servername = "127.0.0.1";
            $username = "root";
            $password = "";
            $dbname = "catalog";

            // Create connection
            $conn = new mysqli($servername, $username, $password, $dbname);

            // Check connection
            if($conn->connect_error) {
                die("Connection failed: " . $conn->connect_error);
            }
            else{

              $sql =  "SELECT COUNT(*) AS number_of_contracts FROM `intent` ";
              $result1 = $conn->query($sql);

              if($result1->num_rows > 0) {
                while($row = $result1->fetch_assoc()) {
                  echo  '<h4 class="d-flex justify-content-between align-items-center mb-3">' 
                    .     '<span class="text-muted">'
                    .         'Service List'
                    .         '<img class="mx-auto mb-1" src="content/svg/contract-logo.png" alt="" width="25" height="25">'
                    .     '</span>'                  
                    .     '<span class="text-muted" title="Sync all intents">' 
                    .       '<form action="sync_contracts.php">'
                    .         '<button class="btn fa fa-refresh fa-md text-muted" ></button>' 
                    .       '</form>'
                    .     '</span>'
                    .     '<span class="badge badge-info badge-pill">' . $row['number_of_contracts'] . '</span>'
                    .   '</h4>';
                }
              }
              else{
                echo  '<h4 class="d-flex justify-content-between align-items-center mb-3">' 
                  .     '<span class="text-muted">'
                  .         'Intents'
                  .         '<img class="mx-auto mb-1" src="content/svg/contract-logo.png" alt="" width="25" height="25">'
                  .     '</span>'
                  .     '<span class="badge badge-info badge-pill">0</span>'
                  .   '</h4>';
              }

              $sql =  "SELECT cont.`Intentid`, cont.`servicename`, cont.`QoSType`, cont.`ClientNodeName`, cont.`status`" 
                    . "FROM `intent` AS cont "
                    //. "INNER JOIN architectures_supported AS arch ON cont.`arch_id` = arch.`id` " 
                    . "ORDER BY cont.`Intentid`";
              $result2 = $conn->query($sql);

              echo '<ul class="list-group mb-3">';
              if ($result2->num_rows > 0) {
                  // output data of each row
                  while($row = $result2->fetch_assoc()) {
                      $iconClass = ($row['status']==2?'fa-check-square text-success':'fa-refresh text-warning');
                      $iconTitle = ($row['status']==0?'synced':'sync');

                      echo  '<li class="list-group-item d-flex justify-content-between lh-condensed">' 
                        .     '<div>'
                        .       '<h6 class="my-0">'
                        .         '<a href="graph.php?id=' . $row['Intentid'] . '">' 
                        .           $row['ClientNodeName'] . ' - ' . $row['servicename'] 
                        .         '</a>'
                        .       '</h6>' 
                        .       '<small class="text-muted">' 
                        .         'QoS:' . $row['QoSType']
                        .       '</small>' 
                        .     '</div>' 
                        .     '<span class="text-muted">' 
                        .       '<i class="fa fa-lg ' . $iconClass . '" title="' . $iconTitle . '"></i>' 
                        .     '</span>' 
                        .   '</li>';
                      //echo "id: " . $row["id"]. " - Name: " . $row["firstname"]. " " . $row["lastname"]. "<br>";
                  }
              } else {
                  echo  '<li class="list-group-item d-flex justify-content-between lh-condensed">' 
                    .     '<div>'
                    .       '<h6 class="my-0">No intents found.</h6>' 
                    .     '</div>'
                    .   '</li>';
              }

              echo '</ul>';
            }
          ?>
        </div>
        <div class="col-md-8 order-md-1">

          <h4 class="mb-3">E2E- Intent Reservation
           <img class="mx-auto mb-2" src="content/svg/e2e-logo.png" alt="" width="50" height="50">
          </h4>
          <form class="needs-validation" novalidate="" action="post_contract.php" method="POST">
            <div class="row">
              <div class="col-md-5 mb-3">
                <label for="name">Source Node Name
                   <img class="mx-auto mb-1" src="content/svg/name-logo.png" alt="" width="25" height="25"> 
                </label>
                <?php
                  $sql =  "SELECT node.`NodeName`" 
                    . "FROM `nodes` AS node "
                    . "ORDER BY node.`NodeName`";
                  $result3 = $conn->query($sql);

                  echo  '<select class="custom-select d-block w-100" id="nodes" name="nodes" required="">';
                  echo '<option value="">Select...</option>';

                  while($row = $result3->fetch_assoc()) {
                    echo  '<option value="' . $row['NodeName'] . '">' 
                      .     $row['NodeName']
                      .   '</option>';
                  }

                  echo '</select>';

                ?>

                <div class="invalid-feedback">
                  Please select a Node.
                </div>
<!--                <input type="text" class="form-control" id="name" name="name" placeholder="Name Your Intent" required="">
                <div class="invalid-feedback">
                  Intent name is required.
                </div>
-->              </div>
              <div class="col-md-5 mb-3">
                <label for="architecture">Select Service
                  <img class="mx-auto mb-1" src="content/svg/archlogo.png" alt="" width="25" height="25"></label>
                <!--<select class="custom-select d-block w-100" id="architecture" name="architecture" required="">
                  <option value="">Choose...</option>
				-->
                <?php
                  $sql =  "SELECT service.`servicename`, service.`ProviderNodeName` FROM `service` AS service WHERE service.`status` = 0 ORDER BY service.`servicename`";
                  $result4 = $conn->query($sql);

                  echo  '<select class="custom-select d-block w-100" id="services" name="services" required="">';
                  echo '<option value="">Select...</option>';

                  while($row = $result4->fetch_assoc()) {
                    echo  '<option value="' . $row['servicename'].'">' 
                      .     $row['servicename'] . $row['ProviderNodeName'] 
                      .   '</option>';
                  }

                  echo '</select>';

                ?>
                  
                </select>
                <div class="invalid-feedback">
                  Please select a Service.
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-5 mb-3">
                <label for="orchestrator">QoS
                </label>
                <?php
                  $sql =  "SELECT qos.`QoSType`, qos.`priority` " 
                    . "FROM `qos` AS qos "
                    . "ORDER BY qos.`priority`";
                  $result5 = $conn->query($sql);

                  echo  '<select class="custom-select d-block w-100" id="qos" name="qos" required="">';
                  echo '<option value="">Select...</option>';

                  while($row = $result5->fetch_assoc()) {
                    echo  '<option value="' . $row['QoSType'] . '">' 
                      .     $row['QoSType']  
                      .   '</option>';
                  }

                  echo '</select>';

                  $conn->close();
                ?>
                <div class="invalid-feedback">
                  Please select QoS Type.
                </div>
              </div>
            </div>     
            
            <hr class="mb-4">
            <button class="btn btn-info btn-lg btn-block" type="submit">Submit The Intent Without ML</button>
          </form>
        </div>
      </div>

      <footer class="my-5 pt-5 text-muted text-center text-small">
        <p class="mb-1">© 2020 NCL - Intent System</p>
        <ul class="list-inline">
          <li class="list-inline-item"><a href="http://ncl.jejunu.ac.kr/ncl427/">Affiliation</a></li>
          <li class="list-inline-item"><a href="http://ncl.jejunu.ac.kr/ncl427/#profile-talha">Developer</a></li>
          <li class="list-inline-item"><a href="http://www.jejunu.ac.kr/">Institution</a></li>
        </ul>
      </footer>
    </div>

    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="js/jquery-3.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script>window.jQuery || document.write('<script src="js/jquery-slim.min.js"><\/script>')</script>
    <script src="js/popper.js"></script>
    <script src="js/bootstrap.js"></script>
    <script src="js/holder.js"></script>
    <script>
      // Example starter JavaScript for disabling form submissions if there are invalid fields
      (function() {
        'use strict';

        window.addEventListener('load', function() {
          // Fetch all the forms we want to apply custom Bootstrap validation styles to
          var forms = document.getElementsByClassName('needs-validation');

          // Loop over them and prevent submission
          var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
              if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
              }
              form.classList.add('was-validated');
            }, false);
          });
        }, false);
      })();

      //$(".list-group li").last().fadeOut();
      $("ul.list-group li").last().attr("style", "display: none !important;" );
      setTimeout(function(){
        $("ul.list-group li").last().removeAttr("style");
        $("ul.list-group li").last().attr("style", "background-color: cornsilk;" );
        setTimeout(function(){
          $("ul.list-group li").last().removeAttr("style");
        }, 200);
      }, 150);
      //console.log($("ul.list-group li").last());

      $(function(){
        var requiredCheckboxes = $('.snssaiChkBx :checkbox[required]');
        requiredCheckboxes.change(function(){
            if(requiredCheckboxes.is(':checked')) {
                requiredCheckboxes.removeAttr('required');
            } else {
                requiredCheckboxes.attr('required', 'required');
            }
        });
      });

      $('#cSnssai').click(function(){
        toggleCustomSnssai();
      });

      function toggleCustomSnssai(){
        if($('#cSnssai').is(':checked')){
          $('#customSliceDiv').show();
        } else{
          $('#customSliceDiv').hide();
        }
      }

      function replaceCustomQoSWithText(){
        /*var replaced = $("body").html().replace('QoS:127','QoS:C');
        $("body").html(replaced);*/
      }

      $("body").ready(function(){
        replaceCustomQoSWithText();
        toggleCustomSnssai();
      });

    </script>
  

</body></html>