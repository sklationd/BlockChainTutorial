import React from "react";
import { DAppProvider, Rinkeby, Kovan } from "@usedapp/core";
import { Header } from "./components/Header";
import { Main } from "./components/Main";
import { Container } from "@mui/material";

function App() {
  return (
    <DAppProvider
      config={{
        networks: [Rinkeby, Kovan],
        notifications: {
          expirationPeriod: 1000,
          checkInterval: 1000,
        },
      }}
    >
      <Header />
      <Container maxWidth="md">
        <Main></Main>
      </Container>
    </DAppProvider>
  );
}

export default App;
