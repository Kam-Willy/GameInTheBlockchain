// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ScoreBoard {
    struct Score {
        string name;
        address player;
        uint256 score;
    }

    Score[] public scores;

    address public owner;

    event ScoreRecorded(string name, address indexed player, uint256 score);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only backend can push scores");
        _;
    }

    function recordScore(string calldata name, address player, uint256 score) external onlyOwner {
        scores.push(Score(name, player, score));
        emit ScoreRecorded(name, player, score);
    }

    function getAllScores() external view returns (Score[] memory) {
        return scores;
    }

    function getScoreCount() external view returns (uint256) {
        return scores.length;
    }
}
