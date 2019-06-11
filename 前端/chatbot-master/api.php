<?php


require_once "chatbot/Chatbot.php";
require_once "chatbot/Config.php";

$config = new Config();
define("LOG", $config->log);
header(LOG ? "Content-Type: text/plain; charset=utf-8" : "Content-Type: application/json; charset=utf-8");
error_reporting(LOG ? E_ALL : JSON_ERROR_NONE);

 function gbk2utf8($data){
    if(is_array($data)){
      return array_map('gbk2utf8', $data);
    }
    return iconv('gbk','utf-8',$data);
  }
$result = array(
    'status' => 'error',
    'type' => 'empty',
    'message' => 'empty message ...',
    'data' => 'empty',
	'groove'=>'empty'
);
$user_input=$_REQUEST['userInput'];
$groove_current=$_REQUEST['groove'];
//$groove_current='0, 0, 0, 1, 1, 0';
//echo gettype($groove_current);
// check request type
if (!isset($_REQUEST['requestType']) || !isset($_REQUEST['userInput'])) {
    $result['status'] = 'error';
    $result['type'] = $_REQUEST['requestType'];
    $result['message'] = 'requestType and userInput is required ...';
    $result['data'] = 'empty';
} else {


    // 若用户上传了userId则用uid当做用户唯一标识否则用ip
    $userId = isset($_REQUEST['userId']) ? $_REQUEST['userId'] : $_SERVER['REMOTE_ADDR'];
    LOG && print "userId : " . $userId . "\n";

    // initialize chatbot
    $chatbot = new Chatbot($config, $userId);


    // talk
    if ($_REQUEST['requestType'] == 'talk') {
		//echo $groove_current;
		$user_input=iconv('UTF-8','GB2312',$user_input);
		exec("python test.py $groove_current $user_input 2>&1",$res);
		//$json= json_encode(gbk2utf8($res),JSON_UNESCAPED_UNICODE);
		//echo $json;
		//print_r( $res);
        //$res = $chatbot->talk($_REQUEST['userInput']);
        //$data = $chatbot->getData();
        $result['status'] = 'success';
        $result['type'] = 'talk';
        //$result['message'] = trim(preg_replace("/\s+/", " ", $res));
		$result['message'] = $res[1];
		$result['groove'] = $res[0];
        //$result['data'] = $res[1];
    } elseif ($_REQUEST['requestType'] == 'forget') {
        //$chatbot->forget();
        $result['status'] = 'success';
        $result['type'] = 'forget';
        $result['message'] = 'forgetting completed ...';
        $result['data'] = 'empty';
    } else {
        $result['status'] = 'error';
        $result['type'] = $_REQUEST['requestType'];
        $result['message'] = 'invalid request type ...';
        $result['data'] = 'empty';
    }


}

if (LOG) {
    print "\n";
    print_r($result);
    print "\n";
} else {
    echo json_encode(gbk2utf8($result),JSON_UNESCAPED_UNICODE);
}



