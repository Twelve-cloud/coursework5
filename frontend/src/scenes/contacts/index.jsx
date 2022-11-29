import { Box } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataContacts } from "../../data/mockData";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import { useEffect, useState } from "react";
import { authApi } from "../../api/authApi";

const Contacts = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    async function fetchMyAPI() {
      try {
        const users = await authApi.getUsers();
        const modifiedUsers = users.map((user) => ({
          ...user,
          first_name: user.first_name || "-",
          last_name: user.last_name || "-",
          date_joined: new Date(user.date_joined).toLocaleString()
        }))
        setUsers(modifiedUsers)
      } catch (error) {
        console.log(error)
      } finally {
        setLoading(false);
      }
    }

    fetchMyAPI()
  }, [])

  const columns = [
    { field: "id", headerName: "ID", flex: 0.5 },
    {
      field: "email",
      headerName: "Email",
      flex: 1,
    },
    {
      field: "username",
      headerName: "Username",
      flex: 1,
    },
    {
      field: "first_name",
      headerName: "First Name",
      flex: 1,
    },
    {
      field: "last_name",
      headerName: "Last Name",
      flex: 1,
    },
    {
      field: "date_joined",
      headerName: "Join Date",
      flex: 1,
    },
    {
      field: "is_staff",
      headerName: "Is Staff",
      flex: 1,
    },
  ];

  return (
    <Box m="20px">
      <Header
        title="USERS"
        subtitle="List of Users for Future Reference"
      />
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
          "& .MuiDataGrid-toolbarContainer .MuiButton-text": {
            color: `${colors.grey[100]} !important`,
          },
        }}
      >
        <DataGrid
          loading={loading}
          rows={users}
          columns={columns}
          components={{ Toolbar: GridToolbar }}
        />
      </Box>
    </Box>
  );
};

export default Contacts;
