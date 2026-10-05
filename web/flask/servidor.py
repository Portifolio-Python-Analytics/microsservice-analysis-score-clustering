from flask import Flask
from flask_cors import CORS
from apscheduler.schedulers.background import BackgroundScheduler
from utils import collector, cleaner, score_modelling, clustering
import pymysql
import os

app = Flask(__name__)
CORS(app)

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
    
    print("Buscando os dados!")
    collector.buscar(conn, cursor)
    
    # cleaner.tratar(conn, cursor)
    
    # score_modelling.calcular(conn, cursor)
    
    # clustering.agrupar(conn, cursor)
    
    print("TESTE")

scheduler = BackgroundScheduler()
scheduler.add_job(
    loadData,
    trigger="interval",
    minutes=1,
    max_instances=1,
    coalesce=True,
    misfire_grace_time=300
)
scheduler.start()

if __name__ == '__main__':
    print("testes")
    app.run(debug=False, port=5000, threaded=True)