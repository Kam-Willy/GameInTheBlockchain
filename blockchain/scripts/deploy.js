const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();
  console.log("Using address:", deployer.address);
  console.log("Balance:", hre.ethers.formatEther(await deployer.provider.getBalance(deployer.address)), "ETH");

  const SnakeNFT = await hre.ethers.getContractFactory("SnakeNFT");
  const contract = await SnakeNFT.deploy(); // Deployed in Ethers v6
  const address = await contract.getAddress();

  console.log("✅ SnakeNFT deployed to:", address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
