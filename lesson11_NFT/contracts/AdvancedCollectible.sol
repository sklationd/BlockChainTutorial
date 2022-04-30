// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    uint256 public randomness;
    bytes32 internal keyHash;
    uint256 public fee;
    uint256 public randomResult;

    event RequestedCollectible(bytes32 indexed requestId, address requester);
    event BreedAssigned(uint256 indexed tokenId, Breed breed);

    enum Breed{PUG, SHIBA_INU, ST_BERNARD}

    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) requestIdToSender;

    constructor(address _vrfCoordinator, address _link, uint256 _fee, bytes32 _keyHash ) public 
        VRFConsumerBase(_vrfCoordinator, _link)
        ERC721("AdvancedCollectible", "ACO")
    {
        keyHash = _keyHash;
        fee = _fee;
        tokenCounter = 0;
    }

    function createCollectible() public {
        bytes32 requestId = getRandomNumber();
        requestIdToSender[requestId] = msg.sender;
        emit RequestedCollectible(requestId, msg.sender);
    }

    function getRandomNumber() internal returns (bytes32 requestId) {
        require(LINK.balanceOf(address(this)) >= fee, "Not enough LINK - fill contract with faucet");
        return requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit BreedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    function getBreed(uint256 tokenId) public view returns (Breed) {
        require(_exists(tokenId));
        return tokenIdToBreed[tokenId];
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "caller is not owner nor approved");
        _setTokenURI(tokenId, _tokenURI);
    }
}