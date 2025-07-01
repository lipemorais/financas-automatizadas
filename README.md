Finanças Automatizadas
======================
[![Sync transactions from Nubank to my YNAB(You Need A Budget) every day at 4am(7 utc)](https://github.com/lipemorais/financas-automatizadas/actions/workflows/sync-nubank-to-ynab.yml/badge.svg)](https://github.com/lipemorais/financas-automatizadas/actions/workflows/sync-nubank-to-ynab.yml)
---

Objetivo
--------
O objetivo desse projeto é pegar suas transações do Nubank e enviar para o YNAB

Prerequisites
------------
1. An account with `pluggy.ai`
1. A connection to Nubank in Pluggy, created
1. The `Client ID` and `Client Secret` of that connection
1. An application created in `pluggy.ai`
    - `CLIENT_ID`
    - `CLIENT_SECRET`
1. Nubank account IDs (from My Pluggy)
1. Copy the `.env.example` to be




## Como emitir o certificado
1. Entre na virtualenv usando o comando `pipenv shell`
2. Execute o commando `pynubank` e siga o processo
3. Para gerar o base64 do certificado utilize o comando `cat cert.p12 | base64 | pbcopy`
4. Com isso vá a váriável de ambiente  `NUBANK CERTIFICATE` no github, cole o certificado em base64 e salve
5. Tudo dever voltar a funcionar como deveria

## Tasks

### Setup
`make setup` or `make s`

### Test
`make test` or `make t`

### Run
`make run` or `make r`

# Resources

- YNAB API doc => https://api.youneedabudget.com/v1
