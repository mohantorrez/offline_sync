<?php

  
    $connect = mysql_connect("localhost","root","") or die("Server unavailable now!");
  mysql_select_db("spritle");
function get_users()
{
  $user_info = array();
  $query = "select * from details";
  $query = mysql_query($query);
  while ($row = mysql_fetch_assoc($query)) 
  {
    $user_info[] = $row;
  }
  
  return $user_info;
}
function insert_list()
{
  $data_json = $_GET['data_json'];
  if(!empty($data_json))
  {
  $values[] = json_decode($data_json,true);
  foreach($values as $value)
  {
     $id = $value['id'];
     if($value['id'] == '')
     {
      $id = $value['id'];
     $author = $value['author'] ;
     $body = $value['body'];
     $title = $value['title'];
          $query = "insert into details (author,body,title) values ('$author','$body','$title')";
          var_dump($query);
          $query = mysql_query($query) or die(mysql_error());
     }
     elseif(!empty($value['id']) && $value['type'] != 'delete')
     {
      $id = $value['id'];
     $author = $value['author'] ;
     $body = $value['body'];
     $title = $value['title'];
          $query = "update details set author='$author',title='$title',body='$body' where id='$id'";
          var_dump($query);
          $query = mysql_query($query) or die(mysql_error());
     }
     elseif ($value['type'] == 'delete') 
     {
           $query = "delete from details where id='$id'";
           $query = mysql_query($query) or die(mysql_error());
     }
  } 
  }
  return $query;
}


$possible_url = array("insert_list", "get_users");

$value = "An error has occurred";

if (isset($_GET["action"]) && in_array($_GET["action"], $possible_url))
{
  switch ($_GET["action"])
    {
      case "insert_list":
        $value = insert_list();
        break;
      case "get_users":
        $value = get_users();
        break;
    }
}

exit(json_encode($value));

?>
