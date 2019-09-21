import hashlib as hl
import json


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    # return '-'.join([str(block [key]) for key in block])
    # return hashlib.sha256(json.dumps(block).encode()).hexdigest()
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys = True).encode())
    # return hash_string_256(json.dumps(block, sort_keys = True).encode())