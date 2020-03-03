import pytest
from client import *
import random

rand_num = random.randint(0, 100)

create_params = {'username': 'quotas'+str(rand_num), 'moduser':'quotas'+str(rand_num),  'newuser': 'quotas'+str(rand_num),'passw': 'daa', 'email': 'qu@dmail.com', 'quota': 1}
login_params = {'username': 'quotas'+str(rand_num), 'passw': 'daa'}
login_params_admin = {'username': 'admin', 'passw': '321nimda'}


def test_user_zero_quotas():
    print("Creating user")
    login(login_params_admin)
    responce_ = new_user(create_params)
    logout('')
    login(login_params)
    query = {'area':'Greece', 'date':'2020-01-01', 'timeres':'PT30M', 'format':'json'}
    responce = actual_total_load(query)
    assert responce.status_code == 200
    responce = actual_total_load(query)
    assert responce.status_code == 500 # 500 -> error: no quotas
    logout('')
    return

    
