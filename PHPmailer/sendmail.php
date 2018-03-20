<?php
  /**
   * Sets error header and json error message response.
   *
   * @param  String $messsage error message of response
   * @return void
   */
 @session_start(); 
  function errorResponse ($messsage) {
    header('HTTP/1.1 500 Internal Server Error');
    die(json_encode(array('message' => $messsage)));
  }

  header('Content-type: application/json');

            $count = "";

            $result = array();

            if(isset($_POST['email']) && isset($_POST['name']) && isset($_POST['message']))
            {
            $email1 = $_POST['email'];
            $name = $_POST['name'];
            $how_about_us =  $_POST['how_about_us'];
            $message = $_POST['message'];
            $subject = 'Clients Feedback';
            $email = trim($email1);
            $count = "";
            $br = "<br>";
            if($email == "")
            {
             $result = array(
                    "success" => false,
                    "message" => "Please enter email address."
                  );
            }

            elseif(!filter_var($email, FILTER_VALIDATE_EMAIL))
              {
             $result = array(
                    "success" => false,
                    "message" => "Please enter valid E-mail."
                  );
              }
            else
              {

 
$_REQUEST['datetime'] = date("Y-m-d H:i:s");

$headers  = "From: hedgefundsclient@gmail.com \r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: text/html; charset=UTF-8\r\n";

$message_to_user  = "<html><body>";
   
$message_to_user .= "<table width='100%' bgcolor='#e0e0e0' cellpadding='0' cellspacing='0' border='0'>";
   
$message_to_user .= "<tr><td>";
   
$message_to_user .= "<table align='center' width='100%' border='0' cellpadding='0' cellspacing='0' style='max-width:650px; background-color:#fff; font-family:Verdana, Geneva, sans-serif;'>";
    
$message_to_user .= "<thead>
  <tr height='80'>
  <th colspan='4' style='background-color:#f5f5f5; border-bottom:solid 1px #bdbdbd; font-family:Verdana, Geneva, sans-serif; color:#333; font-size:34px;' >Client's Feedback</th>
  </tr>
             </thead>";
    
$message_to_user .= "<tbody>
             <tr align='center' height='50' style='font-family:Verdana, Geneva, sans-serif;'>
       <td style='background-color:#00a2d1; text-align:center;'><a href='#' style='color:#fff; text-decoration:none;'>Name: </a></td>
       <td style='background-color:#00a2d1; text-align:center;'><a href='#' style='color:#fff; text-decoration:none;'>" . ucfirst($name) . "</a></td>
       </tr>


        <tr align='center' height='50' style='font-family:Verdana, Geneva, sans-serif;'>
       <td style='text-align:center;'><p style='text-decoration:none;'>Email: </p></td>
       <td style='text-align:center;'><p style='text-decoration:none;'>" . $email . "</p></td>
       </tr>

       <tr align='center' height='50' style='font-family:Verdana, Geneva, sans-serif;'>
       <td style='text-align:center;'><p style='text-decoration:none;'>How They Hear About Us ? </p></td>
       <td style='text-align:center;'><p style='text-decoration:none;'>" . $how_about_us . "</p></td>
       </tr>

      <tr align='center' height='50' style='font-family:Verdana, Geneva, sans-serif;'>
       <td style='text-align:center;'><p  style='text-decoration:none;'>Feedback: </p></td>
       <td style='text-align:center;'><p  style='text-decoration:none;'>" . $message . "</p></td>
       </tr>

              </tbody>";
    
$message_to_user .= "</table>";
   
$message_to_user .= "</td></tr>";
$message_to_user .= "</table>";
   
$message_to_user .= "</body></html>";


$subject_user = "Client's Feedback";

  require './vender/php_mailer/PHPMailerAutoload.php';
  $mail = new PHPMailer;
  //$mail->CharSet = 'UTF-8';
  
                //$mail->isSMTP();                                      // Set mailer to use SMTP
                $mail->Host = 'smtp.gmail.com';  // Specify main and backup SMTP servers
                $mail->SMTPAuth = true;                               // Enable SMTP authentication
                $mail->Username = 'hedgefundsclient@gmail.com';                 // SMTP username
                $mail->Password = 'hedgefundsclient123';                           // SMTP password
                $mail->SMTPSecure = 'ssl';                            // Enable TLS encryption, `ssl` also accepted
                $mail->Port = 465;                                    // TCP port to connect to
                
                $mail->From = $email;
                $mail->FromName = $name;
                $mail->addAddress('hedgefundsclient@gmail.com', $name);     // Add a recipient

                $mail->Subject = $subject;
                $mail->Body    = $message_to_user;
                $mail->IsHTML(true); 
                //$mail->AltBody = 'This is the body in plain text for non-HTML mail clients';

                if(!$mail->send()) {
                 //echo "Error in Sending email: " . $mail->ErrorInfo;
                  $count = 2;
                  
                  $result = array(
                    "success" => false,
                    "message" => "Unable To Send Mail. Please Try Again.",
                    "mailer_error" => 'Mailer Error: '.$mail->ErrorInfo
                  );

                } else {
                  //echo 'Message has been sent';
                  $result = array(
                    "success" => true,
                    "message" => "Thank you for the feedback."
                  );
                  
                }

               
               // if (isset($_GET["callback"])) {
                  //echo 'contact_callback('. json_encode($result) .');';
                //}
                  
                  }
                }
                
                $_SESSION['result']  = $result;

                header('Location:../about.php');
                  
?>
