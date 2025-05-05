import logging
from typing import Dict, List, Set
from Models.transaction import Transaction

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class TransactionPool:
    def __init__(self):
        """Initialize the transaction pool."""
        logging.info("Initializing transaction pool.")
        self.pending_transactions: List[Transaction] = []
        self.transaction_hashes: Set[str] = set()

    def add_transaction(self, transaction: Transaction) -> bool:
        """Add a transaction to the pool if it is valid and not a duplicate.

        Args:
            transaction: The transaction to add.

        Returns:
            bool: True if the transaction was added, False otherwise.
        """
        logging.info("Adding transaction with hash: %s", transaction.transaction_hash)
        if not transaction.is_valid():
            logging.warning("Transaction is invalid.")
            return False

        if transaction.transaction_hash in self.transaction_hashes:
            logging.warning("Transaction is a duplicate.")
            return False

        self.pending_transactions.append(transaction)
        self.transaction_hashes.add(transaction.transaction_hash)
        logging.info("Transaction added successfully.")
        return True

    def get_pending_transactions(self, limit: int = None) -> List[Transaction]:
        """Retrieve pending transactions from the pool.

        Args:
            limit: Optional limit on the number of transactions to retrieve.

        Returns:
            List[Transaction]: A list of pending transactions.
        """
        logging.info("Fetching pending transactions with limit: %s", limit)
        if limit is None or limit >= len(self.pending_transactions):
            return self.pending_transactions.copy()

        return self.pending_transactions[:limit]

    def remove_transactions(self, transactions: List[Transaction]) -> None:
        """Remove a list of transactions from the pool.

        Args:
            transactions: The transactions to remove.
        """
        logging.info("Removing transactions from the pool.")
        transactions_hashes_to_remove = {
            transaction.transaction_hash for transaction in transactions
        }

        self.pending_transactions = [
            transaction
            for transaction in self.pending_transactions
            if transaction.transaction_hash not in transactions_hashes_to_remove
        ]

        self.transaction_hashes -= transactions_hashes_to_remove
        logging.info("Transactions removed successfully.")

    def clear(self) -> None:
        """Clear all transactions from the pool."""
        logging.info("Clearing all transactions from the pool.")
        self.pending_transactions = []
        self.transaction_hashes = set()
        logging.info("Transaction pool cleared.")

    def size(self) -> int:
        """Get the number of transactions in the pool.

        Returns:
            int: Number of pending transactions.
        """
        logging.debug("Getting the size of the transaction pool.")
        return len(self.pending_transactions)

    def to_dict(self) -> Dict:
        """Convert the transaction pool to a dictionary.

        Returns:
            Dict: Dictionary representation of the transaction pool.
        """
        logging.debug("Converting transaction pool to dictionary.")
        return {
            "pending_transactions": [
                transaction.to_dict() for transaction in self.pending_transactions
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "TransactionPool":
        """Create a TransactionPool instance from a dictionary.

        Args:
            data: Dictionary with transaction pool data.

        Returns:
            TransactionPool: A new TransactionPool instance.
        """
        logging.info("Creating transaction pool from dictionary.")
        pool = cls()

        # Add all transactions from the data
        for tx_data in data["pending_transactions"]:
            tx = Transaction.from_dict(tx_data)
            pool.add_transaction(tx)

        logging.info(
            "Transaction pool created from dictionary with %d transactions.",
            len(pool.pending_transactions),
        )
        return pool
