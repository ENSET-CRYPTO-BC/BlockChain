from Utils.crypto_utils import *
from typing import Dict, Optional
import logging


class Transaction:
    def __init__(
        self,
        sender: str,
        recipient: str,
        amount: str,
        private_key: Optional[str] = None,
        timestamp: Optional[int] = None,
    ) -> None:
        """Create a new transaction

        Args:
            sender: Public key (address) of the sender
            recipient: Public key (address) of the recipient
            amount: Amount to transfer
            private_key: Optional private key to sign the transaction immediately
            timestamp: Optional timestamp (will be generated if not provided)

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
        """

        if not sender:
            raise ValueError("Sender address cannot be empty")
        if not recipient:
            raise ValueError("Recipient address cannot be empty")
        if amount <= 0:
            raise ValueError("Amount must be positive")

        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp if timestamp else get_timestamp()
        self.signature = None

        self.transaction_hash = self._calculate_transaction_hash()

        if private_key:
            self.sign(private_key)

    def _calculate_transaction_hash(self) -> str:

        transaction_data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
        }
        return generate_hash(transaction_data)

    def sign(self, private_key_str: str) -> None:
        if self.signature:
            raise ValueError("Transaction is already signed")

        self.signature = generate_signature(
            data=self.transaction_hash, private_key_str=private_key_str
        )

    def is_valid(self) -> bool:
        if self.sender == "network":
            return True

        return verify_signature(self.transaction_hash, self.signature, self.sender)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the transaction object to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the transaction object.
        """
        logging.info("Converting transaction to dictionary.")
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "hash": self.transaction_hash,
            "signature": self.signature,
        }

    def __str__(self) -> str:
        """Generate a string representation of the transaction.

        Returns:
            str: A string summarizing the transaction.
        """
        logging.info("Generating string representation of the transaction.")
        return f"Transaction({self.sender[:10]}... -> {self.recipient[:10]}..., {self.amount})"

    @classmethod
    def from_dict(cls, data: Dict) -> "Transaction":
        """Create a Transaction object from a dictionary.

        Args:
            data (Dict): A dictionary containing transaction details.

        Returns:
            Transaction: A Transaction object created from the dictionary.
        """
        logging.info("Creating transaction from dictionary.")
        transaction = cls(
            sender=data["sender"],
            recipient=data["recipient"],
            amount=data["amount"],
            timestamp=data["timestamp"],
        )

        transaction.transaction_hash = data["hash"]
        transaction.signature = data.get("signature")
        logging.info("Transaction created successfully from dictionary.")
        return transaction
