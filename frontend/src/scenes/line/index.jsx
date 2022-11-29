import { Box } from "@mui/material";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";

const Line = () => {
  const [balances, setBalances] = useState([]);

  useEffect(() => {
    async function fetchMyAPI() {
      try {
        const balances = await authApi.getBalances()
        // const balancesHistories = await Promise.all(balances.map(async (balance) => await authApi.getBalancesHistory(balance.id)));

        console.log(balances)
      } catch (error) {
        console.log(error)
      }
    }

    fetchMyAPI()
  }, [])

  return (
    <Box m="20px">
      <Header title="Balance Chart" subtitle="Balance Chart" />
      <Box height="75vh">
        <LineChart />
      </Box>
    </Box>
  );
};

export default Line;
