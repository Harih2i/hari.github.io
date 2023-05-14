from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

import models
import cronservice
from models import Job
from utils import watch_status, load_logs
from database import SessionLocal, engine, JobRequest

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")




from get_data import *



@app.get("/")
async def home(request: Request):
    # jobs = {
    # "image":
    #     [
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "401",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #                 ]
    #       },
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "image2",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       }
    #     ],
    # "image_frequency":[ 
    #         {"label":"5mins","value":155}, 
    #         {"label":"10mins", "value":222},
    #         {"label":"15mins","value":311},
    #         {"label":"30mins", "value":200},
    #         {"label":"1/2hours", "value":900},
    #         {"label": ">3hours", "value":100}

    #     ],
    # "scheduler":
    #     [
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "scheduler1",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       },
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "scheduler2",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       }
    #     ],
    # "scheduler_frequency":[ 
    #         {"label":"5mins","value":55}, 
    #         {"label":"10mins", "value":22},
    #         {"label":"15mins","value":31},
    #         {"label":"30mins", "value":20},
    #         {"label":"1/2hours", "value":90},
    #         {"label": ">3hours", "value":100}

    #     ],
    # "normalizer":
    #     [
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "normalizer1",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       },
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "normalizer2",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       }
    #     ],
    # "normalizer_frequency":[ 
    #         {"label":"5mins","value":55}, 
    #         {"label":"10mins", "value":22},
    #         {"label":"15mins","value":31},
    #         {"label":"30mins", "value":20},
    #         {"label":"1/2hours", "value":90},
    #         {"label": ">3hours", "value":100}

    #     ],
    # "converter":
    #     [
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "converter1",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       },
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "converter2",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       }
    #     ],
    # "converter_frequency":[ 
    #         {"label":"5mins","value":55}, 
    #         {"label":"10mins", "value":22},
    #         {"label":"15mins","value":31},
    #         {"label":"30mins", "value":20},
    #         {"label":"1/2hours", "value":90},
    #         {"label": ">3hours", "value":100}

    #     ],
    # "association":
    #     [
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "association1",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       },
    #       {
    #         "host": "image-downloader2.v2.ng.movoto.net",
    #         "mls_id": "association2",
    #         "next_run": "2023-05:20 05:00:00",
    #         "commands": ['3,8,13,18,23,28,33,38,43,48,53,58 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 10800 "python ImageDownloader.py -mls_id=100 -sel=new -timeout=10800" >/dev/null 2>&1 &',
    #             '*/5 * * * * . /opt/venv2713/bin/activate && cd /opt/batchscripts/imagedownloader/src && tars_runner -l -t 3600 "python ImageDownloader.py -mls_id=100 -sel=fresh" >/dev/null 2>&1 &'
    #         ]
    #       }
    #     ],
    # "association_frequency":[ 
    #         {"label":"5mins","value":55}, 
    #         {"label":"10mins", "value":22},
    #         {"label":"15mins","value":31},
    #         {"label":"30mins", "value":20},
    #         {"label":"1/2hours", "value":90},
    #         {"label": ">3hours", "value":100}

    #     ]
    # }
    # jobs = {}
    # print("jobs:", jobs)
    jobs = main()
    output = {"request": request, "jobs": jobs}
    return templates.TemplateResponse("home.html", output)




