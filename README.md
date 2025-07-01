Finanças Automatizadas
======================
[![Sync transactions from Nubank to my YNAB(You Need A Budget) every day at 4am(7 utc)](https://github.com/lipemorais/financas-automatizadas/actions/workflows/sync-nubank-to-ynab.yml/badge.svg)](https://github.com/lipemorais/financas-automatizadas/actions/workflows/sync-nubank-to-ynab.yml)
---

Objetivo
--------
O objetivo desse projeto é pegar suas transações do Nubank e enviar para o YNAB

Prerequisites
-------------
You must go through [all the steps here](https://github.com/pluggyai/meu-pluggy?tab=readme-ov-file#connecting-your-bank-account-to-meupluggy) to create a MyPluggy account, a developer portal account, and link them together!

Use
---
### Running Locally
1. Fork this repo and clone your fork
2. [Install the `uv` Python package manager](https://docs.astral.sh/uv/getting-started/installation/#pypi)
3. Setup the repo:
   ```
   make setup
   ```
   and fill in the created `.env` file, using the comments as guidance on where to get the values.
3. Sync transactions with:
   ```
   make run
   ```

### Development
```
make test
```
