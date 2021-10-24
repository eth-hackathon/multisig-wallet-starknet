%lang starknet
%builtins pedersen range_check

from starkware.cairo.common.cairo_builtins import HashBuiltin
from starkware.starknet.common.storage import Storage
from starkware.starknet.common.syscalls import get_caller_address

# Storage.
@storage_var
func stored_number(account_id : felt) -> (res : felt):
end

# Anyone can save their personal number.
@external
func store_number{
        storage_ptr : Storage*, syscall_ptr : felt*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        number_to_store : felt):
    # Fetch the address of the contract that called this function.
    let (account_address) = get_caller_address()
    stored_number.write(account_address, number_to_store)
    return ()
end

# Anyone can view the number for any address.
@view
func view_number{storage_ptr : Storage*, pedersen_ptr : HashBuiltin*, range_check_ptr}(
        account_address : felt) -> (stored_num : felt):
    let (stored_num) = stored_number.read(account_address)
    return (stored_num)
end
