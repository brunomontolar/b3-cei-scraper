# b3-cei-scraper
## Simples scraper para baixar informações da B3.

---
## Arquivo de configuração
- Utilize o arquivo `config.yml` para incluir as variáveis necessárias para fazer a consulta.
- Preencha conforme modelo abaixo:
```
---
# Login
auth:
    user: "apenasNumerosDoCpf"
    password: "suaSenha"
    token:
    cacheGuid:
# Consultas
total:
    date:
positions:
    date:
trades:
    dateStart:
    dateEnd:
```
## Acesso do usuário
### 1- Modo com login e senha
Neste modo, o programa abrirá automaticamente uma janela do Chrome e preencherá os dados do login. No momento em que aparecer o CAPTCHA, ele aguardará a resolução manual para prosseguir.

Concluído o CAPTCHA, ele prosseguirá automaticamente. Fechará a janela e executará as consultas conforme definido abaixo.

**Informações necessárias**
- Preencher o cpf no `user`
- Preencher a senha no `password`
### 2- Utilizando token e cacheGuid
Caso tenha preechido a variável `token` e a `cacheGuid`, o programa pulará automaticamente a parte de login com o Chrome e já fará as consultas definidas.

**É necessário que os valores preenchidos sejam os obtidos de uma sessão válida**

```
authentication:
    token:
    cacheGuid:
```

---

## Posições
- Filtrar a data na qual deseja saber as posições
- Datas entre 01/11/2019 e ontem
- Formato AAAA-MM-DD
- **Padrão data de ontem**
```
positions:
    date: "01-01-2022"
```
## Total da carteira
- Escolher a data da qual da qual deseja saber o valor total da carteira
- Datas entre 01/11/2019 e ontem
- Formato AAAA-MM-DD
- **Padrão data de ontem**
```
total:
    date: "01-01-2022"
```
## Negociações
- Período igual ou inferior a 12 meses
- Formato AAAA-MM-DD
- Escolher data inicial e data final do filtro
- **Como padrão, são escolhidos os últimos 30 dias, contando a partir de ontem**
```
trades:
    dateStart:
    dateEnd:
```

## Dividendos
- Período igual ou inferior a 12 meses
- Formato AAAA-MM-DD
- Escolher data inicial e data final do filtro
- **Como padrão, são escolhidos os últimos 30 dias, contando a partir de ontem**
```
earnings:
    dateStart:
    dateEnd:
    write:
```

## Dividendos
TODO:
Escrever detalhes da função get_earnings
Referente às remunerações de dividendos, juros de capital próprio e outros redimentos
Definir data padrão para filtros

## Remuneração em ações 
TODO:
Escrever detalhes da função get_positions_earnings
Referente às remunerações em posições

## Remuneração futura
TODO:
Escrever detalhes da função get_future_earnings
Referente às remunerações futuras
Definir data padrão para filtro
Trabalhar na validação se o a data é válida (erro de data não poder ser superior à carga)
Trabalhar na validação se a resposta não está vazia

