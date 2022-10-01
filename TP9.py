import psutil, webbrowser, requests, json
from bs4 import BeautifulSoup
from beautifultable import BeautifulTable

def menu():
    ativa_menu = True
    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    table.columns.header = ["", "Menu"]
    table.rows.append(['1', 'Notícias'])
    table.rows.append(['2', 'Clima'])
    table.rows.append(['3', 'Aplicação Web - Spotify'])
    table.rows.append(['4', 'E-Sports'])
    table.rows.append(['5', 'CPU | Memória'])
    table.rows.append(['0', 'Sair'])
    while ativa_menu:
        print(table)
        try:
            escolha = int(input('Escolha uma opção:'))
            if escolha < 0 or escolha > 5:
                print('Opção inválida!')
            else:
                if escolha == 1:
                    informar_noticias()
                elif escolha == 2:
                    informar_clima()
                elif escolha == 3:
                    abrir_aplicacao()
                elif escolha == 4:
                    varrer_web()
                elif escolha == 5:
                    informar_psutil()
                elif escolha == 0:
                    ativa_menu = False
        except ValueError:
            print('Apenas números inteiros!')

def informar_noticias():
    site = requests.get('http://g1.globo.com/ultimas-noticias.html')
    soup = BeautifulSoup(site.text, 'html.parser')
    noticias_dic = {}
    contador = 1
    table = BeautifulTable()

    table.columns.header = ['', "NOTÍCIAS"]
    table.columns.alignment['NOTÍCIAS'] = BeautifulTable.ALIGN_LEFT
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)

    for noticia in soup.find_all('div', {'class': 'feed-post-body-title gui-color-primary gui-color-hover'}):
        table.rows.append([contador, noticia.text.replace('\n', '')])
        noticias_dic[contador] = noticia.text
        contador += 1
    print(table)

    with open('.\\json\\noticias.json', 'w') as file:
        json.dump(noticias_dic, file, indent=4)

def informar_clima():
    url = 'http://api.openweathermap.org/data/2.5/weather?id=3451190&units=metric&lang=pt&appid='

    with open('.\\config\\config.json', 'r') as configuracao:
        key = json.load(configuracao)

    chave = key['key']
    requisicao = requests.post(url + chave, json={'key': 'value'})
    requisicao_dados = requisicao.json()

    table = BeautifulTable()
    table.columns.header = ["Cidade", "Temperatura corrente", 'Temperatura Máxima', 'Temperatura Mínima',
                            'Condição climática', 'Umidade']
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    table.rows.append([requisicao_dados['name'],
                      str(requisicao_dados['main']['temp']) + 'ºC',
                      str(requisicao_dados['main']['temp_max']) + 'ºC',
                      str(requisicao_dados['main']['temp_min']) + 'ºC',
                      requisicao_dados['weather'][0]['description'],
                      str(requisicao_dados['main']['humidity']) + '%'])
    print(table)
    data = {
        requisicao_dados['name']: {
            'Corrente': requisicao_dados['main']['temp'],
            'Temperatura Mín': requisicao_dados['main']['temp_min'],
            'Temperatura Máx': requisicao_dados['main']['temp_max'],
            'Condição Climática': requisicao_dados['weather'][0]['description'],
            'Umidade': requisicao_dados['main']['humidity']
        },
    }

    with open('.\\json\\dados_clima.json', 'w') as file:
        json.dump(data, file, indent=4)

def abrir_aplicacao():
    url = "https://www.spotify.com/br/"
    webbrowser.get(None).open(url)

def varrer_web():
    url = 'https://canaltech.com.br/esports/'
    site = requests.get(url)
    soup = BeautifulSoup(site.text, 'html.parser')
    noticias_esports = {}
    contador = 1

    table = BeautifulTable()
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    table.columns.header = ["", "NOTíCIAS E-SPOSTS"]
    table.columns.alignment["NOTíCIAS E-SPOSTS"] = BeautifulTable.ALIGN_LEFT

    for noticia in soup.find_all('h5', {'class': 'title'})[:5]:
        table.rows.append([contador, noticia.text.replace('\n', '')])
        noticias_esports[contador] = noticia.text
        contador += 1
    print(table)

    with open('.\\json\\noticias_esports.json', 'w') as file:
        json.dump(noticias_esports, file, indent=4)

def informar_psutil():
    info_memoria = psutil.virtual_memory()
    memoria_total = round(info_memoria.total / (1024 * 1024 * 1024), 2)
    memoria_disponivel = round(info_memoria.free / (1024 * 1024 * 1024), 2)
    memoria_uso = info_memoria.percent
    uso_cpu = psutil.cpu_percent()

    data = {
        'Memoria Total': str(memoria_total) + 'GB',
        'Memoria Utilizada': str(memoria_uso) + '%',
        'Memoria Disponivel': str(memoria_disponivel) + 'GB',
        'Uso de CPU': str(uso_cpu) + '%'
    }

    table = BeautifulTable()
    table.columns.header = ["Informação", "Uso"]
    table.columns.alignment["Informação"] = BeautifulTable.ALIGN_LEFT
    table.columns.alignment["Uso"] = BeautifulTable.ALIGN_LEFT
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    for key, value in data.items():
        table.rows.append([key, value])
    print(table)

    with open('.\\json\\dados_de_uso.json', 'w') as file:
        json.dump(data, file, indent=4)

menu()
