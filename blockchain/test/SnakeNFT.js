const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("SnakeNFT", function () {
  let SnakeNFT, contract, owner, addr1;

  beforeEach(async () => {
  [owner, addr1] = await ethers.getSigners();
  SnakeNFT = await ethers.getContractFactory("SnakeNFT");
  contract = await SnakeNFT.deploy(); // ✅ That's it in Ethers v6
  });

  it("should deploy and set initial tokenCounter to 0", async () => {
    expect(await contract.tokenCounter()).to.equal(0);
  });

  it("should mint an NFT with a valid URI", async () => {
    const tokenURI = "ipfs://example_uri_123";
    const tx = await contract.mintNFT(addr1.address, tokenURI);
    const receipt = await tx.wait();

    // Check ownership
    expect(await contract.ownerOf(0)).to.equal(addr1.address);

    // Check URI
    expect(await contract.tokenURI(0)).to.equal(tokenURI);

    // Check token counter
    expect(await contract.tokenCounter()).to.equal(1);
  });

  it("should increment tokenCounter for each NFT", async () => {
    await contract.mintNFT(addr1.address, "ipfs://uri1");
    await contract.mintNFT(addr1.address, "ipfs://uri2");
    expect(await contract.tokenCounter()).to.equal(2);

  it("should not allow non-owner to mint", async () => {
    const tokenURI = "ipfs://unauthorized";
    await expect(
    contract.connect(addr1).mintNFT(addr1.address, tokenURI)
  ).to.be.revertedWithCustomError(contract, "OwnableUnauthorizedAccount")
    .withArgs(addr1.address);
  });
});
