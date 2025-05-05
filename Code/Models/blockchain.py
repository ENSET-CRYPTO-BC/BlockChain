from typing import Dict, List
from Models.block import Block
from Models.transaction import Transaction
from Utils.crypto_constants import CryptoConstants
from Utils.crypto_utils import get_timestamp


class BlockChain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = []
        self.difficulty = difficulty

        self._create_genesis_block()

    def _create_genesis_block(self):
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

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, transactions: List[Transaction]) -> Block:
        previous_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain) + 1,
            previous_hash=previous_block.hash,
            transactions=transactions,
        )

        new_block.mine_block(self.difficulty)

        self.chain.append(new_block)

        return new_block

    def is_valid_chain(self) -> bool:

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                return False

            if current_block.hash != current_block._calculate_hash():
                return False

            if not current_block.has_valid_transactions():
                return False

        return True

    def adjust_difficulty(self, difficulty: int) -> None:
        self.difficulty = difficulty

    def to_dict(self) -> Dict:
        return {
            "difficulty": self.difficulty,
            "chain": [block.to_dict() for block in self.chain],
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "BlockChain":
        """Create a Blockchain instance from a dictionary.

        Args:
            data: Dictionary with blockchain data

        Returns:
            Blockchain: A new Blockchain instance
        """
        blockchain = cls(difficulty=data["difficulty"])
        # Clear the default genesis block
        blockchain.chain = []

        # Add all blocks from the data
        for block_data in data["chain"]:
            blockchain.chain.append(Block.from_dict(block_data))

        return blockchain
