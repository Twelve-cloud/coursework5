import { Box, Typography, useTheme } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataInvoices } from "../../data/mockData";
import Header from "../../components/Header";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";

const Stocks = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [stocks, setStocks] = useState([]);

    const columns = [
        { field: "id", headerName: "ID" },
        {
            field: "company",
            headerName: "Company",
            flex: 1,
        },
        {
            field: "amount",
            headerName: "Stocks Amount",
            flex: 1,
        },
        {
            field: "current_price",
            headerName: "Current Price",
            flex: 1,
            cellClassName: "name-column--cell",
        },
    ];

    useEffect(() => {
        async function fetchMyAPI() {
            try {
                const stocks = await authApi.getStocks()
                // const modified = stocks.map((stock) => ({
                //     ...stock,
                //     description: stock.description || "-",
                //     created_at: new Date(stocks.created_at).toLocaleString()
                // }))

                console.log(stocks)
                setStocks(stocks)
            } catch (error) {
                console.log(error)
            }
        }

        fetchMyAPI()
    }, [])

    return (
        <Box m="20px">
            <Header title="STOCKS" subtitle="List of Stocks" />
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
                <DataGrid rows={stocks} columns={columns} />
            </Box>
        </Box>
    );
};

export default Stocks;
