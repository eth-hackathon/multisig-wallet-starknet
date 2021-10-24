# Requires cairo-lang >= 0.4.1
import pytest
import asyncio
from starkware.starknet.testing.starknet import Starknet
from utils.Account import Account

# Create signers that use a private key to sign transaction objects.
NUM_SIGNING_ACCOUNTS = 1
DUMMY_PRIVATE = 123456789987654321
# All accounts currently have the same L1 fallback address.
L1_ADDRESS = 0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984

@pytest.fixture(scope='module')
def event_loop():
    return asyncio.new_event_loop()

@pytest.fixture(scope='module')
async def account_factory():
    # Initialize network
    starknet = await Starknet.empty()
    accounts = []
    print(f'Deploying {NUM_SIGNING_ACCOUNTS} accounts...')
    for i in range(NUM_SIGNING_ACCOUNTS):
        account = Account(DUMMY_PRIVATE + i, L1_ADDRESS)
        await account.create(starknet)
        accounts.append(account)
        print(f'Account {i} is: {account}')

    # Admin is usually accounts[0], user_1 = accounts[1].
    # To build a transaction to call func_xyz(arg_1, arg_2)
    # on a TargetContract:

    # user_1 = accounts[1]
    # await user_1.tx_with_nonce(
    #     to=TargetContractAddress,
    #     selector_name='func_xyz',
    #     calldata=[arg_1, arg_2])
    return starknet, accounts


@pytest.fixture(scope='module')
async def application_factory(account_factory):
    starknet, accounts = account_factory
    application = await starknet.deploy("contracts/application.cairo")
    print('deploy application contract')
    return starknet, accounts, application

@pytest.mark.asyncio
async def test_store_number(application_factory):
    _, accounts, application = application_factory
    # Let two different users save a number.
    user_0 = accounts[0]
    user_0_number = 543
    # user_1 = accounts[1]
    # user_1_number = 888

    await user_0.tx_with_nonce(
        to=application.contract_address,
        selector_name='store_number',
        calldata=[user_0_number])
    print('DID IT')

    # await user_1.tx_with_nonce(
    #         to=application.contract_address,
    #         selector_name='store_number',
    #         calldata=[user_1_number])

    # View transactions don't require an authorized transaction.
    (user_0_stored, ) = await application.view_number(
        user_0.address).invoke()
    # (user_1_stored, ) = await application.view_number(
    #     user_1.address).invoke()

    assert user_0_stored == user_0_number
    # assert user_0_stored == user_0_number
