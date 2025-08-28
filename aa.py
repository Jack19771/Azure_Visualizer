import requests
import os

BASE_URL = "https://registry.terraform.io/v1/providers/hashicorp/consul/2.22.0"
RAW_BASE = "https://raw.githubusercontent.com/hashicorp/terraform-provider-consul/v2.22.0/"

OUTPUT_DIR = "consul_docs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Pobranie manifestu providera
manifest = requests.get(BASE_URL).json()

# 2. Iteracja po docsach
for doc in manifest["docs"]:
    path = doc["path"]  # np. docs/resources/service.md
    url = RAW_BASE + path

    resp = requests.get(url)
    if resp.status_code == 200:
        filename = path.replace("/", "_")  # np. docs_resources_service.md
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(resp.text)

        print(f"✔ Zapisano: {filepath}")
    else:
        print(f"❌ Błąd {resp.status_code} dla {url}")
