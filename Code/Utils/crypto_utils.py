import hashlib
from typing import Any, Tuple
import logging
from Utils.utils import *
import time

# Elliptic Curve Digital Signature Algorithm
import ecdsa
import base64


# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set log level to INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def generate_hash(data: Any) -> str:
    """Compute the hash (SHA-512) of data

    Args:
        data (Any): Data to be hashed. will be converted to bytes if another type than string

    Returns:
        str: The hash of the data entry in hexadecimal
    """
    logging.info("Computing hash for data of type: %s", type(data).__name__)

    if not isinstance(data, str):
        data = dump_data(data)
        logging.debug("Data converted to JSON string: %s", data)

    encoded_data = data.encode()
    hash_result = hashlib.sha512(encoded_data).hexdigest()
    logging.info("Hash computation complete.")
    return hash_result


def generate_keys_pairs() -> Tuple[str, str]:
    """Generate public and private key pairs

    Returns:
        Tuple: (private_key_str, public_key_str) each one encoded in base64 (for readability)
    """
    logging.info("Generating ECDSA key pairs.")

    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key: ecdsa.VerifyingKey = private_key.get_verifying_key()

    private_key_str = base64.b64encode(private_key.to_string()).decode()
    public_key_str = base64.b64encode(public_key.to_string()).decode()

    logging.info("Key pair generation complete.")
    logging.debug("Private Key: %s", private_key_str)
    logging.debug("Public Key: %s", public_key_str)

    return (private_key_str, public_key_str)


def generate_signature(data: Any, private_key_str: str) -> str:
    """generate the signature of the data using a private key

    Args:
        data (Any): Data to be signed
        private_key_str (str): Previously generated private_key (in Base64)

    Returns:
        str: Base64 encoded signature
    """

    if not isinstance(data, str):
        data = dump_data(data)
        logging.debug("Data converted to JSON string: %s", data)

    private_key_str = base64.b64decode(private_key_str)
    private_key = ecdsa.SigningKey.from_string(private_key_str, curve=ecdsa.SECP256k1)

    signature = private_key.sign(data.encode())

    return base64.b64encode(signature).decode()


def verify_signature(data: Any, signature_str: str, public_key_str: str) -> bool:
    """Verify the signature of the given data using the provided public key.

    Args:
        data (Any): The data whose signature needs to be verified.
        signature_str (str): The Base64-encoded signature of the data.
        public_key_str (str): The Base64-encoded public key used for verification.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
    logging.info("Starting signature verification.")
    try:
        if not isinstance(data, str):
            logging.debug("Data is not a string. Converting to JSON string.")
            data = dump_data(data)

        logging.debug("Decoding public key from Base64.")
        public_key_str = base64.b64decode(public_key_str)
        public_key = ecdsa.VerifyingKey.from_string(
            public_key_str, curve=ecdsa.SECP256k1
        )

        logging.debug("Decoding signature from Base64.")
        signature = base64.b64decode(signature_str)

        logging.info("Verifying the signature.")
        result = public_key.verify(signature, data.encode())
        logging.info("Signature verification successful.")
        return result
    except Exception as e:
        logging.error("Signature verification failed: %s", str(e))
        return False


def get_timestamp() -> int:
    """Get the current timestamp in seconds since the epoch.

    Returns:
        int: The current timestamp as an integer.
    """
    logging.info("Fetching the current timestamp.")
    timestamp = int(time.time())
    logging.debug("Current timestamp: %d", timestamp)
    return timestamp
