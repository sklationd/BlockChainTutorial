// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    address[] public allowedTokens;
    
    // token -> user -> amount 
    mapping(address => mapping(address => uint256)) public stakingBalance;
    // user -> token count
    mapping(address => uint256) public uniqueTokensStaked;
    // token -> priceFeed address
    mapping(address => address) public tokenToPriceFeed;
    address[] public stakers;

    IERC20 public dappToken;

    constructor(address _dappTokenAddress) {
        dappToken = IERC20(_dappTokenAddress);
    }

    function setTokenPriceFeed(address _token, address _priceFeed) public onlyOwner {
        tokenToPriceFeed[_token] = _priceFeed;
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0");
        require(isAllowedToken(_token), "This token is not allowed!");
        
        // TRANSFER
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        // Update stakers
        if(uniqueTokensStaked[msg.sender] == 0) {
            stakers.push(msg.sender);
        }
        
        // Update uniqueTokensStaked
        updateUniqueTokenStaked(msg.sender, _token);

        // Update stakingBalance
        stakingBalance[_token][msg.sender] += _amount;
    }

    function unstakeTokens(address _token) public {
        uint256 stakedTokenAmount = stakingBalance[_token][msg.sender];
        require( stakedTokenAmount > 0, "Staking balance cannot be 0");
        IERC20(_token).transfer(msg.sender, stakedTokenAmount);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender]--;

        if (uniqueTokensStaked[msg.sender] == 0) {
            for (
                uint256 stakersIndex = 0;
                stakersIndex < stakers.length;
                stakersIndex++
            ) {
                if (stakers[stakersIndex] == msg.sender) {
                    stakers[stakersIndex] = stakers[stakers.length - 1];
                    stakers.pop();
                }
            }
        }
    }

    function issueTokens() public onlyOwner {
        for(uint256 index=0; index<stakers.length; index++) {
            address recipient = stakers[index];
            uint256 totalValue = getUserTotalValue(recipient);
            dappToken.transfer(recipient, totalValue);
            // transfer a token reward to recipient based on
            // their total deposited value
        
        }
    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;
        require(uniqueTokensStaked[_user] > 0, "User doesn't have any staked token!");
        for(uint256 index = 0; index < allowedTokens.length; index++ ) {
            totalValue += getUserSingleTokenValue(_user, allowedTokens[index]);
        }
        return totalValue;
    }

    function getUserSingleTokenValue(address _user, address _token) public view returns (uint256) {
        if(uniqueTokensStaked[_user] <= 0) {
            return 0;
        }
        (uint256 price, uint256 decimals) = getTokenValue(_token);
        return (stakingBalance[_token][_user] * price / (10**decimals));
    }

    function getTokenValue(address _token) public view returns (uint256, uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(tokenToPriceFeed[_token]);
        (,int256 price,,,) = priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());
        return (uint256(price), decimals);
    }

    function updateUniqueTokenStaked(address _user, address _token) internal {
        if(stakingBalance[_token][_user] <= 0 ) {
            uniqueTokensStaked[_user]++;
        }
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function isAllowedToken(address _token) public view returns (bool) {
        for( uint256 index = 0; index < allowedTokens.length; index++ ) {
            if( allowedTokens[index] == _token ) {
                return true;
            }
        }
        return false;
    }
}

