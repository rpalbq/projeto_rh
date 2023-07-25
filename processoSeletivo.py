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
        if db.processo_seletivo.count_documents({}) > 0:
            etapas = db.processo_seletivo.find()
            print('----------PROCESSOS SELETIVOS---------')
            for etapa in etapas:
                print(f"ID: {etapa['_id']}")
                print(f"NUMERO: {etapa['numero']}")
                print(f"DESCRICAO: {etapa['descricao']}")
                print('---------------------------------')
        else:
            print('Não existem processos seletivos no momento')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    desconectar(conn)


def inserir():
    
    conn = conectar()
    db = conn.projeto_rh


    numero = int(input("Informe o numero/idamigavel do processo:"))
    descricao = input("Informe a descricao:")

    try:
        db.processo_seletivo.insert_one(
            {
                "numero": numero,
                "descricao": descricao
            }
        )
        print(f'O processo {descricao} foi inserido com sucesso!')

    except errors.PyMongoError as e:
        print(f'Não foi possíel adicionar o processo: {e}')
    desconectar(conn)


def atualizar():

    conn =  conectar()
    db = conn.projeto_rh

    _id = input('Informe o id do processo:')
    numero =  int(input('Informe o numero/id amigavel do processo:'))
    descricao = input('informe a descricao do processo:')

    try: 
        if db.processo_seletivo.count_documents({}) > 0:
            res = db.processo_seletivo.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "numero": numero,
                        "descricao": descricao,
                    }
                }
            )
            if res.modified_count == 1:
                print(f'O processo {descricao} foi atualizado com sucesso!')
            else:
                print('Não foi possível atualizar o processo :c')
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

    _id = input("Informe o id do processo:")

    try:
        if db.processo_seletivo.count_documents({}) > 0:
            res = db.processo_seletivo.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            if res.deleted_count > 0:
                print('Processo deletado com sucesso!')
            else:
                print("Não foi possível deletar")
        else:
            print("Não existem processos para serem deletados")
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados. {e}')
    except erros.InvalidId as f:
        print(f'Object Id invalido. {f}')
    desconectar(conn)


def menuProcesso():

    print('-------------MENU PROCESSO SELETIVO -----------------')
    print('Selecione uma opcão: ')
    print('1 - Listar processos')
    print('2 - Inserir processos')
    print('3 - Atualizar processos')
    print('4 - Deletar processsos')
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