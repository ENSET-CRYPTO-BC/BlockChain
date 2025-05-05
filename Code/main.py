from Utils.crypto_utils import *
import base64

data = {i: i * 3.12 for i in range(10)}

keys = generate_keys_pairs()
print(keys)

signature = generate_signature(data, keys[0])
print(signature)

has_ = generate_hash(dump_data(data))
print(has_)
print(len(has_))

verif = verify_signature(data=data, public_key_str=keys[1], signature_str=signature)
print(verif)
