import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataInvoices } from "../../data/mockData";
import Header from "../../components/Header";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";
import { v4 as uuidv4 } from 'uuid';

const Companies = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [companies, setCompanies] = useState([]);

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
                }}
            >
                <DataGrid onRowClick={(params) => console.log(params.id)} sx={{ cursor: "pointer" }} rows={companies} columns={columns} />
            </Box>
        </Box>
    );
};

export default Companies;
