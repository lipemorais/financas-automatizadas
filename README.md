# Finanças Automatizadas
[![Sync transactions from Nubank to my YNAB(You Need A Budget) every day at 4am(7 utc)](https://github.com/lipemorais/financas-automatizadas/actions/workflows/sync-nubank-to-ynab.yml/badge.svg)](https://github.com/lipemorais/financas-automatizadas/actions/workflows/sync-nubank-to-ynab.yml)
---

## Objetivo
O objetivo desse projeto é pegar suas transações do Nubank e enviar para o YNAB

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
