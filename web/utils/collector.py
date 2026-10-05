import json
import re
import time
from datetime import datetime

import pymysql
import requests


def buscar_cnpjs(cursor):

    cursor.execute("""
        SELECT DISTINCT documento
        FROM cliente
        WHERE pf = 0
          AND documento IS NOT NULL
    """)

    cnpjs = set()

    for row in cursor.fetchall():

        documento = re.sub(r"\D", "", row["documento"])

        if len(documento) == 14:
            cnpjs.add(documento)

    print(f"CNPJs encontrados: {len(cnpjs)}")

    return sorted(cnpjs)


def consultar_cnpj(cnpj):

    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"

    print(f"Consultando {cnpj}")

    resposta = requests.get(url, timeout=30)

    if resposta.status_code == 429:
        print("Rate limit. Aguardando 70 segundos...")
        time.sleep(70)
        resposta = requests.get(url, timeout=30)

    resposta.raise_for_status()

    return resposta.json()


def consultar_endereco(cep):

    cep = re.sub(r"\D", "", cep)

    resposta = requests.get(
        f"https://viacep.com.br/ws/{cep}/json/",
        timeout=20
    )

    resposta.raise_for_status()

    return resposta.json()


def consultar_coordenadas(logradouro,
                          numero,
                          cidade):

    resposta = requests.get(

        "https://nominatim.openstreetmap.org/search",

        params={

            "q":
            f"{logradouro}, {numero}, {cidade}, Brazil",

            "format": "json",

            "limit": 1

        },

        headers={
            "User-Agent": "confeitaria-nocelli"
        },

        timeout=30

    )

    resposta.raise_for_status()

    dados = resposta.json()

    if not dados:

        return None, None

    return (

        float(dados[0]["lat"]),

        float(dados[0]["lon"])

    )


def inserir_raw_cnpj(cursor, linha, fechamento):

    sql = """
    INSERT INTO raw_cnpjs
    (
        cnpj_raiz,
        simples,
        estabelecimento,
        latitude,
        longitude,
        razao_social,
        capital_social,
        responsavel_federativo,
        atualizado_em,
        porte,
        natureza_juridica,
        qualificacao_do_responsavel,
        socios,
        anomes
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
    )
    """

    cursor.execute(

        sql,

        (

            linha["cnpj_raiz"],

            json.dumps(
                linha["simples"],
                ensure_ascii=False
            ),

            json.dumps(
                linha["estabelecimento"],
                ensure_ascii=False
            ),

            linha["latitude"],

            linha["longitude"],

            linha["razao_social"],

            linha["capital_social"],

            linha["responsavel_federativo"],

            datetime.fromisoformat(
                linha["atualizado_em"].replace("Z", "+00:00")
            ).strftime("%Y-%m-%d %H:%M:%S"),

            json.dumps(
                linha["porte"],
                ensure_ascii=False
            ),

            json.dumps(
                linha["natureza_juridica"],
                ensure_ascii=False
            ),

            linha["qualificacao_do_responsavel"],

            json.dumps(
                linha["socios"],
                ensure_ascii=False
            ),
            int(fechamento)

        )

    )

def copiar_movimentacoes(cursor, fechamento):

    cursor.execute(f"""
        INSERT INTO raw_movimentacoes
        (
            nome_produto,
            dtHora,
            qtd,
            id_canal,
            categoria_canal,
            id_movimentacao,
            valor_movimentacao,
            id_cliente,
            documento_cliente,
            id_produto,
            anomes
        )
        SELECT
            p.nome AS nome_produto,
            m.dt_hora AS dtHora,
            co.qtd,
            ca.id AS id_canal,
            ca.categoria AS categoria_canal,
            m.id AS id_movimentacao,
            m.valor AS valor_movimentacao,
            cl.id AS id_cliente,
            cl.documento AS documento_cliente,
            p.id AS id_produto,
            {int(fechamento)} AS anomes
        FROM movimentacao AS m
        LEFT JOIN canal AS ca
            ON m.fk_canal = ca.id
        LEFT JOIN compra AS co
            ON m.id = co.fk_movimentacao
        LEFT JOIN produto AS p
            ON co.fk_produto = p.id
        LEFT JOIN cliente AS cl
            ON co.fk_cliente = cl.id
        WHERE cl.pf = 0
            AND cl.documento IS NOT NULL
            AND m.dt_hora >= CURDATE() - INTERVAL 30 DAY;
    """)


def handler(conn, cursor):

    try:
        fechamento = datetime.now().strftime("%Y%m")
        print(f"Processando período {fechamento}")

        cnpjs = buscar_cnpjs(cursor)
        resultados = []

        for cnpj in cnpjs:

            try:
                dados = consultar_cnpj(cnpj)
                estabelecimento = dados.get(
                    "estabelecimento",
                    {}
                )
                endereco = consultar_endereco(
                    estabelecimento.get("cep", "")
                )
                latitude, longitude = consultar_coordenadas(
                    endereco.get("logradouro", ""),
                    estabelecimento.get("numero", ""),
                    endereco.get("localidade", "")
                )

                linha = {
                    "cnpj_raiz": cnpj,
                    "simples":
                        dados.get("simples"),
                    "estabelecimento":
                        estabelecimento,
                    "latitude":
                        latitude,
                    "longitude":
                        longitude,
                    "razao_social":
                        dados.get("razao_social"),
                    "capital_social":
                        dados.get("capital_social"),
                    "responsavel_federativo":
                        dados.get("responsavel_federativo"),
                    "atualizado_em":
                        dados.get("atualizado_em"),
                    "porte":
                        dados.get("porte"),
                    "natureza_juridica":
                        dados.get("natureza_juridica"),
                    "qualificacao_do_responsavel":
                        dados.get(
                            "qualificacao_do_responsavel",
                            {}
                        ).get("descricao"),
                    "socios":
                        dados.get("socios")
                }
                resultados.append(linha)
            except Exception as e:
                print(f"Erro ao consultar CNPJ {cnpj}: {e}")
                continue

        print(f"{len(resultados)} registros obtidos.")

        print("Gravando dados na tabela raw_cnpjs...")

        for linha in resultados:

            try:

                inserir_raw_cnpj(cursor, linha, fechamento)

            except pymysql.err.IntegrityError as e:

                print(
                    f"CNPJ {linha['cnpj_raiz']} já existe na tabela."
                )

            except Exception as e:

                print(
                    f"Erro ao inserir {linha['cnpj_raiz']}: {e}"
                )

        print("Copiando movimentações...")

        copiar_movimentacoes(cursor, fechamento)

        print("Processamento concluído com sucesso.")

        return {

            "status": "ok",

            "cnpjs_processados": len(resultados),

            "data_execucao": fechamento

        }

    except Exception as e:
        conn.rollback()
        raise

def buscar(conn, cursor):
    handler(conn, cursor)