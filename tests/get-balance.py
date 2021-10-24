from starkware.starknet.public.abi import get_storage_var_address

user = 1628448741648245036800002906075225705100596136133912895015035902954123957052
user_balance_key = get_storage_var_address('balance', user)
print(f'Storage key for user {user}:\n{user_balance_key}')
