import requests
import pandas as pd
from datetime import datetime, timedelta
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class ApiScraper:
    def __init__(self, guid, token):
        self.guid = guid
        self.token = token
        self.session = requests.session()
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.yesterday = (datetime.today() - timedelta(days=1)
                          ).strftime("%Y-%m-%d")
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
        }
        self.session.headers.update(headers)
        self.session.headers.update({'Authorization': self.token})
        self.session.headers.update({'guid': self.guid})

    def getTotal(self, date=None):
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
            to_drop = [
                'temBloqueio',
                'marcacoes',
                'emissor',
                'escriturador',
                'administrador',
                'documento',
                'codigoIsin',
                'existeLogotipo',
                'classeAtivo',
                'documentoInstituicao',
                'descricaoTipoProduto',
                'razaoSocial',
                'tipoRegime',
                'categoriaProduto',
                'tipoIf'
            ]
            df = (
                pd.json_normalize(response.json()['itens'], record_path=['posicoes'], meta=[
                                  'categoriaProduto', 'tipoProduto', 'descricaoTipoProduto'])
                .drop(columns=to_drop, errors='ignore')
                .assign(vencimento=lambda x: pd.to_datetime(x['vencimento']))
                .assign(dataEmissao=lambda x: pd.to_datetime(x['dataEmissao']))
                .assign(dataReferencia=lambda x: pd.to_datetime(x['dataReferencia']))
            )
            if page == 1:
                self.positions = df
            else:
                self.positions.append(df)
            if response.json()['paginaAtual'] == response.json()['totalPaginas']:
                break
            page = page + 1

        return self.positions

    def get_trades(self, dateStart=None, dateEnd=None, write=False):
        if dateStart is None:
            dateStart = (datetime.today() - timedelta(days=31)
                         ).strftime("%Y-%m-%d")
        if dateEnd is None:
            dateEnd is self.yesterday
        params = {
            'dataInicio': dateStart,
            'dataFim': dateEnd,
        }
        page = 1
        self.trades = pd.DataFrame()
        
        while True:
            response = self.session.get(
                f'https://investidor.b3.com.br/api/extrato-negociacao-ativos/v1/negociacao-ativos/{page}',
                params=params,
                verify=False
            )
            for item in response.json()['itens']:
                self.trades = pd.concat([self.trades, (pd.json_normalize(
                    item, record_path='negociacaoAtivos', meta='data'))])
            if response.json()['paginaAtual'] == response.json()['totalPaginas']:
                break
            curPage = response.json()['paginaAtual']
            totPages = response.json()['totalPaginas']
            print(f'Scraped trades page {curPage} of {totPages}')
            page = page + 1
        if write:
            self.trades.to_csv(f'trades_{dateStart}_{dateEnd}.csv')
            print(f'Saved trades file: trades_{dateStart}_{dateEnd}.csv')
        return self.trades

    def get_earnings(self, dateStart=None, dateEnd=None, write=False):
        if dateStart is None:
            dateStart = (datetime.today() - timedelta(days=31)
                         ).strftime("%Y-%m-%d")
        if dateEnd is None:
            dateEnd is self.yesterday
        page = 1
        self.earnings = pd.DataFrame()
        while True:
            params = {
                'dti': dateStart,
                'dtf': dateEnd,
                'p': page,
            }
            response = self.session.get(
                f'https://investidor.b3.com.br/api/extrato-eventos-provisionados/v1/recebidos',
                params=params,
                verify=False
            )
            df = (
                pd.json_normalize(
                    response.json()['d'], record_path='proventos')
                .drop(columns=['qtdTotalPaginas', 'qtdTotalItens', 'id'])
                .assign(dataPagamento=lambda x: pd.to_datetime(x['dataPagamento']))
            )
            self.earnings = pd.concat([self.earnings, df])
            if response.json()['np'] == response.json()['pn']:
                break
            page = page + 1
        if write:
            self.earnings.to_csv(f'earnings_{dateStart}_{dateEnd}.csv')
        return self.earnings

    def get_positions_earnings(self, dateStart=None, dateEnd=None, write=False):
        if dateStart is None:
            dateStart = (datetime.today() - timedelta(days=31)
                         ).strftime("%Y-%m-%d")
        if dateEnd is None:
            dateEnd is self.yesterday

        params = {
            'dataInicio': dateStart,
            'dataFim': dateEnd,
        }
        page = 1
        self.positionsEarnings = pd.DataFrame()
        while True:
            response = self.session.get(
                f'https://investidor.b3.com.br/api/extrato-movimentacao/v1.2/movimentacao/{page}',
                params=params,
                verify=False,
            )
            df = (
                pd.json_normalize(
                    response.json()['itens'], record_path='movimentacoes', meta='data')
                .assign(data=lambda x: pd.to_datetime(x['data']))
            )

            self.positionsEarnings = pd.concat([self.positionsEarnings, df])
            if response.json()['paginaAtual'] == response.json()['totalPaginas']:
                break
            page = page + 1
        if write:
            self.positionsEarnings.to_csv(f'positionsEarnings_{dateStart}_{dateEnd}.csv')
        return self.positionsEarnings

    def get_future_earnings(self, date=None):
        if date is None:
            date = (datetime.today() - timedelta(days=10)).strftime("%Y-%m-%d")
        params = {
            'data': date,
            'filtroEventosProvisionados': [
                '1',
                '2',
                '3',
                '4',
            ],
        }
        page = 1
        self.futureEarnings = pd.DataFrame()
        while True:
            response = self.session.get(
                f'https://investidor.b3.com.br/api/extrato-eventos-provisionados/v1.4/receber/{page}',
                params=params,
                verify=False
            )
            df = (
                pd.json_normalize(response.json()['itens'])
                .assign(previsaoPagamento=lambda x: pd.to_datetime(x['previsaoPagamento']))
            )
            self.futureEarnings = pd.concat([self.futureEarnings, df])
            if response.json()['paginaAtual'] == response.json()['totalPaginas']:
                break
            page = page + 1
        return self.futureEarnings

    def get_hist_positions(self, dateStart=None, dateEnd=None, freq='MS', write=False):
        if dateStart is None:
            dateStart = (datetime.today() - timedelta(days=30)
                         ).strftime("%Y-%m-%d")
        if dateEnd is None:
            dateEnd = datetime.today().strftime("%Y-%m-%d")
        self.historicalPositions = pd.DataFrame()
        for dt in pd.date_range(dateStart, dateEnd, freq=freq):
            print(f'Getting position from date: {dt.strftime("%Y-%m-%d")}')
            df = self.get_positions(dt.strftime("%Y-%m-%d"))
            df['date'] = dt
            self.historicalPositions = pd.concat([self.historicalPositions, df])
        if write:
            self.historicalPositions.to_csv(f'histPos_{dateStart}_{dateEnd}.csv')
        return self.historicalPositions
