from vagas import menuVagas
from candidatos import menuCandidatos
from processoSeletivo import menuProcesso

def menu_principal():
    while True:
        print('--------- MENU PRINCIPAL ----------')
        print('Selecione uma opção: ')
        print('1 - Vagas')
        print('2 - Candidatos')
        print('3 - Processo Seletivo')
        print('0 - Sair')
        opcao = int(input())

        if opcao == 0:
            print('Saindo do programa')
            break
        elif opcao == 1:
            menuVagas()  
        elif opcao == 2:
            menuCandidatos() 
        elif opcao == 3:
            menuProcesso()  
        else:
            print('Opção inválida! Tente novamente.')

if __name__ == "__main__":
    menu_principal()
