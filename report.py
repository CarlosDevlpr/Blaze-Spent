from codecs import getdecoder
from os import access
import requests as req
from functional_python import pipe


print('\n\n>>>Bem vindo a calculadora do blaze <<<')

def data_api(transaction, page, access_token):
    return req.get(f"https://blaze.com/api/{transaction}?page={page}", headers ={"authorization":'Bearer ' + access_token, "user-agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1","authority":"blaze.com"}).json()

def askCredentials():
    print('Coloque as suas credenciais abaixo\n')
    username = input('Qual o seu email na blaze? ')
    password = input('Qual a sua senha na blaze? ')
    credentials = {'username': username, 'password': password}
    return credentials

def loginBlaze(credentials): 
    print('\nLogando na sua conta...')
    access_token = req.put('https://blaze.com/api/auth/password', json=credentials).json()['access_token']
    return access_token

def getDeposits(access_token):
    print('\nExtraindo depósitos...')
    deposits = data_api('deposits', 1, access_token)
    pages = deposits['meta']['total_pages']
    records = int(deposits['meta']['total_records'])
    if pages == 1:
        amount = 0
        for record in range(records):
            amount += float(deposits['records'][record]['amount'])
    if pages > 1:
        amount = 0
        for page in range(pages):
            this_page_deposits = data_api('deposits', page, access_token)
            for record in range(records):
                amount += this_page_deposits['records'][record]['amount']
    print(f'Você já depositou: R$:{amount}')
    return access_token

def getWithdrawals(access_token):
    print('\nExtraindo saques...')
    withdrawals = data_api('withdrawals', 1, access_token)
    pages = withdrawals['meta']['total_pages']
    records = int(withdrawals['meta']['total_records'])
    if pages == 1:
        amount = 0
        for record in range(records):
            this_record = withdrawals['records'][record]

            if this_record['status'] == 'complete':
                amount += float(this_record['amount'])
            if this_record['status'] == 'refunded':
                pass
    if pages > 1:
        amount = 0
        for page in range(pages):
            this_page_withdrawals = data_api('withdrawals', page, access_token)
            for record in range(records):
                this_record = this_page_withdrawals['records'][record]
                if this_record['status'] == 'complete':
                    amount += this_record['amount']
                if this_record['status'] == 'refunded':
                    pass
    print(f'Você já sacou: R$:{amount}')
    return amount

depositsPipe = pipe(
    loginBlaze,
    getDeposits
)

getWithdrawals(getDeposits(loginBlaze(askCredentials())))

