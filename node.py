from blockchain import Blockchain
from uuid import uuid4
from utility.verification import Verification
from wallet import Wallet



class Node:
    def __init__(self):
        # self.id = str(uuid4())
        # self.id = 'abel'
        self.wallet = Wallet()
        self.blockchain = Blockchain(self.wallet.public_key)


    def get_transaction_value(self):
        """ Returns the input of the user (a new transaction amount) as a float."""
        tx_recipient = input('Enter the recipient of the transaction: ')
        tx_amount = float(input('Your transation amount please: '))
        return tx_recipient, tx_amount


    def get_user_choice(self):
        user_input = input('Your choice: ')
        return user_input


    def print_blockchain_elements(self):
        """ Output all blocks in the blockchain """
        # output the blockchain list to the console
        for block in self.blockchain.chain:
            print("Outputting Block")
            print(block)
        else:
            print('-' * 20)


    def listen_for_input(self):
        waiting_for_input = True
        while waiting_for_input:
            print("Please choose: ")
            print('1: Add a new transaction value')
            print('2: Mine a new block')
            print('3: Output the blockchain blocks')
            # print('4: Output participants')
            print('5: Check transaction validity')
            print('6: Create wallet ')
            print('7: Load wallet ')
            # print('h: Manipulate the chain')
            print('q: Quit')
            user_choice = self.get_user_choice()
            if user_choice == '1':
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount = amount):
                    print('Added Transaction')
                else:
                    print('Transaction failed')
                print(self.blockchain.open_transactions)

            elif user_choice == '2':
                self.blockchain.mine_block()
                    # open_transactions = []
                    # save_data()
            elif user_choice == '3':
                self.print_blockchain_elements()
            # elif user_choice == '4':
            #     print(participants)
            elif user_choice == '5':
                if Verification.verify_transactions(self.blockchain.open_transactions, self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid Transactions')
            # elif user_choice == "h":
            #     if len(blockchain) >= 1:
            #         blockchain[0] ={
            #             'previous hash':'',
            #             'index': 0,
            #             'transactions': [{'sender':'abel','recipient':'Lucy','amount':500.00}]
            #                 }
            elif user_choice == '6':
                # self.wallet = Wallet()
                self.wallet.create_keys()
            elif user_choice == '7':
                pass
            elif user_choice == 'q':
                waiting_for_input = False
            else:
                print('Input was invalid, please pick a value from the list!')
            if not Verification.verify_chain(self.blockchain.chain):
                self.print_blockchain_elements()
                print("invalid blockchain")
                break
            print('Balance of {}:{:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))
        else:
            print('User left!')
        print("Done")


if __name__ == '__main__':
    node = Node()
    node.listen_for_input()

# print(__name__)