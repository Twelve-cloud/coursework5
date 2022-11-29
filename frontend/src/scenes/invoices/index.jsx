import { Box, Button, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataInvoices } from "../../data/mockData";
import Header from "../../components/Header";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";

const Invoices = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [balances, setBalances] = useState([]);

  const columns = [
    { field: "id", headerName: "ID" },
    {
      field: "broker",
      headerName: "Broker",
      flex: 1,
    },
    {
      field: "balance",
      headerName: "Balance",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "balance_with_shares",
      headerName: "Balance With Shares",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "updated_at",
      headerName: "Updated Date",
      flex: 1,
    },
  ];

  useEffect(() => {
    async function fetchMyAPI() {
      try {
        const balances = await authApi.getBalances()
        const modified = balances.map((balance) => ({
          ...balance,
          balance: balance.balance + "$",
          balance_with_shares: balance.balance_with_shares + "$",
          updated_at: new Date(balance.updated_at).toLocaleString(),
        }))

        setBalances(modified)
      } catch (error) {
        console.log(error)
      }
    }

    fetchMyAPI()
  }, [])

  return (
    <Box m="20px">
      <Header title="BALANCES" subtitle="List of Balances" />
      <Box
        m="40px 0 0 0"
        height="75vh"
        sx={{
          "& .MuiDataGrid-root": {
            border: "none",
          },
          "& .MuiDataGrid-cell": {
            borderBottom: "none",
          },
          "& .name-column--cell": {
            color: colors.greenAccent[300],
          },
          "& .MuiDataGrid-columnHeaders": {
            backgroundColor: colors.blueAccent[700],
            borderBottom: "none",
          },
          "& .MuiDataGrid-virtualScroller": {
            backgroundColor: colors.primary[400],
          },
          "& .MuiDataGrid-footerContainer": {
            borderTop: "none",
            backgroundColor: colors.blueAccent[700],
          },
          "& .MuiCheckbox-root": {
            color: `${colors.greenAccent[200]} !important`,
          },
        }}
      >
        <DataGrid rows={balances} columns={columns} />
      </Box>
    </Box>
  );
};

export default Invoices;
