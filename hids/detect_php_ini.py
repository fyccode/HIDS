import re

file_path = '/opt/lampp/etc/php.ini'
print('======正在对php.ini配置项进行检测======')
# 对php.ini进行安全配置检查
with open(file_path,'r') as fp:
    content = fp.readlines()
for i in content:
    if re.findall(r'^magic_quotes_gpc\s?=',i) != []:
        if 'Off' in i.strip():
            print('警告: magic_quotes_gpc功能未开启,建议开启该功能以防止特殊符号注入')
    if re.findall(r'^display_errors\s?=',i) != []:
        if 'On' in i.strip():
            print('警告: display_errors功能开启中,建议非调试模式下关闭该功能')
    if re.findall(r'^allow_url_fopen\s?=',i) != []:
        if 'On' in i.strip():
            print('警告: allow_url_fopen开启中')
    if re.findall(r'^allow_url_include\s?=',i) != []:
        if 'On' in i.strip():
            print('警告: allow_url_include开启中')
    if re.findall(r'^open_basedir\s?=',i) != []:
        print('警告： open_basedir功能开启中')
    if re.findall(r'^disable_functions=',i) != []:
        if re.findall(r'^disable_functions=(.+?)\n',i) == []:
            print('警告: 检测到未禁用任何危险函数')
    if re.findall(r'^expose_php\s?=',i) != []:  # 此参数决定是否暴露php版本
        if 'On' in i.strip():
            print('警告: expose_php功能开启中,建议关闭该功能')