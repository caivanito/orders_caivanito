import requests


def get_usd(url, params={}):
    #url = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
    #params = {'year': year, 'author': author}
    r = requests.get(url, params=params,  verify=False)
    cotizaciones = r.json()
    dolar_blue = ''
    for c in cotizaciones:
        if c['casa']['nombre'] == 'Dolar Blue':
            dolar_blue = c
    return dolar_blue