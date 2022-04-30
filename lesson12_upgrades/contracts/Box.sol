// SPDX-License-Identifer: MIT
pragma solidity ^0.8.0;

contract Box {
    uint256 private value;

    event ValueChanged(uint256 newValue);

    function store(uint256 _value) public {
        value = _value;
        emit ValueChanged(value); 
    }

    function retrieve() public view returns (uint256) {
        return value;
    }
}