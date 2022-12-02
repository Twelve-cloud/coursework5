import { Box } from "@mui/material";
import Header from "../../components/Header";
import LineChart from "../../components/LineChart";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";
import CircularProgress from '@mui/material/CircularProgress';

const Line = () => {
  const [lineData, setLineData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchMyAPI() {
      setLoading(true)
      try {
        const balances = await authApi.getBalances()
        const balancesHistories = await Promise.all(balances.map(async (balance) => await authApi.getBalancesHistory(balance.id)));
        const lineData = balancesHistories.map((history, idx) => ({
          id: `Balance ${idx + 1}`,
          data: history.map((balance) => ({
            x: new Date(balance.date).toLocaleString(),
            y: balance.balance
          })).sort(function (a, b) {
            return new Date(b.date) - new Date(a.date);
          })
        }))

        setLineData(lineData.sort());
      } catch (error) {
        console.log(error)
      } finally {
        setLoading(false)
      }
    }

    fetchMyAPI()
  }, [])

  if (loading) {
    return <div style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "calc(100vh - 69px)"
    }}>
      <CircularProgress />
    </div>
  }

  return (
    <Box m="20px">
      <Header title="Balance Chart" subtitle="Balance Chart" />
      <Box height="75vh">
        <LineChart lineData={lineData} />
      </Box>
    </Box>
  );
};

export default Line;
