# code
code for security
1.参照wazuh的方式，利用python写的HIDS。
2.该HIDS包含解码器和规则。其中规则是JSON格式的数据，可自行按照例子添加；解码器会对规则进行解读，识别具体是哪种威胁
3.预警信息会写入数据库与预警文件
