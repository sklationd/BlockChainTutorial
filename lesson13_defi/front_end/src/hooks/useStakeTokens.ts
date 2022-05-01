import * as React from "react";
import { useContractFunction, useEthers } from "@usedapp/core";
import TokenFarm from "../chain_info/contracts/TokenFarm.json";
import ERC20 from "../chain_info/contracts/MockERC20.json";
import networkMapping from "../chain_info/deployments/map.json";
import { Contract } from "@ethersproject/contracts";
import { constants, utils } from "ethers";

export const useStakeTokens = (tokenAddress: string) => {
  const { chainId } = useEthers();
  const ABI = TokenFarm.abi;
  const tokenFarmAddress = chainId
    ? networkMapping[String(chainId)]["TokenFarm"][0]
    : constants.AddressZero;
  const tokenFarmInterface = new utils.Interface(ABI);
  const tokenFarmContract = new Contract(tokenFarmAddress, tokenFarmInterface);

  const ERC20_ABI = ERC20.abi;
  const ERC20Interface = new utils.Interface(ERC20_ABI);
  const ERC20Contract = new Contract(tokenAddress, ERC20Interface);

  const { send: approveErc20Send, state: approveAndStakeErc20State } =
    useContractFunction(ERC20Contract, "approve", {
      transactionName: "Approve ERC20 transaction",
    });
  const approveAndStake = (amount: string) => {
    setAmountToStake(amount);
    return approveErc20Send(tokenFarmAddress, amount);
  };

  const { send: stakeSend, state: stakeState } = useContractFunction(
    tokenFarmContract,
    "stakeTokens",
    {
      transactionName: "Stake Tokens",
    }
  );

  const [amountToStake, setAmountToStake] = React.useState("0");

  React.useEffect(() => {
    if (approveAndStakeErc20State.status === "Success") {
      stakeSend(amountToStake, tokenAddress);
    }
  }, [approveAndStakeErc20State, amountToStake, tokenAddress, stakeSend]);

  const [state, setState] = React.useState(approveAndStakeErc20State);

  React.useEffect(() => {
    if (approveAndStakeErc20State.status === "Success") {
      setState(stakeState);
    } else {
      setState(approveAndStakeErc20State);
    }
  }, [approveAndStakeErc20State, stakeState]);

  return { approveAndStake, state };
};
