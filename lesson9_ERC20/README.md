# ERC-20

토큰이라고 하는것은 결국 [ERC-20(Token Standard)](https://eips.ethereum.org/EIPS/eip-20) 규격을 만족하는 Smart Contract이다. 문서에 명시되어있는 인터페이스를 직접 다 구현할 수도 있고, [OpenZeppelin](https://docs.openzeppelin.com/contracts/4.x/erc20)과 같이 이미 구현 된 라이브러리를 사용해서 작업 할 수도 있다.

# OpenZeppelin ERC-20

### `ERC20`

```solidity
contract ERC20 is Context, IERC20, IERC20Metadata {
   ...
}
```

OpenZeppelin의 ERC-20 구현체를 살펴보면 위와 같다. `Context`, `IERC20`, `IERC20Metadata` 이렇게 세개의 Contract를 inherit한다. 각각의 부모 Context 역시 살펴보자.

### `Context`

```solidity
abstract contract Context {
    function _msgSender() internal view virtual returns (address) {
        return msg.sender;
    }

    function _msgData() internal view virtual returns (bytes calldata) {
        return msg.data;
    }
}
```

Provides information about the current execution context, including the
sender of the transaction and its data. While these are generally available
via msg.sender and msg.data, they should not be accessed in such a direct
manner, since when dealing with meta-transactions the account sending and
paying for execution may not be the actual sender (as far as an application
is concerned).

### `IERC-20`

```solidity
interface IERC20 {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool);
}
```

IERC-20은 EIP에 기술되어있는 ERC-20의 인터페이스이다. ERC-20이 구현해야 하는 함수를 명시적으로 알려주는 부모 Contract라고 이해하면 될 것 같다.

- `totalSupply()`: Returns the amount of tokens in existence. This function is a getter and does not modify the state of the contract. Keep in mind that there are no floats in Solidity. Therefore most tokens adopt 18 decimals and will return the total supply and other results as followed `1000000000000000000` for `1` token. Not every token has `18` decimals and this is something you really need to watch for when dealing with tokens.
- `balanceOf(address account)`: Returns the amount of tokens owned by an address (`account`). This function is a getter and does not modify the state of the contract.
- `transfer(address to, uint256 amount)`: Moves the amount of tokens from the function caller address (`msg.sender`) to the recipient address. This function emits the `Transfer` event. It returns true if the transfer was possible.
- `allowance(address owner, address spender)`: The ERC-20 standard allows an address to give an allowance to another address to be able to retrieve tokens from it. This getter returns the remaining number of tokens that the spender will be allowed to spend on behalf of owner. This function is a getter and does not modify the state of the contract and should return `0` by default.
- `approve(address spender, uint256 amount)`: Set the amount of allowance the spender is allowed to transfer from the function caller (`msg.sender`) balance. This function emits the `Approval` event. The function returns whether the allowance was successfully set.
- `transferFrom(address from, address to, uint256 amount)`: Moves the amount of tokens from sender to recipient using the allowance mechanism. amount is then deducted from the caller’s allowance. This function emits the `Transfer` event.
- event `Transfer`: This event is emitted when the amount of tokens (value) is sent from the from address to the to address.
- event `Approval`: This event is emitted when the amount of tokens (value) is approved by the owner to be used by the spender.

### `IERC20Metadata`

```solidity
interface IERC20Metadata is IERC20 {
    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
}
```

말 그대로 토큰의 메타데이터에 대한 인터페이스이다. 이름, 심볼(주식의 티커), decimal 자리수가 있다.

- `name`: 토큰의 이름
- `symbol`: 토큰의 심볼
- `decimals`: 토큰의 decimal place

정리하면 `IERC20`에 있는 함수와, `IERC20Metadata`에 있는 메타 데이터를 포함하는 컨트랙트를 작성하면 그게 ERC-20 규약을 따르는 것이고, 다시 말해 토큰이 되는 것이다.

### Reference

- https://ethereum.org/en/developers/tutorials/understand-the-erc-20-token-smart-contract/
- https://ethereum.org/en/developers/tutorials/erc20-annotated-code/
- https://eips.ethereum.org/EIPS/eip-20
