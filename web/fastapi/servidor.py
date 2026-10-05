import os
import pymysql

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from utils import collector, cleaner, score_modelling, clustering

scheduler = BackgroundScheduler()

def conectar():
    return pymysql.connect(
        host=os.environ["MYSQL_HOST"],
        port=int(os.environ.get("MYSQL_PORT", 3306)),
        user=os.environ["MYSQL_USER"],
        password=os.environ["MYSQL_PASSWORD"],
        database=os.environ["MYSQL_DATABASE"],
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )

def loadData():

    conn = conectar()
    cursor = conn.cursor()

    try:
        print("Buscando os dados!")
        collector.buscar(conn, cursor)
        
        print("Tratando os dados!")
        cleaner.tratar(conn, cursor)
        # score_modelling.calcular(conn, cursor)
        # clustering.agrupar(conn, cursor)
        conn.commit()
        print("TESTE")

    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


@asynccontextmanager
async def lifespan(app: FastAPI):

    scheduler.add_job(
        loadData,
        trigger="interval",
        minutes=2,
        id="load_data",
        replace_existing=True
    )

    scheduler.start()

    print("Scheduler iniciado.")

    yield

    scheduler.shutdown(wait=False)

    print("Scheduler encerrado.")


app = FastAPI(
    title="Analysis Score Clustering",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():

    return {
        "status": "ok"
    }


@app.get("/run")
def run():

    loadData()

    return {
        "status": "Processamento executado."
    }