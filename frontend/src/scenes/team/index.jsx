import { Box, Button, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataTeam } from "../../data/mockData";
import Header from "../../components/Header";
import { useState, useEffect } from "react";
import { authApi } from "../../api/authApi";

const Team = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [brokers, setBrokers] = useState([]);
  const columns = [
    { field: "id", headerName: "ID" },
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      cellClassName: "name-column--cell",
    },
    {
      field: "description",
      headerName: "Description",
      flex: 1
    },
    {
      field: "rate",
      headerName: "Rate",
      flex: 1,
    },
    {
      field: "Accounts",
      headerName: "Accounts",
      flex: 1,
      renderCell: ({ id }) => {
        return (
          <Button onClick={() => onCreateClick(id)} sx={{ backgroundColor: colors.greenAccent[600] }}>Create account</Button>
        );
      },
    },
  ];

  useEffect(() => {
    async function fetchMyAPI() {
      try {
        const brokers = await authApi.getBrokers();
        const modified = brokers.map((broker) => ({
          ...broker,
          description: broker.description || "-",
        }))
        setBrokers(modified)
      } catch (error) {
        console.log(error)
      }
    }

    fetchMyAPI()
  }, [])

  const onCreateClick = async (id) => {
    const values = {
      user: Number(localStorage.getItem("user_id")),
      broker: id,
      balance: 5000,
      balance_with_shares: 0,
    }

    try {
      await authApi.createBrokerAccount(values);
    } catch (error) {
      console.log(error)
    }

  }

  return (
    <Box m="20px">
      <Header title="BROKERS" subtitle="Managing the Brokers Members" />
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
        <DataGrid rows={brokers} columns={columns} />
      </Box>
    </Box>
  );
};

export default Team;
