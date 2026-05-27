import requests
import re
import base64
import json
from urllib.parse import quote

def main():
    url = "https://raw.githubusercontent.com/TopChina/proxy-list/main/README.md"
    print("正在下载 README.md ...")
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception as e:
        print(f"下载失败: {e}")
        return

    # 正则提取 IP:端口, 地区, 用户名
    pattern = r"\|\s*([\d.]+:\d+)\s*\|\s*([^|]+?)\s*\|\s*([A-Za-z0-9+/=_-]+)\s*\|"
    matches = re.findall(pattern, resp.text)

    servers = []
    for ip_port, region, username in matches:
        ip, port = ip_port.split(':', 1)
        region = region.strip()
        username = username.strip()
        # 构建 V2RayN 能识别的自定义配置对象
        server = {
            "remarks": region,                   # 显示名称
            "address": ip,                       # 服务器地址
            "port": int(port),                   # 端口
            "protocol": "http",                  # 协议类型（固定 http）
            "id": username,                      # 用户名（对应 V2RayN 的 "id" 字段）
            "security": "",                      # 加密方式（HTTP 不加密留空）
            "network": "tcp",                    # 传输协议
            "headerType": "none",                # 伪装类型
            "flow": "",                          # 流控
            "aid": 0,                            # 额外ID
            "host": "",                          # 伪装域名
            "path": "",                          # 路径
            "tls": "",                           # TLS 设置
        }
        servers.append(server)

    if not servers:
        print("未提取到任何代理。")
        return

    # 将对象列表转为 JSON 并 Base64 编码
    json_str = json.dumps(servers, ensure_ascii=False, separators=(',', ':'))
    encoded = base64.b64encode(json_str.encode()).decode()

    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write(encoded)

    print(f"成功生成 sub.txt，共 {len(servers)} 条 HTTP 代理。")

if __name__ == "__main__":
    main()
