import logging
from typing import Dict, List
from Models.block import Block
from Models.transaction import Transaction
from Utils.crypto_constants import CryptoConstants
from Utils.crypto_utils import get_timestamp

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class BlockChain:
    def __init__(self, difficulty: int = 2):
        """Initialize the blockchain with a genesis block.

        Args:
            difficulty: The mining difficulty level (default is 2).
        """
        logging.info("Initializing blockchain with difficulty %d", difficulty)
        self.chain: List[Block] = []
        self.difficulty = difficulty

        self._create_genesis_block()

    def _create_genesis_block(self):
        """Create the genesis block and add it to the chain."""
        logging.info("Creating genesis block.")
        genesis_transaction = Transaction(
            sender="network",
            recipient="genesis-address",
            amount=50,
            timestamp=get_timestamp(),
        )

        genesis_block = Block(
            index=0,
            previous_hash="0" * CryptoConstants.HASH_LEN,
            transactions=[genesis_transaction],
            timestamp=get_timestamp(),
        )

        self.chain.append(genesis_block)
        logging.info("Genesis block created with hash: %s", genesis_block.hash)

    def get_latest_block(self) -> Block:
        """Get the latest block in the blockchain.

        Returns:
            Block: The latest block in the chain.
        """
        logging.debug("Fetching the latest block in the chain.")
        return self.chain[-1]

    def add_block(self, transactions: List[Transaction]) -> Block:
        """Add a new block to the blockchain.

        Args:
            transactions: List of transactions to include in the new block.

        Returns:
            Block: The newly added block.
        """
        logging.info("Adding a new block to the blockchain.")
        previous_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_block.hash,
            transactions=transactions,
        )

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)
        logging.info(
            "New block added with index %d and hash: %s",
            new_block.index,
            new_block.hash,
        )

        return new_block

    def is_valid_chain(self) -> bool:
        """Validate the integrity of the blockchain.

        Returns:
            bool: True if the blockchain is valid, False otherwise.
        """
        logging.info("Validating the blockchain.")
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                logging.error(
                    "Invalid blockchain: Previous hash mismatch at block %d", i
                )
                return False

            if current_block.hash != current_block._calculate_hash():
                logging.error("Invalid blockchain: Hash mismatch at block %d", i)
                return False

            if not current_block.has_valid_transactions():
                logging.error("Invalid blockchain: Invalid transactions at block %d", i)
                return False

        logging.info("Blockchain is valid.")
        return True

    def adjust_difficulty(self, difficulty: int) -> None:
        """Adjust the mining difficulty of the blockchain.

        Args:
            difficulty: The new difficulty level.
        """
        logging.info("Adjusting blockchain difficulty to %d", difficulty)
        self.difficulty = difficulty

    def to_dict(self) -> Dict:
        """Convert the blockchain to a dictionary representation.

        Returns:
            Dict: A dictionary representation of the blockchain.
        """
        logging.debug("Converting blockchain to dictionary.")
        return {
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BlockChain":
        """Create a Blockchain instance from a dictionary.

        Args:
            data: Dictionary with blockchain data.

        Returns:
            BlockChain: A new Blockchain instance.
        """
        logging.info("Creating blockchain from dictionary.")
        blockchain = cls(difficulty=data["difficulty"])
        # Clear the default genesis block
        blockchain.chain = []

        # Add all blocks from the data
        for block_data in data["chain"]:
            blockchain.chain.append(Block.from_dict(block_data))

        logging.info(
            "Blockchain created from dictionary with %d blocks.", len(blockchain.chain)
        )
        return blockchain
