from starkware.crypto.signature.signature import (
    pedersen_hash, private_to_stark_key, sign)

private_key = 123456789987654322
message_hash = 2365826009273691707890899106612420763155492262135161736090313659483385404866 
public_key = private_to_stark_key(private_key)
signature = sign(
    msg_hash=message_hash, priv_key=private_key)
print(f'Public key: {public_key}')
print(f'Signature: {signature}')

