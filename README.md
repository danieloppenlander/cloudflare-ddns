# cloudflare-ddns

## Usage

### docker-compose

```yaml
version: "3.8"

services:
  cloudflare-ddns:
    container_name: cloudflare-ddns
    image: danieloppenlander/cloudflare-ddns:latest
    restart: unless-stopped
    environment:
      - ZONE_NAME=<zone-name>
      - NAME=<a-record-name>
      - IS_PROXIED=false
      - API_EMAIL=<email>
      - API_KEY=<key>
```
