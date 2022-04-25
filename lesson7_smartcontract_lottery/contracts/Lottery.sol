// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable public recentWinner;
    uint256 public randomness;
    address payable[] public players;
    AggregatorV3Interface internal priceFeed;
    uint256 public usdEntryFee;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    event RequestedRandomness(bytes32 requestID);
 
    LOTTERY_STATE public lotteryState;
    
    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public randomResult;

    constructor(
        uint256 _usdEntryFee,
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
        ) 
    public VRFConsumerBase(
        _vrfCoordinator, 
        _link
        ) 
    {
        keyHash = _keyHash;
        fee = _fee;

        usdEntryFee = _usdEntryFee * (10**18);
        priceFeed = AggregatorV3Interface(_priceFeedAddress);
        lotteryState = LOTTERY_STATE.CLOSED;
    }

    /** 
     * Requests randomness 
     */
    function getRandomNumber() public returns (bytes32 requestId) {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");
        return requestRandomness(keyHash, fee);
    }

    /**
     * Callback function used by VRF Coordinator
     */
    function fulfillRandomness(bytes32 requestId, uint256 _randomness) internal override {
        require(lotteryState == LOTTERY_STATE.CALCULATING_WINNER, "you aren't there yet");
        uint256 winnerIndex = randomness % players.length;
        recentWinner = players[winnerIndex];
        recentWinner.transfer(address(this).balance);

        // Reset
        players = new address payable[](0);
        lotteryState = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }

    function enter() public payable {
        require(lotteryState == LOTTERY_STATE.OPEN);
        // check msg.value whether it is bigger than entrance fee or not
        require(msg.value >= getEntranceFee(), "Not enough ETH to enter!");
        players.push(msg.sender);
    }

    // 진입하기 위해서 필요한 Wei
    function getEntranceFee() public view returns (uint256) {
        // 1 이더리움이 몇 달러인지에 대한 정보, 그런데 소수점 보정을 위해 결과 값에 10의 8승이 곱해져있음
        (, int256 price, , , ) = priceFeed.latestRoundData(); // has 8 decimal
        uint256 adjustedPrice = uint256(price) * (10**10);
        return ( usdEntryFee * (10**18) ) / adjustedPrice;
    }

    function startLottery() public onlyOwner {
        require(lotteryState == LOTTERY_STATE.CLOSED, "Can't start a new lottery yet!");
        lotteryState = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        require(lotteryState==LOTTERY_STATE.OPEN, "Lottery is not opened yet!");
        lotteryState = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestID = getRandomNumber();
        emit RequestedRandomness(requestID);
    }

}

