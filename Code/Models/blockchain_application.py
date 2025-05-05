from typing import Dict, Tuple
from Models.blockchain import BlockChain
from Models.transaction import Transaction
from Models.transaction_pool import TransactionPool
from Utils.crypto_utils import generate_keys_pairs


class BlockChainApplication:
    def __init__(self):
        self.blockchain = BlockChain()
        self.transaction_pool = TransactionPool()
        self.wallets: Dict[str, Tuple[str, str]] = {}

        if not self.wallets:
            self._create_wallet("system")

    def _create_wallet(self, name: str) -> Tuple[str, str]:
        private_key_str, public_key_str = generate_keys_pairs()
        self.wallets[name] = (private_key_str, public_key_str)
        return private_key_str, public_key_str

    def _get_wallet_by_name(self, name: str) -> Tuple[str, str]:
        if name not in self.wallets:
            return self._create_wallet(name)
        return self.wallets[name]

    def create_transaction(
        self, sender_name: str, recipient_name: str, amount: float
    ) -> Transaction:
        sender_private_key_str, sender_public_key_str = self._get_wallet_by_name(
            sender_name
        )

        _, recipient_public_key_str = self._get_wallet_by_name(recipient_name)

        transaction = Transaction(
            sender=sender_public_key_str,
            recipient=recipient_public_key_str,
            amount=amount,
            private_key=sender_private_key_str,
        )

        self.transaction_pool.add_transaction(transaction)
        return transaction

    def mine_block(self, reward: float = 10) -> bool:
        pending_transactions = self.transaction_pool.get_pending_transactions(limit=2)

        if not pending_transactions:
            return False

        _, miner_public_key = self._get_wallet_by_name("system")
        coinbase_transaction = Transaction(
            sender="network", recipient=miner_public_key, amount=reward
        )

        pending_transactions.insert(0, coinbase_transaction)

        self.blockchain.add_block(pending_transactions)

        self.transaction_pool.remove_transactions(pending_transactions)

        return True

    def display_blockchain(self) -> None:
        """Display the current state of the blockchain."""
        print("\n===== BLOCKCHAIN =====")
        for block in self.blockchain.chain:
            print(f"Block #{block.index} - Hash: {block.hash[:10]}...")
            print(f"  Previous Hash: {block.previous_hash[:10]}...")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Transactions: {len(block.transactions)}")

            for i, transaction in enumerate(block.transactions):
                print(f"    {i+1}. {transaction}")
            print()

    def display_pending_transactions(self) -> None:
        """Display the pending transactions in the pool."""
        pending = self.transaction_pool.get_pending_transactions()

        print("\n===== PENDING TRANSACTIONS =====")
        if not pending:
            print("No pending transactions.")
        else:
            for i, transaction in enumerate(pending):
                print(f"{i+1}. {transaction}")
        print()

    def validate_blockchain(self) -> None:
        """Validate the blockchain and display the result."""
        is_valid = self.blockchain.is_valid_chain()
        print("\n===== BLOCKCHAIN VALIDATION =====")
        if is_valid:
            print("Blockchain is valid and consistent!")
        else:
            print("Blockchain validation FAILED!")
        print()

    def display_wallets(self) -> None:
        """Display the available wallets."""
        print("\n===== WALLETS =====")
        for name, (_, public_key) in self.wallets.items():
            print(f"{name}: {public_key[:10]}...")
        print()

    def run(self) -> None:
        """Run the blockchain application."""
        while True:
            print("\n===== BLOCKCHAIN MENU =====")
            print("1. Display Blockchain")
            print("2. Create Transaction")
            print("3. Display Pending Transactions")
            print("4. Mine Block")
            print("5. Validate Blockchain")
            print("6. Display Wallets")
            print("7. Exit")

            choice = input("\nEnter your choice (1-7): ")

            if choice == "1":
                self.display_blockchain()
            elif choice == "2":
                sender = input("Enter sender name: ")
                recipient = input("Enter recipient name: ")

                try:
                    amount = float(input("Enter amount: "))
                    Transaction = self.create_transaction(sender, recipient, amount)
                    print(f"Transaction created: {Transaction}")
                except ValueError as e:
                    print(f"Error: {e}")
            elif choice == "3":
                self.display_pending_transactions()
            elif choice == "4":
                if self.mine_block():
                    print("Block mined successfully!")
                else:
                    print("No transactions to mine.")
            elif choice == "5":
                self.validate_blockchain()
            elif choice == "6":
                self.display_wallets()
            elif choice == "7":
                print("Exiting... Goodbye")
                print("Thank you for using BlockChain Application")
                break
            else:
                print("Invalid choice. Please try again.")
