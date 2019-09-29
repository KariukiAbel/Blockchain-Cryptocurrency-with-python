from functools import reduce
# import hashlib as hl
# from collections import OrderedDict
import json
# import pickle


# from hash_util import hash_string_256, hash_block
# from hash_util import hash_block
from block import Block
from transaction import Transaction
from utility.hash_util import hash_block
from utility.verification import Verification
from wallet import Wallet

# from verification import Verification

# use python3 for compilation
MINING_REWARD = 10


print(__name__)

class Blockchain:
    def __init__(self, hosting_node_id):
        genesis_block = Block(0, '', [], 100, 0)
        # initializing an empty private bockchain list
        # self.__chain = [genesis_block]
        self.chain = [genesis_block]
        self.__open_transactions = []
        self.hosting_node = hosting_node_id
        self.load_data()
        

    @property
    def chain(self):
        return self.__chain[:]


    @chain.setter
    def chain(self, val):
        self.__chain = val


    # def get_chain(self):
    #     return self.__chain[:]


    def get_open_transactions(self):
        return self.__open_transactions[:]


        # genesis_block = {
        #             'previous_hash': '',
        #             'index': 0,
        #             'transactions': [],
        #             'proof': 100
        #                 }
        # blockchain = [genesis_block]
        # blockchain = []
        # open_transactions = []
        # owner = 'abel'
        # participants = {'abel'}  # this is a set


    def load_data(self):
        # global blockchain
        # global open_transactions
        try:
            # with open('blockchain.p', mode = 'rb') as f:
            with open('blockchain.txt', mode = 'r') as f:
                file_content = f.readlines()
                # file_content = pickle.loads(f.read())
                # print(file_content)          
                # blockchain = file_content ['chain']
                # open_transactions = file_content ['ot']
                blockchain = json.loads(file_content[0][:-1])
                # open_transactions = json.loads(file_content[1])
                # blockchain = [{'previous_hash': block['previos_hash'], 'index': block['index'], 'proof': block['proof'], 'transactions': []} for block in blockchain]
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    # converted_tx = [OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'] )]) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    # updated_block = {
                    #     'previous_hash': block['previous_hash'],
                    #     'index': block['index'],
                    #     'proof': block['proof'],
                    #     'transactions': [OrderedDict(
                    #         [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'] )]) for tx in block['transactions']]
                    # }
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    # updated_transaction = OrderedDict([('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'] )])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
            # # genesis_block = {
            # #         'previous_hash': '',
            # #         'index': 0,
            # #         'transactions': [],
            # #         'proof': 100
            # #             }
            # blockchain = [genesis_block]
            # open_transactions = []
            print('Handled Exception...')
            pass
        finally:
            print('Clean up')


    def save_data(self):
        try:
            # with open('blockchain.p', mode = 'wb') as f:
            with open('blockchain.txt', mode = 'w') as f:
                # # f.write(str(blockchain))
                # # f.write('\n')
                # f.write(str(open_transactions))
                savable_chain = [block.__dict__ for block in [Block(block_el.index, 
                block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], 
                block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                # f.write(json.dumps(blockchain))
                f.write(json.dumps(savable_chain))
                f.write('\n')
                savable_tx = [tx.__dict__ for tx in self.__open_transactions]
                # f.write(json.dumps(open_transactions))
                f.write(json.dumps(savable_tx))
                # save_data = {
                #     'chain': blockchain,
                #     'ot': open_transactions
                # }
                # f.write(pickle.dumps(save_data))
        except IOError:
            print('Saving failed')


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
            proof += 1
        return proof


    def get_balance(self):
        if self.hosting_node == None:
            return None
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == participant] for block in self.__chain]
        # tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
        open_tx_sender = [tx.amount
                        for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                            if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        # amount_sent = 0
        # for tx in tx_sender:
        #     if len(tx) > 0:
        #         amount_sent += tx[0]
        tx_recipient = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]
        # amount_received = 0
        amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                                if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
        # for tx in tx_recipient:
        #     if len(tx) > 0:
        #         amount_received += tx[0]
        return amount_received - amount_sent


    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain."""
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]


    def add_transaction(self, recipient, sender, signature, amount = 1.0):
        """ Append a new value as well as the last blockchain value to the blockchain.
        
        Arguements:
        :sender :The sender of the coins.
        :recipient: The recipient of the coins
        :Amount : The amount of coins sent with the transaction (default is 1.0).
        """
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        #             }
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        # if not Wallet.verify_transaction(transaction):
        #     return False
        # transaction = OrderedDict(
        #     [('sender', sender), ('recipient', recipient), ('amount', amount )])
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            # participants.add(sender)
            # participants.add(recipient)
            self.save_data()
            return True
        return False


    def mine_block(self):
        if self.hosting_node == None:
            return None
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        # print(hashed_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #         'sender': 'MINING',
        #         'recipient': owner,
        #         'amount': MINING_REWARD
        #             }
        reward_transaction = Transaction('MINING', self.hosting_node, '', MINING_REWARD)
        # reward_transaction = OrderedDict(
        #                 [('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                # return False
                return None
        copied_transactions.append(reward_transaction)
        # print (hashed_block)

        # for key in last_block:
        #     value = last_block[key]
        #     hashed_block = hashed_block + str(value)

        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        # for tx in block.transactions:
        #     if not Wallet.verify_transaction(tx):
        #         return False
        # block = {
        #         'previous_hash': hashed_block,
        #         'index': len(blockchain),
        #         'transactions': copied_transactions,
        #         'proof': proof
        # }
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return block


# tx_amount = get_transaction_value()
# add_value(tx_amount)