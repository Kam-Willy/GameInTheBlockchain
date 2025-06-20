const hre = require("hardhat");

async function main() {
  const ScoreBoard = await hre.ethers.getContractFactory("ScoreBoard");
  const scoreboard = await ScoreBoard.deploy();
  const address = await scoreboard.getAddress();

  console.log("✅ ScoreBoard deployed at:", address);
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
