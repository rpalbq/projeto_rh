from pymongo import MongoClient, errors
from bson.objectid import ObjectId
from bson import errors as erros

def conectar():

    conn = MongoClient('localhost', 27017)

    return conn


def desconectar(conn):
    
    if conn:
        conn.close()


def listar():

    conn = conectar()
    db = conn.projeto_rh

    try:
        if db.vagas.count_documents({}) > 0:
            vagas = db.vagas.find()
            print('----------VAGAS---------')
            for vaga in vagas:
                print(f"ID: {vaga['_id']}")
                print(f"NUMERO: {vaga['numero']}")
                print(f"DESCRICAO: {vaga['descricao']}")
                print(f"HABILIDADES: {vaga['habilidades']}")
                print(f"SITUACAO: {vaga['situacao']}")
                print(f"FORMATO: {vaga['formato']}")
                print(f"QUANTIDADE DE VAGAS GERAL: {vaga['qnt_vagas'][0]['geral']}")
                print(f" QUANTIDADE DE VAGAS PARA AÇÃO AFIRMATIVA - RAÇA: {vaga['qnt_vagas'][1]['acao_afirmativa']['raca']}")
                print(f"QUANTIDADE DE VAGS PARA AÇÃO AFIRMATIVA- GÊNERO: {vaga['qnt_vagas'][1]['acao_afirmativa']['genero']}")
                print(f"SALARIO: {vaga['salario']}")
                print
        else:
            print('Não existem vagas no momento')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    desconectar(conn)


def inserir():
    
    conn = conectar()
    db = conn.projeto_rh


    numero = int(input("Informe o numero/idamigavel da vaga:"))
    descricao = input("Informe a descricao:")
    habilidades = input("Informe as habilidades (separadas por vírgula):").split(',')
    situacao = input("Informe a situacao da vaga:")
    formato = input("Informe o formato da vaga:")
    geral = int(input("Informe a quantidade de vagas no geral(sem ações afirmativas)"))
    raca = int(input("Informe a quantidade de vagas separadas para ação afirmativa - raca)"))
    genero = int(input("Informe a quantidade de vagas separadas para ação afirmativa - gênero"))
    salario = float(input("Informe o salário:"))

    try:
        db.vagas.insert_one(
            {
                "numero": numero,
                "descricao": descricao,
                "habilidades": habilidades,
                "situacao": situacao,
                "formato": formato,
                "qnt_vagas": [
                    { 
                        "geral": geral
                    },
                    {
                        "acao_afirmativa": {
                            "raca": raca,
                            "genero": genero
                        }
                    }
                ],
                "salario": salario
            }
        )
        print(f'A vaga {descricao} foi inserida com sucesso!')
    except errors.PyMongoError as e:
        print(f'Não foi possível adicionar a vaga: {e}')
    desconectar(conn)


def atualizar():

    conn =  conectar()
    db = conn.projeto_rh

    _id = input('Informe o id da vaga:')
    numero = int(input("Informe o numero/idamigavel da vaga:"))
    descricao = input("Informe a descricao:")
    habilidades = input("Informe as habilidades (separadas por vírgula):").split(',')
    situacao = input("Informe a situacao da vaga:")
    formato = input("Informe o formato da vaga:")
    geral = int(input("Informe a quantidade de vagas no geral(sem ações afirmativas)"))
    raca = int(input("Informe a quantidade de vagas separadas para ação afirmativa - raca)"))
    genero = int(input("Informe a quantidade de vagas separadas para ação afirmativa - gênero"))
    salario = float(input("Informe o salário:"))

    try: 
        if db.vagas.count_documents({}) > 0:
            res = db.vagas.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "numero": numero,
                        "descricao": descricao,
                        "habilidades": habilidades,
                        "situacao": situacao,
                        "formato": formato,
                        "qnt_vagas": [
                            { 
                                "geral": geral
                            },
                            {
                                "acao_afirmativa": {
                                    "raca": raca,
                                    "genero": genero
                                }
                            }
                        ],
                        "salario": salario
                    }
               }
            )
            if res.modified_count == 1:
                print(f'A vaga {descricao} foi atualizada com sucesso!')
            else:
                print('Não foi possível atualizar a vaga :c')
        else:
            print('Não existem documentos para serem atualizados')

    except errors.PyMongoError as e:
        print(f'Não foi possível acessar o banco de dados. {e}')
    except erros.InvalidId as f:
        print(f'Object Id inválido. {f}')
        
    desconectar(conn)


def deletar():
    
    conn = conectar()
    db =  conn.projeto_rh

    _id = input("Informe o id da vaga:")

    try:
        if db.vagas.count_documents({}) > 0:
            res = db.vagas.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            if res.deleted_count > 0:
                print('Vaga deletada com sucesso!')
            else:
                print("Não foi possível deletar")
        else:
            print("Não existem vagas para serem deletadas")
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados. {e}')
    except erros.InvalidId as f:
        print(f'Object Id invalido. {f}')
    desconectar(conn)


def menuVagas():

    print('-------------MENU VAGAS-----------------')
    print('Selecione uma opcão: ')
    print('1 - Listar vagas')
    print('2 - Inserir vagas')
    print('3 - Atualizar vagas')
    print('4 - Deletar vagas')
    opcao = int(input())
    if opcao in  [1,2,3,4]:
        if opcao == 1:
            listar()
        elif opcao == 2:
            inserir()
        elif opcao == 3:
            atualizar()
        elif opcao == 4:
            deletar()
        else:
            print('Opção inválida!')
    else:
        print('Opção invalida!')