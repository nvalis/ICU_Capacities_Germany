#!/usr/bin/env python
# coding: utf-8

import requests
import json
from datetime import datetime


def main():
    now = datetime.now()
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0"
    }
    r = requests.get(
        "https://www.intensivregister.de/api/public/intensivregister", headers=headers
    )

    with open(now.strftime("%y%m%d_%H%M%S_new.json"), "w") as f:
        f.write(r.text)


if __name__ == "__main__":
    main()

