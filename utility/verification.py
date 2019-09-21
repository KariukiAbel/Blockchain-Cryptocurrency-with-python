"""Provides some verification helper methods."""

# from hash_util import hash_string_256, hash_block
from utility.hash_util import hash_string_256, hash_block


class Verification:
    @staticmethod
    def valid_proof(transactions, last_hash, proof):
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
        guess_hash = hash_string_256(guess)
        print(guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        # # block_index= 0
        # is_valid = True
        # for block_index in range (len(blockchain)):
        #     if block_index == 0:
        #         continue
        #     elif blockchain[block_index][0] == blockchain[block_index - 1]:
        #         is_valid = True
        #     else:
        #         is_valid = False
        #         # break
        # # for block in blockchain:
        # #     if block_index == 0:
        # #         block_index += 1
        # #         continue
        # #     elif block[0] == blockchain[block_index - 1]:
        # #         is_valid = True
        # #     else:
        # #         is_valid = False
        # #         break
        # #         block_index =+ 1
        # return is_valid
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index -1]):
                return False
            if not cls.valid_proof(block.transactions[: -1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance):
        sender_balance = get_balance()
        return sender_balance >= transaction.amount

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        # is_valid = True
    # for tx in open_transactions:
    #     if verify_transaction(tx):
    #         is_valid = True
    #     else:
    #         is_valid = False
    # return is_valid
        """Verifies all open transactions"""
        return all([cls.verify_transaction(tx, get_balance) for tx in open_transactions])