import requests
import yaml
import queries 
import pyfiglet
from art import art
from rich.console import Console
from rich.panel import Panel



def lista_moedas():
    response = queries.listar_moeda()

    print("Segue a lista de criptomoedas disponiveis.")
    print("-----------------------------------------------------------------------")
    
    for i in response:
        
        print(f"Nome da Criptomoeda: {i['name']} || Simbolo: {i['symbol']} || ID: {i['id']}")
        print(" ")


    escolha = input("\nDeseja verificar uma criptomoeda? (1 - Sim / 2 - Não): ")
    if escolha == "1":
        opcao_buscar_cripto(obter_ids_moedas())


    

def obter_ids_moedas():
    response = queries.listar_moeda()
    return {i["id"] for i in response}


def buscar_cripto(ids_moeda):    
        
        moeda = input("Insira o ID da moeda (Exemplo: bitcoin): ").lower()
       
        while moeda not in ids_moeda:
            print("Id inválido! Insira um ID correto.")
            moeda = input("Insira o ID da moeda (Exemplo: bitcoin): ").lower()

        moeda_corrente = input("Insira a moeda corrente (Exemplo: usd): ").lower()

        response = queries.moeda_preco(moeda, moeda_corrente)

        valor_escolhido = response[moeda][moeda_corrente]

        print(f"O valor de {moeda} em {moeda_corrente} é de: {format(valor_escolhido, '.2f')} {moeda_corrente.upper()}")

        return moeda, moeda_corrente

    
def informacoes_adicionais(moeda, moeda_corrente): 
    response = queries.informacao_moeda(moeda, moeda_corrente)

    data = response

    include_market_cap = f"{moeda_corrente}_market_cap"  
    include_24hr_vol = f"{moeda_corrente}_24h_vol" 
    include_24hr_change = f"{moeda_corrente}_24h_change"


    if moeda in data and include_market_cap in data[moeda]: 
        print(f"Valor de mercado da cripto {moeda} em {moeda_corrente.upper()}: {data[moeda][include_market_cap]}")
    else:
        print("Market Cap não encontrado.")

    if moeda in data and include_24hr_vol in data[moeda]: 
        print(f"Volume de transações na última hora da cripto {moeda}: {data[moeda][include_24hr_vol]}")
    else:
        print("Volume de transações não encontrado.")
 
    if moeda in data and include_24hr_change in data[moeda]: 
        print(f"Alteração de valor da cripto {moeda} nas ultimas 24 horas: {data[moeda][include_24hr_change]}")
    else:
        print("Alteração de valor não encontrada.")


def conversor_moeda():

    moeda = input("Insira o id criptomoeda que deseja converter: (Exemplo bitcoin, ethereum) ")
    quantidade_moeda = float(input("Insira quantidade da criptomoeda que deseja comparar: (Exemplo: 0.05) "))
    conversao = input("Deseja converter o valor para outra criptomoeda ou para moeda fiduciária? (1 - Criptomoeda / 2 - Moeda Fiduciária) ")

    if conversao == '1':
        moeda_fiduciaria = "usd"
        cripto_comparada = input("Insira o ID da outra criptomoeda para concluir a conversão: ").lower()
        response = queries.moeda_preco(moeda, moeda_fiduciaria)
        valor_cripto_original = response[moeda][moeda_fiduciaria]
        response_2 = queries.moeda_preco(cripto_comparada, moeda_fiduciaria)
        valor_cripto_comparada = response_2[cripto_comparada][moeda_fiduciaria]

        conversao = (quantidade_moeda * valor_cripto_original) / valor_cripto_comparada

        print(f"{quantidade_moeda} {moeda} equivalem a {conversao} {cripto_comparada}.")


    elif conversao == '2':
        moeda_comparada = input("Insira a moeda fiduciaria para ser comparada: (Exemplo BRL, USD) ").lower()
        response = queries.moeda_preco(moeda, moeda_comparada)
        valor_cripto_original = response[moeda][moeda_comparada]

        valor_convertido = valor_cripto_original * quantidade_moeda

        print(f"Os {quantidade_moeda} {moeda} convertidos equivalem a {valor_convertido} em {moeda_comparada}")


    else:
        print("Opção não disponível")

def opcao_buscar_cripto(ids_moeda):
    moeda, moeda_corrente = buscar_cripto(ids_moeda)
    escolha = input("\nDeseja obter mais informações? (1 - Sim / 2 - Não): ")

    if escolha == "1":
        informacoes_adicionais(moeda, moeda_corrente)

def main_2():
    ascii_banner = pyfiglet.figlet_format("CryptoSeeker")

    console = Console()

    panel = Panel(ascii_banner, title="Bem-vindo ao CryptoSeeker!", subtitle="Desenvolvido por: Lucas Luiz (Trayonn)", expand=False)

    console.print(panel)

    print("Carregando dados das moedas...")
    ids_moeda = obter_ids_moedas()

    opcoes = {
        "1": lambda: opcao_buscar_cripto(ids_moeda),
        "2": lista_moedas,
        "3": conversor_moeda
    }

    while True:
        escolha = input("\nEscolha uma opção: \n"
                        "1- Buscar uma criptomoeda pelo ID\n"
                        "2- Ver lista de IDs criptomoedas\n"
                        "3- Conversor de Moedas\n"
                        "0- Sair\n"
                        "Digite sua escolha: ")
        
        if escolha == "0":
            print("Saindo o CryptoSeeker. Adeus!")
            break

        opcao = opcoes.get(escolha)
        if opcao:
            opcao()
        else:
            print("Opção inválida! Tente novamente.")

    pass

        

if __name__ == "__main__":
    
    print("###############################")
    
    main_2()



