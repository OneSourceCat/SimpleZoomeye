<?php

include("E:/School_of_software/information_security/holiday-learning/python/django/safecat/libs/GeoIP/geoipcity.inc");
include("E:/School_of_software/information_security/holiday-learning/python/django/safecat/libs/GeoIP/geoipregionvars.php");
$ip_str = $argv[1];
$gi = geoip_open("E:/School_of_software/information_security/holiday-learning/python/django/safecat/libs/GeoIP/GeoLiteCity.dat",GEOIP_STANDARD);
$record = geoip_record_by_addr($gi,$ip_str);
print json_encode($record);
geoip_close($gi);
return json_encode($record) ;

?>