import base64
import json
import yaml
from flask import Flask
from flask import request

def get_vmess(vmess_content):
    """
    获取vmess订阅
    :param url:
    :return:
    """
    if not vmess_content.endswith("=="):
        vmess_content += "=="
    print(vmess_content)
    vmess = base64.b64decode(vmess_content).decode()
    vmess = json.loads(vmess)
    vmess = vmess_sub_to_clash(vmess)
    print(vmess)

    return remove_vmess_node([vmess], "特殊")


def vmess_sub_to_clash(d):
    """
    将vmess订阅结果转换成clash的proxy格式
    :param d:
    :return:
    """
    new_d = {
        "name": d["ps"],
        "type": "vmess",
        "server": d["add"],
        "port": d["port"],
        "uuid": d["id"],
        "alterId": 2,
        "cipher": "auto",
        "tls": True
    }
    return new_d


def remove_vmess_node(vmess_list, keyword):
    """
    将指定的关键字节点从节点列表中移除
    :param vmess_list:
    :param keyword:
    :return:
    """
    new_vmess_list = []
    for n in vmess_list:
        if keyword in n["name"]:
            continue
        new_vmess_list.append(n)
    return new_vmess_list


def generate_proxy_groups(proxy_groups: list, proxies: list) -> list:
    """
  - 🇭🇰 香港节点
  - 🇨🇳 台湾节点
  - 🇸🇬 新加坡节点
  - 🇯🇵 日本节点
  - 🇺🇲 美国节点
  - 🚀 手动切换
    :param proxy_groups:
    :param proxies:
    :return:
    """
    um = []
    jp = []
    sg = []
    cn = []
    hk = []
    for n in proxies:
        if "美国" in n["name"]:
            um.append(n["name"])
        elif "日本" in n["name"]:
            jp.append(n["name"])
        elif "新加坡" in n["name"]:
            sg.append(n["name"])
        elif "台湾" in n["name"]:
            cn.append(n["name"])
        elif "港" in n["name"]:
            hk.append(n["name"])

    for idx, value in enumerate(proxy_groups):
        if value["name"] == "🇭🇰 香港节点":
            proxy_groups[idx]["proxies"] = hk
        if value["name"] == "🇨🇳 台湾节点":
            proxy_groups[idx]["proxies"] = cn
        if value["name"] == "🇸🇬 新加坡节点":
            proxy_groups[idx]["proxies"] = sg
        if value["name"] == "🇯🇵 日本节点":
            proxy_groups[idx]["proxies"] = jp
        if value["name"] == "🇺🇲 美国节点":
            proxy_groups[idx]["proxies"] = um
        if value["name"] == "🚀 手动切换":
            proxy_groups[idx]["proxies"] = [n["name"] for n in proxies]

    return proxy_groups


def get_clash_sub(vmess_url):
    """
    :param vmess_url:
    :return:
    """
    proxies = get_vmess(vmess_url)
    proxy_groups = [{'name': 'Proxy', 'type': 'select', 'proxies': ['🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点', '🚀 手动切换', 'DIRECT']}, {'name': 'Domestic', 'type': 'select', 'proxies': ['DIRECT', 'Proxy', '🚀 手动切换']}, {'name': 'PayPal', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Netflix', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Spotify', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Others', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', 'Domestic']}, {'name': 'AdBlock', 'type': 'select', 'proxies': ['REJECT', 'DIRECT', 'Proxy']}, {'name': 'Apple', 'type': 'select', 'proxies': ['DIRECT', 'Proxy', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'AsianTV', 'type': 'select', 'proxies': ['DIRECT', 'Domestic', 'Proxy', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'GlobalTV', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Telegram', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Steam', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Speedtest', 'type': 'select', 'proxies': ['Proxy', 'DIRECT', 'Domestic']}, {'name': 'Microsoft', 'type': 'select', 'proxies': ['DIRECT', 'Proxy', '🇭🇰 香港节点', '🇨🇳 台湾节点', '🇸🇬 新加坡节点', '🇯🇵 日本节点', '🇺🇲 美国节点']}, {'name': 'Netease Music', 'type': 'select', 'proxies': ['DIRECT', 'Domestic']}, {'name': '🇭🇰 香港节点', 'type': 'url-test', 'url': 'http://www.gstatic.com/generate_204', 'interval': 500, 'proxies': None}, {'name': '🇨🇳 台湾节点', 'type': 'url-test', 'url': 'http://www.gstatic.com/generate_204', 'interval': 500, 'proxies': None}, {'name': '🇸🇬 新加坡节点', 'type': 'url-test', 'url': 'http://www.gstatic.com/generate_204', 'interval': 500, 'proxies': None}, {'name': '🇯🇵 日本节点', 'type': 'url-test', 'url': 'http://www.gstatic.com/generate_204', 'interval': 500, 'proxies': None}, {'name': '🇺🇲 美国节点', 'type': 'url-test', 'url': 'http://www.gstatic.com/generate_204', 'interval': 500, 'proxies': None}, {'name': '🚀 手动切换', 'type': 'select', 'proxies': None}]
    proxy_groups = generate_proxy_groups(proxy_groups, proxies)

    template = {
        'port': 7890, 
        'socks-port': 7891, 
        'allow-lan': True, 
        'mode': 'Rule', 
        'log-level': 'info',
        'external-controller': '127.0.0.1:9090',
        'cfw-bypass': ['qq.com', 'music.163.com', '*.music.126.net', 'localhost', '127.*', '10.*', '172.16.*',
                       '172.17.*', '172.18.*', '172.19.*', '172.20.*', '172.21.*', '172.22.*', '172.23.*',
                       '172.24.*', '172.25.*', '172.26.*', '172.27.*', '172.28.*', '172.29.*', '172.30.*',
                       '172.31.*', '192.168.*', '<local>'],
        "Proxy": proxies, 
        "Proxy Group": proxy_groups, 
        "Rule": ['DOMAIN-KEYWORD,unity,Proxy', 'DOMAIN-KEYWORD,unity3d,Proxy', 'DOMAIN,pt.m-team.cc,Proxy', 'DOMAIN,tracker.m-team.cc,DIRECT'],
    }

    return yaml.dump(template, sort_keys=False)


app = Flask(__name__)


@app.route("/")
def hello():
    vmess_url = request.args.get('vmess')
    return get_clash_sub(vmess_url)


if __name__ == "__main__":
    app.run(port=5000, host='0.0.0.0')
