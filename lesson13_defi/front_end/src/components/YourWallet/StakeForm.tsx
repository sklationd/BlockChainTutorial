import * as React from "react";
import { useNotifications } from "@usedapp/core";
import { Token } from "../Main";
import { Button, Input, CircularProgress } from "@mui/material";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import { useStakeTokens } from "../../hooks/useStakeTokens";
import { utils } from "ethers";

interface StakeFormProps {
  token: Token;
}

export const StakeForm = ({ token }: StakeFormProps) => {
  const { address: tokenAddress } = token;
  const { notifications } = useNotifications();

  const [amount, setAmount] = React.useState<
    number | string | Array<number | string>
  >(0);

  const handleChange: React.ChangeEventHandler<HTMLInputElement> = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const newAmount =
      event.target.value === "" ? "" : Number(event.target.value);
    setAmount(newAmount);
    console.log(newAmount);
  };

  const { approveAndStake, state: approveAndStakeErc20State } =
    useStakeTokens(tokenAddress);
  const handleStakeSubmit = () => {
    const amountAsWei = utils.parseEther(amount.toString());
    return approveAndStake(amountAsWei.toString());
  };

  const isMining = approveAndStakeErc20State.status === "Mining";
  const [showERC20ApprovalSuccess, setShowERC20ApprovalSuccess] =
    React.useState(false);
  const [showStakeTokenSuccess, setShowStakeTokenSuccess] =
    React.useState(false);

  const handleCloseSnack = () => {
    setShowERC20ApprovalSuccess(false);
    setShowStakeTokenSuccess(false);
  };

  React.useEffect(() => {
    if (
      notifications.filter(
        (notification) =>
          notification.type === "transactionSucceed" &&
          notification.transactionName === "Approve ERC20 transaction"
      ).length > 0
    ) {
      setShowERC20ApprovalSuccess(true);
      setShowStakeTokenSuccess(false);
    }

    if (
      notifications.filter(
        (notification) =>
          notification.type === "transactionSucceed" &&
          notification.transactionName === "Stake Tokens"
      ).length > 0
    ) {
      setShowERC20ApprovalSuccess(false);
      setShowStakeTokenSuccess(true);
    }
  }, [notifications, showERC20ApprovalSuccess, showStakeTokenSuccess]);

  return (
    <>
      <div>
        <Input
          placeholder="Staking amount"
          type="number"
          onChange={handleChange}
        />
        <Button
          onClick={handleStakeSubmit}
          size="large"
          color="primary"
          variant="contained"
          disabled={isMining}
        >
          {isMining ? <CircularProgress size={26} /> : "Stake !"}
        </Button>
      </div>
      <Snackbar
        open={showERC20ApprovalSuccess}
        autoHideDuration={5000}
        onClose={handleCloseSnack}
      >
        <Alert onClose={handleCloseSnack} severity="success">
          ERC-20 token transfer approved! Now approve the staking transaction!
          🍕
        </Alert>
      </Snackbar>
      <Snackbar
        open={showStakeTokenSuccess}
        autoHideDuration={5000}
        onClose={handleCloseSnack}
      >
        <Alert onClose={handleCloseSnack} severity="success">
          ERC-20 token staking finished! 😎
        </Alert>
      </Snackbar>
    </>
  );
};
