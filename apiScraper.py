import requests
import pandas as pd
from datetime import datetime, timedelta


class ApiScraper:
    def __init__(self, guid, token):
        self.guid = guid
        self.token = token
        self.session = requests.session()
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        self.session.headers.update(headers)
        self.session.headers.update({'Authorization': self.token})
        self.session.headers.update({'guid': self.guid})

    def getTotal(self,date=None):
        if date is None:
            date = self.yesterday
        response = self.session.get(
            f'https://investidor.b3.com.br/api/home/v2/total-acumulado?dc={date}T00:00:00&cache-guid={self.guid}',
            verify=False
        )
        self.total = (
            pd.json_normalize(response.json())
            .assign(data=lambda x: pd.to_datetime(x['data']))
            .set_index('data')
        )
        return self.total

    def get_positions(self, date=None):
        if date is None:
            date = self.yesterday
        page = 1
        params = {
            'data': date,
        }

        while True:
            response = self.session.get(
                f'https://investidor.b3.com.br/api/extrato-posicao/v1/posicao/{page}',
                params=params,
                verify=False
            )

            df = (
                pd.json_normalize(response.json()['itens'], record_path=['posicoes'], meta=[
                                  'categoriaProduto', 'tipoProduto', 'descricaoTipoProduto'])
                .drop(columns=['temBloqueio', 'marcacoes', 'emissor', 'escriturador', 'administrador', 'documento', 'codigoIsin', 'existeLogotipo', 'classeAtivo', 'documentoInstituicao', 'descricaoTipoProduto', 'razaoSocial', 'tipoRegime', 'categoriaProduto', 'tipoIf'])
                .assign(vencimento = lambda x: pd.to_datetime(x['vencimento']))
                .assign(dataEmissao = lambda x: pd.to_datetime(x['dataEmissao']))
                .assign(dataReferencia = lambda x: pd.to_datetime(x['dataReferencia']))
            )
            if page == 1:
                self.positions = df
            else:
                self.positions.append(df)
            if response.json()['paginaAtual'] == response.json()['totalPaginas']:
                break
            page = page + 1

        return self.positions
