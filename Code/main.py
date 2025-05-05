from typing import Dict, Tuple
from Models.blockchain import BlockChain
from Models.transaction import Transaction
from Models.transaction_pool import TransactionPool
from Utils.crypto_utils import generate_keys_pairs


class MainApplication:
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
