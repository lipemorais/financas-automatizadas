# TODO
- CRON options
  - Github Actions - https://docs.github.com/en/actions/learn-github-actions/events-that-trigger-workflows#scheduled-events
  - Cron no computador
  - Heroku Schedule
- Account
  - NICE_TO_HAVE: Send all transactions at once ynab.send_account_transaction
- NICE_TO_HAVE: Add mypy to verify type hint
- NICE_TO_HAVE: schemas
- add CI

# DONE 
 - Spikes with pynubank
 - Setup python-decouple
 - Spike with YNAB API
 - Tests instructions to README
 - Create a README
     - Setup instruction
 - Account
  - Put everything together on main
  - Get transactions
  - Filter transactions
  - Send it to ynab - transaction_schema = {"amount": 000, "category": "string", "date": "2021-09-07"}
- Card
  - Send it to ynab
  - Implement card sync at main function
  - Get card transactions
  - Filter card transactions
