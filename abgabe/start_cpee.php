<?php
  $curl_handle = curl_init();
  curl_setopt($curl_handle, CURLOPT_URL, "https://cpee.org/flow/start/xml/");
  curl_setopt($curl_handle, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($curl_handle, CURLOPT_POST, true);
  $start = '------'."\r\n".'Content-Disposition: form-data; name="behavior"'."\r\n\r\n".'fork_running'."\r\n".'------'."\r\n".'Content-Disposition: form-data; name="xml"'."\r\n".'Content-Type: text/xml'."\r\n\r\n";
  $xml = file_get_contents('production.xml');
  $end = "\r\n".'------'."\r\n"; 
  $body = '';
  $body .= $start.$xml.$end;
  //var_dump($body);
  //curl_setopt($curl_handle, CURLOPT_HTTPHEADER, array('Content-Type: multipart/form-data;boundary=----','Content-Length: '.strlen($body)));
  curl_setopt($curl_handle, CURLOPT_HTTPHEADER, array('Content-Type: multipart/form-data;boundary=----'));
  curl_setopt($curl_handle, CURLOPT_POSTFIELDS, $body);
  $result = curl_exec($curl_handle);
  if(curl_error($curl_handle)) {
    print(curl_error($curl_handle));
  }
  else {
    var_dump($result);
  }
  curl_close($curl_handle);
?>