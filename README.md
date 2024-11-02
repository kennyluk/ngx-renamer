# Rename titles in Paperless NGX using OpenAI

This is a Paperless NGX post consumption script.More information under this link : https://docs.paperless-ngx.com/advanced_usage/#consume-hooks.
You need an OpenAI API account to run it.

## Installation in Paperless NGX

**Download or checkout the source code:**

* Copy the directory into your paperless docker compose directory (where the `docker-compose.yml` is located).

```bash
# It will look like this
user@host:~/paperless$ tree . -L 2
.
├── consume
├── docker-compose.env
├── docker-compose.yml
├── export
└── ngx-renamer
    ├── change_title.py
    ├── modules
    ├── post_consume_script.sh
    ├── README.md
    ├── requirements.txt
    ├── settings.yaml
    ├── setup_venv.sh
    ├── test_pdf.py
    ├── test_title.py
    ├── title_finder.py
```

**Create a `.env` file in the `ngx-renamer` directory and put your credentials in:**

```bash
# you can create an openai key under https://platform.openai.com/settings/organization/api-keys
OPENAI_API_KEY=<your_key_from_openai>
# you find the api key in your paperless user proofile
PAPERLESS_NGX_API_KEY=<your_paperless_api_token>
# the url of your paperless installation
PAPERLESS_NGX_URL=http://your-domain.whatever:port
```

**Open the `docker-compose.yml` file and add the directory `ngx-renamer` as internal directory to the webserver container and `post_consume_script.sh` as post consumption script:**

```bash
  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    restart: unless-stopped
    depends_on:
      - db
      - broker
      - gotenberg
      - tika
    ports:
      - "8443:8000"
    volumes:
      - /data/paperless/data:/usr/src/paperless/data
      - /data/paperless/media:/usr/src/paperless/media
      - ./export:/usr/src/paperless/export
      - /data/paperless/consume:/usr/src/paperless/consume
      # this is the new volume for nxg-renamer - add this
      - /your/path/to/paperless/ngx-renamer:/usr/src/ngx-renamer
    env_file: docker-compose.env
    environment:
      PAPERLESS_REDIS: redis://broker:6379
      PAPERLESS_DBHOST: db
      PAPERLESS_TIKA_ENABLED: 1
      PAPERLESS_TIKA_GOTENBERG_ENDPOINT: http://gotenberg:3000
      PAPERLESS_TIKA_ENDPOINT: http://tika:9998
      # This is the post consumption script call - add this
      PAPERLESS_POST_CONSUME_SCRIPT: /usr/src/ngx-renamer/post_consume_script.sh
```
**Restart your paperless system:**
```bash
user@host:~/paperless$ docker compose down
[+] Running 6/6
 ✔ Container paperless-webserver-1  Removed  10.4s
 ✔ Container paperless-db-1         Removed   0.3s
 ✔ Container paperless-tika-1       Removed   0.3s
 ✔ Container paperless-broker-1     Removed   0.2s
 ✔ Container paperless-gotenberg-1  Removed  10.2s
 ✔ Network paperless_default        Removed   0.2s
user@host:~/paperless$ docker compose up -d
[+] Running 6/6
 ✔ Network paperless_default        Created   0.1s
 ✔ Container paperless-broker-1     Started   0.6s
 ✔ Container paperless-db-1         Started   0.6s
 ✔ Container paperless-gotenberg-1  Started   0.5s
 ✔ Container paperless-tika-1       Started   0.6s
 ✔ Container paperless-webserver-1  Started   0.7s
```

**To initialize the virtual python environment in the docker container you have to call `setup_venv.sh`once and after any update of the container image. Make sure that the scripts and files are accessible by `root`. Follow these steps:**

```bash
# Change owner to root
user@host:~/paperless$ sudo chown -R root ngx-renamer/
# Make scripts executable
user@host:~/paperless$ sudo chmod +x ngx-renamer/setup_venv.sh
user@host:~/paperless$ sudo chmod +x ngx-renamer/post_consume_script.sh
# run setup routine
user@host:~/paperless$ docker compose exec -u paperless webserver /usr/src/ngx-renamer/setup_venv.sh
```

**The result sould look like:**

```bash
# Shortened version of the output
user@khost:~/paperless$ docker compose exec -u paperless webserver /usr/src/ngx-renamer/setup_venv.sh
Setting up virtual environment...
OK
...
Downloading PyYAML-6.0.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (767 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 767.5/767.5 kB 5.7 MB/s eta 0:00:00
Installing collected packages: pyyaml
Successfully installed pyyaml-6.0.2
```

**Done! Post cosumption only start after Paperless NGX created a new document through uploads, consumptions, or mails.**

```bash
# This script should run with an 404 error.
user@host:~/paperless$ docker compose exec -u paperless webserver /usr/src/ngx-renamer/post_consume_script.sh
```

## Python development and testing

If you want to develop and test is without integrating it in Paperless NGX you can do that.

* Create a virtual environment
* Load all libraries
* Call test scripts
* Enjoy optimizing the prompt in settings.yaml


### Create virtual environment

```bash
# python or python3 is up to your system
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### Load all needed libraries

```bash
(.venv)$ pip install -r requirements.txt
```

### Call test scripts

```bash
# prints the thought title from a american law text
(.venv)$ python3 test_title.py
````

```bash
# read the content from a OCR'ed pdf file
(.venv)$ python3 ./test_pdf.py path/to/your/ocr-ed/pdf/file

