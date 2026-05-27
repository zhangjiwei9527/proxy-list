import requests, re, base64
from urllib.parse import quote

url = "https://raw.githubusercontent.com/TopChina/proxy-list/main/README.md"
resp = requests.get(url)
lines = []
for ip_port, region, user in re.findall(r"\|\s*([\d.]+:\d+)\s*\|\s*([^|]+?)\s*\|\s*([A-Za-z0-9+/=_-]+)\s*\|", resp.text):
    ip, port = ip_port.split(':')
    link = f"http://{quote(user)}:{quote('1')}@{ip}:{port}#{quote(region.strip())}"
    lines.append(link)
sub = base64.b64encode("\n".join(lines).encode()).decode()
with open("sub.txt", "w") as f:
    f.write(sub)
