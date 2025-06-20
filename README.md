* A Pygame-based Snake game
* NFT minting
* Score recording on the Ethereum Sepolia testnet
* On-chain leaderboard display via a PyQt5 UI

---

````markdown
# 🐍 SnakeChain — A Web3-Powered Snake Game

**SnakeChain** is an interactive, on-chain Snake game that merges classic arcade gameplay with blockchain technology. It allows players to:
- Play a fully-featured Snake game built with **Pygame**
- **Mint game screenshots as NFTs** to IPFS via **Pinata**
- **Record scores on-chain** using a custom **Solidity smart contract** deployed on **Ethereum Sepolia**
- **View global, personal, and all-time leaderboards** using a **PyQt5 UI**

> This project demonstrates how blockchain and gaming can merge to create immutable, player-centric experiences.

---

## 🎮 Features

### 🕹 Gameplay
- Smooth Pygame-based snake logic with emoji-powered **superfoods** (`🕷️`, `🐀`, `🐰`, etc.)
- **Pause/Resume**, food evolution, superfood spawning, and length-based scoring
- Game Over screen with options:
  - `R`: Restart game
  - `Q`: Quit
  - `V`: View scores

### 🧠 Scoreboard System
- Scores are stored **on-chain** using a `ScoreBoard` smart contract
- Leaderboard UI built with **PyQt5**
  - Global top scores (highest in a single session)
  - All-time total scores per player
  - Personal history only visible to the player

### 🖼 NFT Minting
- Game screenshots are saved on **IPFS (Pinata)**
- Metadata includes:
  - Player name
  - Score and snake length
  - Game snapshot
- NFT minted via `SnakeNFT.sol` using **Web3.py**

---

## 🔗 Smart Contracts

### `SnakeNFT.sol`
- ERC-721 NFT smart contract using OpenZeppelin
- Only the **game owner** can mint NFTs

### `ScoreBoard.sol`
- Stores:
  ```solidity
  struct Score {
      string name;
      address player;
      uint256 score;
  }
````

* Events emitted and scores recorded on-chain

✅ Both contracts are deployed on **Ethereum Sepolia** and verified on **Etherscan**.

---

## 🧱 Tech Stack

| Layer        | Tech                   |
| ------------ | ---------------------- |
| Game Engine  | Pygame (Python)        |
| UI           | PyQt5                  |
| Blockchain   | Solidity (Hardhat)     |
| Web3 Layer   | Web3.py, Infura        |
| Storage      | IPFS via Pinata        |
| NFT Standard | ERC-721 (OpenZeppelin) |

---

## 🚀 Getting Started

### 1. Clone the Project

```bash
git clone https://github.com/yourusername/snakechain.git
cd snakechain
```

### 2. Install Requirements

```bash
pip install -r requirements.txt
```

### 3. Setup `.env`

Create a `.env` file with your credentials:

```
PINATA_API_KEY=...
PINATA_SECRET_API_KEY=...
PRIVATE_KEY=...           # Wallet's private key (DO NOT SHARE)
PUBLIC_ADDRESS=0x...      # Wallet's public address
INFURA_URL=https://sepolia.infura.io/v3/YOUR-PROJECT-ID
CONTRACT_ADDRESS=0x...    # NFT Contract
SCOREBOARD_ADDRESS=0x...  # Scoreboard Contract
```

### 4. Run the Game

```bash
python main.py
```

---

## 📦 Directory Structure

```
BlockchainGame/
├── blockchain/
│   ├── nft_service.py
│   ├── score_chain.py
│   └── abi/
├── contracts/
│   ├── SnakeNFT.sol
│   └── ScoreBoard.sol
├── game/
│   ├── snake.py
│   ├── scoreboard.py
│   └── scoreboard_ui.py
├── screenshots/
├── scripts/
│   └── deploy.js
├── main.py
├── .env.example
└── README.md
```

---

## 🧪 Tests

```bash
npx hardhat test
```

Includes unit tests for:

* NFT deployment and minting
* Scoreboard contract logic
* Permission validation

---

## 🌐 Deployment

* Smart contracts are deployed via Hardhat.
* You can deploy your own versions by configuring `hardhat.config.js`.

---

## 📸 Example

After a game ends:

* Game Over screen appears
* Screenshot is saved
* NFT is minted to the player
* Score is recorded on-chain
* Leaderboard UI allows viewing global & personal scores

---

## 🛡 Security Notes

* `.env` is in `.gitignore` and must never be committed.
* Ensure your **private key is never shared** or pushed to GitHub.

---

## 📜 License

MIT License © 2025 \[Wilfred K.N]

---

## 🙌 Acknowledgements

* [Pygame](https://www.pygame.org/)
* [Infura](https://infura.io/)
* [Pinata](https://pinata.cloud/)
* [OpenZeppelin](https://openzeppelin.com/)
* [Web3.py](https://web3py.readthedocs.io/)

---
