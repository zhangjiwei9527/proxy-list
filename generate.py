import requests
import re
import base64
import json

def main():
    url = "https://raw.githubusercontent.com/TopChina/proxy-list/main/README.md"
    print("正在下载 README.md ...")
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"下载失败: {e}")
        return

    pattern = r"\|\s*([\d.]+:\d+)\s*\|\s*([^|]+?)\s*\|\s*([A-Za-z0-9+/=_-]+)\s*\|"
    matches = re.findall(pattern, resp.text)

    servers = []
    for ip_port, region, username in matches:
        ip, port = ip_port.split(':', 1)
        region = region.strip()
        username = username.strip()

        server = {
            "remarks": region,           # 节点名称
            "address": ip,               # 服务器地址
            "port": int(port),           # 端口
            "id": username,              # 用户名
            "security": "1",             # ✅ 密码固定为 1，填入 security 字段
            "protocol": "http",          # 协议类型
            "configType": 1,             # 标记为 HTTP 代理（兼容旧版）
            "network": "tcp",
            "headerType": "none",
            "allowInsecure": False,
            "streamSecurity": "",
            "publicKey": "",
            "shortId": "",
            "fingerprint": "",
            "sni": ""
        }
        servers.append(server)

    if not servers:
        print("未提取到任何代理。")
        return

    json_str = json.dumps(servers, ensure_ascii=False, separators=(',', ':'))
    encoded = base64.b64encode(json_str.encode()).decode()

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"成功生成 sub.txt，共 {len(servers)} 条 HTTP 代理。")

if __name__ == "__main__":
    main()
