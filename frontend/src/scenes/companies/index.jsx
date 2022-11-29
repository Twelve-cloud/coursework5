import { Box, useTheme } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import Header from "../../components/Header";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";
import { useNavigate } from "react-router-dom";

const Companies = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [companies, setCompanies] = useState([]);
    const navigate = useNavigate();

    const columns = [
        { field: "id", headerName: "ID" },
        {
            field: "title",
            headerName: "Title",
            flex: 1,
            cellClassName: "name-column--cell",
        },
    ];

    useEffect(() => {
        async function fetchMyAPI() {
            try {
                const companies = await authApi.getCompanies()
                // const modified = stocks.map((stock) => ({
                //     ...stock,
                //     description: stock.description || "-",
                //     created_at: new Date(stocks.created_at).toLocaleString()
                // }))

                const modified = Object.keys(companies).map(key => ({ id: key, title: companies[key] }));

                setCompanies(modified)
            } catch (error) {
                console.log(error)
            }
        }

        fetchMyAPI()
    }, [])

    return (
        <Box m="20px">
            <Header title="CONPANIES" subtitle="List of Companies" />
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
                    onRowClick={(params) => navigate(`${params.id}`)}
                    sx={{ cursor: "pointer" }}
                    rows={companies}
                    columns={columns}
                    components={{ Toolbar: GridToolbar }} />
            </Box>
        </Box>
    );
};

export default Companies;
