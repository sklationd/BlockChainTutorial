import { styled } from "@mui/system";

interface BalanceMsgProps {
  label: string;
  tokenImgSrc: string;
  amount: number;
}

const Container = styled("div")({
  display: "inline-grid",
  gridTemplateColumns: "auto auto auto",
  gap: 8,
  alignItems: "center",
});

const TokenImg = styled("img")({
  width: "32px",
});

const Amount = styled("div")({
  fontWeight: 700,
});

export const BalanceMsg = ({ label, tokenImgSrc, amount }: BalanceMsgProps) => {
  return (
    <Container>
      <div>{label}</div>
      <Amount>{amount}</Amount>
      <TokenImg src={tokenImgSrc} alt="Token Logo" />
    </Container>
  );
};
