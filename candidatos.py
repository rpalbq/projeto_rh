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
        if db.candidatos.count_documents({}) > 0:
            candidatos = db.candidatos.find()
            print('----------CANDIDATOS---------')
            for candidato in candidatos:
                print(f"ID: {candidato['_id']}")
                print(f"NOME: {candidato['nome']}")
                print(f"CPF: {candidato['cpf']}")
                print(f"DATA DE NASCIMENTO: {candidato['data_nasc']}")
                print(f"EMAIL: {candidato['contato']['email']}")
                print(f"TELEFONE: {candidato['contato']['telefone']}")
                print(f"CURSO: {candidato['curso']['nome']}")
                print(f"INSTITUIÇÃO: {candidato['curso']['instituicao']}")
                print("HABILIDADES:")
                for habilidade in candidato['habilidades']:
                    print(f"    Nome: {habilidade['nome']}")
                    print(f"    Nível: {habilidade['nivel']}")
                print(f"ID VAGA: {candidato['id_vaga']}")
                print(f"ID SITUAÇÃO: {candidato['id_situacao']}")
                print(f"PRETENSÃO SALARIAL: {candidato['pretensao_salarial']}")
                print(f"LINK CURRÍCULO: {candidato['link_curriculo']}")
                print('---------------------------------')
        else:
            print('Não existem candidatos cadastrados no momento')
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados: {e}')
    desconectar(conn)


def inserir():

    conn = conectar()
    db = conn.projeto_rh

    nome = input("Informe o nome do candidato:")
    cpf = input("Informe o CPF do candidato:")
    data_nasc = input("Informe a data de nascimento do candidato (formato: YYYY-MM-DD):")
    email = input("Informe o e-mail do candidato:")
    telefone = input("Informe o telefone do candidato:")
    curso_nome = input("Informe o nome do curso do candidato:")
    curso_instituicao = input("Informe a instituição do curso do candidato:")
    habilidades = []
    while True:
        nome_habilidade = input("Informe o nome da habilidade do candidato (ou digite 'sair' para encerrar):")
        if nome_habilidade.lower() == 'sair':
            break
        nivel_habilidade = input("Informe o nível da habilidade do candidato:")
        habilidades.append({"nome": nome_habilidade, "nivel": nivel_habilidade})

    id_vaga = input("Informe o ID da vaga a que o candidato está se candidatando:")
    id_situacao = input("Informe o ID da situação do candidato:")
    pretensao_salarial = float(input("Informe a pretensão salarial do candidato:"))
    link_curriculo = input("Informe o link para o currículo do candidato:")

    try:
        db.candidatos.insert_one(
            {
                "nome": nome,
                "cpf": cpf,
                "data_nasc": data_nasc,
                "contato": {
                    "email": email,
                    "telefone": telefone
                },
                "curso": {
                    "nome": curso_nome,
                    "instituicao": curso_instituicao
                },
                "habilidades": habilidades,
                "id_vaga": id_vaga,
                "id_situacao": id_situacao,
                "pretensao_salarial": pretensao_salarial,
                "link_curriculo": link_curriculo
            }
        )
        print(f'O candidato {nome} foi inserido com sucesso!')
    except errors.PyMongoError as e:
        print(f'Não foi possível adicionar o candidato: {e}')
    desconectar(conn)


def atualizar():

    conn = conectar()
    db = conn.projeto_rh

    _id = input('Informe o id do candidato:')
    nome = input("Informe o nome do candidato:")
    cpf = input("Informe o CPF do candidato:")
    data_nasc = input("Informe a data de nascimento do candidato (formato: AAAA-MM-DD):")
    email = input("Informe o email do candidato:")
    telefone = input("Informe o telefone do candidato:")
    curso_nome = input("Informe o nome do curso do candidato:")
    instituicao = input("Informe a instituição do curso do candidato:")
    habilidades = []
    print("Informe as habilidades (digite 'sair' quando terminar):")
    while True:
        habilidade_nome = input("Nome da habilidade: ")
        if habilidade_nome.lower() == 'sair':
            break
        habilidade_nivel = input("Nível da habilidade: ")
        habilidades.append({"nome": habilidade_nome, "nivel": habilidade_nivel})
    
    id_vaga = input("Informe o ID da vaga:")
    id_situacao = input("Informe o ID da situação:")
    pretensao_salarial = float(input("Informe a pretensão salarial do candidato:"))
    link_curriculo = input("Informe o link do currículo do candidato:")

    try: 
        if db.candidatos.count_documents({}) > 0:
            res = db.candidatos.update_one(
                {"_id": ObjectId(_id)},
                {
                    "$set": {
                        "nome": nome,
                        "cpf": cpf,
                        "data_nasc": data_nasc,
                        "contato": {
                            "email": email,
                            "telefone": telefone
                        },
                        "curso": {
                            "nome": curso_nome,
                            "instituicao": instituicao
                        },
                        "habilidades": habilidades,
                        "id_vaga": id_vaga,
                        "id_situacao": id_situacao,
                        "pretensao_salarial": pretensao_salarial,
                        "link_curriculo": link_curriculo
                    }
                }
            )
            if res.modified_count == 1:
                print('Candidato atualizado com sucesso!')
            else:
                print('Não foi possível atualizar o candidato :c')
        else:
            print('Não existem candidatos para serem atualizados')

    except errors.PyMongoError as e:
        print(f'Não foi possível acessar o banco de dados. {e}')
    except erros.InvalidId as f:
        print(f'Object Id inválido. {f}')
        
    desconectar(conn)


def deletar():
    
    conn = conectar()
    db =  conn.projeto_rh

    _id = input("Informe o id do candidato:")

    try:
        if db.candidatos.count_documents({}) > 0:
            res = db.candidatos.delete_one(
                {
                    "_id": ObjectId(_id)
                }
            )
            if res.deleted_count > 0:
                print('Candidato deletado com sucesso!')
            else:
                print("Não foi possível deletar")
        else:
            print("Não existem candidatos para serem deletados")
    except errors.PyMongoError as e:
        print(f'Erro ao acessar o banco de dados. {e}')
    except erros.InvalidId as f:
        print(f'Object Id invalido. {f}')
    desconectar(conn)


def menuCandidatos():

    print('-------------MENU CANDIDATOS -----------------')
    print('Selecione uma opcão: ')
    print('1 - Listar candidatos')
    print('2 - Inserir candidatos')
    print('3 - Atualizar candidatos')
    print('4 - Deletar candidatos')
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