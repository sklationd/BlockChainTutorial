import { useEthers } from "@usedapp/core";
import { Button } from "@mui/material";
import { styled } from "@mui/system";

const Container = styled("div")({
  display: "flex",
  justifyContent: "flex-end",
  padding: 8,
});

export const Header = () => {
  const { account, activateBrowserWallet, deactivate } = useEthers();
  const isConnected = account !== undefined;
  return (
    <Container>
      {isConnected ? (
        <Button variant="outlined" onClick={deactivate}>
          Disconnect
        </Button>
      ) : (
        <Button variant="contained" onClick={() => activateBrowserWallet()}>
          Connect
        </Button>
      )}
    </Container>
  );
};
