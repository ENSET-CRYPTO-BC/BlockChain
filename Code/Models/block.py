import logging
from turtledemo.sorting_animate import Block
from typing import List, Optional, Dict
from Models.transaction import Transaction
from Utils.crypto_utils import generate_hash, get_timestamp

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class Block:
    def __init__(
        self,
        index: int,
        previous_hash: str,
        transactions: List[Transaction],
        timestamp: Optional[int] = None,
        nonce: int = 0,
    ) -> None:
        """Initialize a new block.

        Args:
            index: Position of the block in the chain
            previous_hash: Hash of the previous block
            transactions: List of transactions to include in this block
            timestamp: Optional timestamp (will be generated if not provided)
            nonce: Value used for mining (proof-of-work)
        """
        logging.info("Initializing a new block with index %d", index)
        self.index = index
        self.timestamp = timestamp if timestamp else get_timestamp()
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.nonce = nonce
        self.hash = self._calculate_hash()
        logging.info("Block initialized with hash: %s", self.hash)

    def _calculate_hash(self) -> str:
        """Calculate the hash of the block header.

        Returns:
            str: The hash of the block header.
        """
        logging.debug("Calculating hash for block with index %d", self.index)
        block_header = {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "transactions": [tx.transaction_hash for tx in self.transactions],
            "nonce": self.nonce,
        }

        return generate_hash(block_header)

    def mine_block(self, difficulty: int) -> None:
        """Perform proof-of-work to mine the block.

        Args:
            difficulty: The number of leading zeros required in the hash.
        """
        logging.info("Mining block with index %d", self.index)
        target = "0" * difficulty

        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self._calculate_hash()

        logging.info("Block mined successfully with hash: %s", self.hash)

    def has_valid_transactions(self) -> bool:
        """Check if all transactions in the block are valid.

        Returns:
            bool: True if all transactions are valid, False otherwise.
        """
        logging.info("Validating transactions for block with index %d", self.index)
        return all(transaction.is_valid() for transaction in self.transactions)

    def to_dict(self) -> dict:
        """Convert the block to a dictionary representation.

        Returns:
            dict: A dictionary representation of the block.
        """
        logging.debug("Converting block with index %d to dictionary", self.index)
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce,
            "transactions": [
                transaction.to_dict() for transaction in self.transactions
            ],
        }

    def __str__(self) -> str:
        """Generate a string representation of the block.

        Returns:
            str: A string summarizing the block.
        """
        logging.debug(
            "Generating string representation for block with index %d", self.index
        )
        return f"Block #{self.index} [Hash: {self.hash[:10]}..., Number of Transactions: {len(self.transactions)}]"

    @classmethod
    def from_dict(cls, data: Dict) -> "Block":
        """Create a Block instance from a dictionary.

        Args:
            data: Dictionary with block data

        Returns:
            Block: A new Block instance
        """
        logging.info("Creating block from dictionary")
        transactions = [
            Transaction.from_dict(tx_data) for tx_data in data["transactions"]
        ]

        block = cls(
            index=data["index"],
            previous_hash=data["previous_hash"],
            transactions=transactions,
            timestamp=data["timestamp"],
            nonce=data["nonce"],
        )
        block.hash = data["hash"]
        logging.info("Block created from dictionary with index %d", block.index)
        return block
