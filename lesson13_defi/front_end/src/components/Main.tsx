import { useEthers } from "@usedapp/core";
import helperConfig from "../helper-config.json";
import networkMapping from "../chain_info/deployments/map.json";
import brownieConfig from "../brownie-config.json";
import { constants } from "ethers";
import dapp from "../dapp.png";
import weth from "../eth.png";
import dai from "../dai.png";
import { YourWallet } from "./YourWallet/YourWallet";
import { styled } from "@mui/system";

export type Token = {
  image: string;
  address: string;
  name: string;
};

const Head2 = styled("h2")({
  color: "white",
  textAlign: "center",
  padding: 32,
});

export const Main = () => {
  const { chainId } = useEthers();
  const networkName = chainId ? helperConfig[chainId] : "dev";
  const dappTokenAddress = chainId
    ? networkMapping[String(chainId)]["DAppToken"][0]
    : constants.AddressZero;

  const wethTokenAddress = chainId
    ? brownieConfig["networks"][networkName]["weth_token"]
    : constants.AddressZero;

  const fauTokenAddress = chainId
    ? brownieConfig["networks"][networkName]["fau_token"]
    : constants.AddressZero;

  const supportedTokens: Array<Token> = [
    {
      image: dapp,
      address: dappTokenAddress,
      name: "DAPP",
    },
    {
      image: weth,
      address: wethTokenAddress,
      name: "WETH",
    },
    {
      image: dai,
      address: fauTokenAddress,
      name: "DAI",
    },
  ];
  return (
    <>
      <Head2>Dapp Token App</Head2>
      <YourWallet supportedTokens={supportedTokens} />;
    </>
  );
};
