import * as React from "react";
import { Token } from "../Main";
import Box from "@mui/material/Box";
import Tab from "@mui/material/Tab";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { WalletBalance } from "./WalletBalance";
import { StakeForm } from "./StakeForm";
import { styled } from "@mui/system";

interface YourWalletProps {
  supportedTokens: Array<Token>;
}

const StyledTabContent = styled("div")({
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  gap: 32,
});

const StyledBox = styled("div")({
  backgroundColor: "white",
  borderRadius: 25,
});

const StyledHeader = styled("h1")({
  color: "white",
});

export const YourWallet = ({ supportedTokens }: YourWalletProps) => {
  const [selectedTokenIndex, setSelectedTokenIndex] = React.useState<number>(0);

  const handleChange = (event: React.ChangeEvent<{}>, newValue: string) => {
    setSelectedTokenIndex(parseInt(newValue));
  };

  return (
    <Box>
      <StyledHeader>Your Wallet</StyledHeader>
      <StyledBox>
        <TabContext value={selectedTokenIndex.toString()}>
          <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
            <TabList onChange={handleChange} aria-label="Stake form tabs">
              {supportedTokens.map((token, index) => {
                return (
                  <Tab
                    label={token.name}
                    value={index.toString()}
                    key={index}
                  ></Tab>
                );
              })}
            </TabList>
          </Box>
          {supportedTokens.map((token, index) => {
            return (
              <TabPanel value={index.toString()} key={index}>
                <StyledTabContent>
                  <WalletBalance token={token} />
                  <StakeForm token={token}></StakeForm>
                </StyledTabContent>
              </TabPanel>
            );
          })}
        </TabContext>
      </StyledBox>
    </Box>
  );
};
