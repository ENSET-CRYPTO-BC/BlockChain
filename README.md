# Blockchain Implementation in Python

## Video Demonstration
https://github.com/user-attachments/assets/ea167cdd-a792-4dd8-83b9-7ad6122a7f74


A simple blockchain implementation in Python that demonstrates core blockchain concepts including:
- Block creation and mining
- Transaction management
- Cryptographic security
- Chain validation

## Project Structure
```
ReposiortyFolder/
├──Report/
│    ├── Main.pdf/ # The main report pdf of the project
└── Code/
    ├── main.py # main code to run the application
    ├── Models/
    │   ├── blockchain.py      # Main blockchain implementation
    │   ├── block.py          # Block structure
    │   ├── transaction.py    # Transaction handling
    │   └── transaction_pool.py # Transaction pool management
    └── Utils/
        ├── crypto_utils.py   # Cryptographic functions
        └── utils.py          # General utilities
```

## Features
- Proof of Work mining system
- ECDSA digital signatures
- SHA-512 hashing
- Transaction validation
- Chain integrity verification

## Documentation
For detailed documentation and implementation details, see the [Full Report](../Report/Main.pdf).

## Requirements
- Python 3.8+
- ecdsa
- hashlib
