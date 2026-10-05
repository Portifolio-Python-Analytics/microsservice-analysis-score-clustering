import pandas as pd
from datetime import datetime
import ast

fechamento = datetime.now().strftime('%Y%m')
key_name_final = f"output/"

def remover_colunas(df, cols):
    return df.drop(columns=cols)

def remover_duplicados(df, cols):
    return df.drop_duplicates(subset=cols)

def pega_json(x):
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return {}
    return x if isinstance(x, dict) else {}

def safe_eval(x):
    if pd.isna(x):
        return {}
    if isinstance(x, str):
        try:
            return ast.literal_eval(x)
        except:
            return {}
    return x if isinstance(x, dict) else {}

def normalizar_valor(x):

    if x is None:
        return None

    if isinstance(x, (dict, list)):
        return str(x)

    if isinstance(x, float) and pd.isna(x):
        return None

    if hasattr(x, "item"):
        try:
            x = x.item()
        except Exception:
            pass

    return x

def registrar_movimentacoes_tratadas(df_tratado, cursor, fechamento):

    if df_tratado.empty:
        raise ValueError("Sem registros")

    sql = """
        INSERT INTO trusted_movimentacoes
        (
            id,
            nome_produto,
            dthora,
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
        VALUES (
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s
        )
    """

    valores = []

    for _, row in df_tratado.iterrows():

        valores.append((
            normalizar_valor(row["id"]),
            normalizar_valor(row["nome_produto"]),
            normalizar_valor(row["dthora"]),
            normalizar_valor(row["qtd"]),
            normalizar_valor(row["id_canal"]),
            normalizar_valor(row["categoria_canal"]),
            normalizar_valor(row["id_movimentacao"]),
            normalizar_valor(row["valor_movimentacao"]),
            normalizar_valor(row["id_cliente"]),
            normalizar_valor(row["documento_cliente"]),
            normalizar_valor(row["id_produto"]),
            normalizar_valor(fechamento)
        ))

    cursor.executemany(sql, valores)

def registrar_cnpjs_tratados(df_tratado, cursor, fechamento):

    if df_tratado.empty:
        raise ValueError("Sem registros")

    sql = """
        INSERT INTO trusted_cnpjs
        (
            cnpj_raiz,
            id_aplicacao,
            mei_simples,
            atividade_principal,
            atividade_secundarias,
            tipo,
            nome_fantasia,
            situacao,
            tipo_logradouro,
            logradouro,
            numero,
            razao_social,
            bairro,
            cep,
            cidade_nome,
            cidade_ibge_id,
            cidade_siafi_id,
            estado_nome,
            estado_sigla,
            pais_nome,
            telefone1,
            telefone2,
            capital_social,
            fax,
            email,
            situacao_especial,
            data_situacao_especial,
            latitude,
            longitude,
            responsavel_federativo,
            atualizado_em,
            porte,
            natureza_juridica,
            qualificacao_do_responsavel,
            socios,
            anomes
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    valores = []

    for _, row in df_tratado.iterrows():

        valores.append((
            normalizar_valor(row["cnpj_raiz"]),
            normalizar_valor(row["id_aplicacao"]),
            normalizar_valor(row["mei_simples"]),
            normalizar_valor(row["atividade_principal"]),
            normalizar_valor(row["atividade_secundarias"]),
            normalizar_valor(row["tipo"]),
            normalizar_valor(row["nome_fantasia"]),
            normalizar_valor(row["situacao"]),
            normalizar_valor(row["tipo_logradouro"]),
            normalizar_valor(row["logradouro"]),
            normalizar_valor(row["numero"]),
            normalizar_valor(row["razao_social"]),
            normalizar_valor(row["bairro"]),
            normalizar_valor(row["cep"]),
            normalizar_valor(row["cidade_nome"]),
            normalizar_valor(row["cidade_ibge_id"]),
            normalizar_valor(row["cidade_siafi_id"]),
            normalizar_valor(row["estado_nome"]),
            normalizar_valor(row["estado_sigla"]),
            normalizar_valor(row["pais_nome"]),
            normalizar_valor(row["telefone1"]),
            normalizar_valor(row["telefone2"]),
            normalizar_valor(row["capital_social"]),
            normalizar_valor(row["fax"]),
            normalizar_valor(row["email"]),
            normalizar_valor(row["situacao_especial"]),
            normalizar_valor(row["data_situacao_especial"]),
            normalizar_valor(row["latitude"]),
            normalizar_valor(row["longitude"]),
            normalizar_valor(row["responsavel_federativo"]),
            normalizar_valor(row["atualizado_em"]),
            normalizar_valor(row["porte"]),
            normalizar_valor(row["natureza_juridica"]),
            normalizar_valor(row["qualificacao_do_responsavel"]),
            normalizar_valor(row["socios"]),
            int(fechamento)
        ))

    print(
        f"Quantidade de registros: {len(valores)}"
    )

    print(
        f"Quantidade de parâmetros por registro: {len(valores[0])}"
    )

    cursor.executemany(sql, valores)

def tratar_movimentacoes(df):
    df_movimentacoes = df.copy()
    
    df_movimentacoes['movimentacao'] = df_movimentacoes['movimentacao'].apply(safe_eval)
    df_movimentacoes['cliente'] = df_movimentacoes['cliente'].apply(safe_eval)
    df_movimentacoes['produto'] = df_movimentacoes['produto'].apply(safe_eval)

    df_movimentacoes['id_canal'] = df_movimentacoes['movimentacao'].apply(
        lambda x: x.get('canal', {}).get('id')
    )

    df_movimentacoes['categoria_canal'] = df_movimentacoes['movimentacao'].apply(
        lambda x: x.get('canal', {}).get('categoria')
    )

    df_movimentacoes['id_movimentacao'] = df_movimentacoes['movimentacao'].apply(
        lambda x: x.get('id')
    )

    df_movimentacoes['valor_movimentacao'] = df_movimentacoes['movimentacao'].apply(
        lambda x: x.get('valor')
    )

    df_movimentacoes['id_cliente'] = df_movimentacoes['cliente'].apply(
        lambda x: x.get('id')
    )

    df_movimentacoes['documento_cliente'] = df_movimentacoes['cliente'].apply(
        lambda x: x.get('documento')
    )

    df_movimentacoes['id_produto'] = df_movimentacoes['produto'].apply(
        lambda x: x.get('id')
    )

    df_movimentacoes['nome_produto'] = df_movimentacoes['produto'].apply(
        lambda x: f"{x.get('tipo')} ({x.get('descricao')})"
    )

    df_movimentacoes['dthora'] = df_movimentacoes['movimentacao'].apply(
        lambda x: x.get('dtHora')
    )

    df_movimentacoes['dthora'] = pd.to_datetime(
        df_movimentacoes['dthora']
    ).dt.strftime('%Y-%m-%d %H:%M:%S')

    df_limpo_mov = remover_colunas(
        df_movimentacoes,
        ['movimentacao', 'cliente', 'produto']
    )

    schema_mov_cols = [
        "id",
        "nome_produto",
        "dthora",
        "qtd",
        "id_canal",
        "categoria_canal",
        "id_movimentacao",
        "valor_movimentacao",
        "id_cliente",
        "documento_cliente",
        "id_produto"
    ]

    for col in schema_mov_cols:
        if col not in df_limpo_mov.columns:
            df_limpo_mov[col] = None

    df_limpo_mov = df_limpo_mov[schema_mov_cols]
    
    return df_limpo_mov

def tratar_cnpjs(df):
    df_final_cnpjs = df.copy()

    df_final_cnpjs['id_aplicacao'] = df_final_cnpjs.index
    df_final_cnpjs['porte'] = df_final_cnpjs['porte'].apply(
        lambda x: pega_json(x).get('descricao')
    )
    df_final_cnpjs['natureza_juridica'] = df_final_cnpjs['natureza_juridica'].apply(
        lambda x: pega_json(x).get('descricao')
    )
    df_final_cnpjs['qualificacao_do_responsavel'] = df_final_cnpjs['qualificacao_do_responsavel'].apply(
        lambda x: 'NA' if x is None else x
    )
    df_final_cnpjs['socios'] = df_final_cnpjs['socios'].apply(
        lambda x: None if not x else x
    )
    df_final_cnpjs['responsavel_federativo'] = df_final_cnpjs['responsavel_federativo'].apply(
        lambda x: 0 if pd.isna(x) else 1
    )
    df_final_cnpjs['atualizado_em'] = pd.to_datetime(
        df_final_cnpjs['atualizado_em']
    ).dt.strftime("%d/%m/%Y")
    df_final_cnpjs['mei_simples'] = df_final_cnpjs['simples'].apply(
        lambda x: 0 if x == "Não" else 1
    )
    df_final_cnpjs['tipo'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('tipo')
    )
    df_final_cnpjs['nome_fantasia'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('nome_fantasia') or 'NA'
    )
    df_final_cnpjs['situacao'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('situacao_cadastral') or 'NA'
    )
    df_final_cnpjs['cidade_nome'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('cidade', {}).get('nome') or 'NA'
    )
    df_final_cnpjs['estado_sigla'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('estado', {}).get('sigla') or 'NA'
    )
    df_final_cnpjs['telefone1'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: (
            f"+55 {pega_json(x).get('ddd1')} {pega_json(x).get('telefone1')}"
            if pega_json(x).get('ddd1') and pega_json(x).get('telefone1')
            else 'NA'
        )
    )
    df_final_cnpjs['telefone2'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: (
            f"+55 {pega_json(x).get('ddd2')} {pega_json(x).get('telefone2')}"
            if pega_json(x).get('ddd2') and pega_json(x).get('telefone2')
            else 'NA'
        )
    )
    df_final_cnpjs['fax'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: (
            f"+55 {pega_json(x).get('ddd_fax')} {pega_json(x).get('fax')}"
            if pega_json(x).get('ddd_fax') and pega_json(x).get('fax')
            else 'NA'
        )
    )
    df_final_cnpjs['email'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('email') or 'NA'
    )
    df_final_cnpjs['atividade_principal'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('atividade_principal')
    )
    df_final_cnpjs['atividade_secundarias'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('atividades_secundarias')
    )
    df_final_cnpjs['tipo_logradouro'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('tipo_logradouro') or 'NA'
    )

    df_final_cnpjs['logradouro'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('logradouro') or 'NA'
    )
    df_final_cnpjs['numero'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('numero') or 'NA'
    )
    df_final_cnpjs['bairro'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('bairro') or 'NA'
    )
    df_final_cnpjs['cep'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('cep') or 'NA'
    )
    df_final_cnpjs['cidade_ibge_id'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('cidade', {}).get('ibge_id')
    )
    df_final_cnpjs['cidade_siafi_id'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('cidade', {}).get('siafi_id')
    )
    df_final_cnpjs['estado_nome'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('estado', {}).get('nome') or 'NA'
    )
    df_final_cnpjs['pais_nome'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('pais', {}).get('nome') or 'NA'
    )
    df_final_cnpjs['situacao_especial'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('situacao_especial') or 'NA'
    )
    df_final_cnpjs['data_situacao_especial'] = df_final_cnpjs['estabelecimento'].apply(
        lambda x: pega_json(x).get('data_situacao_especial') or 'NA'
    )
    df_limpo_intermediario = remover_colunas(
        df_final_cnpjs,
        ['simples', 'estabelecimento']
    )
    df_limpo_intermediario['anomes'] = fechamento
    df_final = remover_duplicados(
        df_limpo_intermediario,
        ['cnpj_raiz', 'razao_social']
    )
    df_final = df_final.astype({
        'cnpj_raiz': str,
        'razao_social': str,
        'capital_social': float,
        'responsavel_federativo': 'Int64',
        'latitude': float,
        'longitude': float
    })

    schema_cols = [
        "cnpj_raiz",
        "id_aplicacao",
        "mei_simples",
        "atividade_principal",
        "atividade_secundarias",
        "tipo",
        "nome_fantasia",
        "situacao",
        "tipo_logradouro",
        "logradouro",
        "numero",
        "razao_social",
        "bairro",
        "cep",
        "cidade_nome",
        "cidade_ibge_id",
        "cidade_siafi_id",
        "estado_nome",
        "estado_sigla",
        "pais_nome",
        "telefone1",
        "telefone2",
        "capital_social",
        "fax",
        "email",
        "situacao_especial",
        "data_situacao_especial",
        "latitude",
        "longitude",
        "responsavel_federativo",
        "atualizado_em",
        "porte",
        "natureza_juridica",
        "qualificacao_do_responsavel",
        "socios",
        "anomes"
    ]

    for col in schema_cols:
        if col not in df_final.columns:
            df_final[col] = None

    df_final = df_final[schema_cols]
    
    return df_final

def buscar_movimentacoes_raw(cursor, fechamento):
    
    cursor.execute(f"""
        SELECT
            *
        FROM raw_movimentacoes
        WHERE anomes = {fechamento}
    """)
    
    return cursor.fetchall()

def buscar_cnpjs_raw(cursor, fechamento):
    
    cursor.execute(f"""
        SELECT *
        FROM raw_cnpjs
        WHERE anomes = {fechamento}
        """)
    
    return cursor.fetchall()

def handler(conn, cursor):
    
    try:
        fechamento = datetime.now().strftime("%Y%m")
        
        # CNPJS
        print('IMPORTANDO CNPJs')
        df_import_cnpjs = pd.DataFrame(
            buscar_cnpjs_raw(
                cursor=cursor,
                fechamento=fechamento
            ),
            columns=[desc[0] for desc in cursor.description]
        )
        
        print('TRATANDO CNPJs')
        df_final_cnpjs = tratar_cnpjs(
            df=df_import_cnpjs
        )
        
        print('REGISTRANDO CNPJs')
        registrar_cnpjs_tratados(
            df_tratado=df_final_cnpjs,
            cursor=cursor,
            fechamento=fechamento
        )
    except Exception as e:
        print(e)
        conn.rollback()

    try:
        # MOVIMENTACOES
        print('IMPORTANDO MOV')
        df_import_mov = pd.DataFrame(
            buscar_movimentacoes_raw(
                cursor=cursor,
                fechamento=fechamento
            ),
            columns=[desc[0] for desc in cursor.description]
        )
        
        print('TRATANDO MOV')
        df_final_mov = tratar_cnpjs(
            df=df_import_mov
        )
        
        print('REGISTRANDO MOV')
        registrar_movimentacoes_tratadas(
            df_tratado=df_final_mov,
            cursor=cursor,
            fechamento=fechamento
        )
        
        return {
            "status": "ok",
            "cnpjs_processados": len(df_final_cnpjs),
            "data_execucao": fechamento
        }
        
    except Exception as e:
        print(e)
        conn.rollback()
    
    conn.commit()

def tratar(conn, cursor):
    handler(conn, cursor)
