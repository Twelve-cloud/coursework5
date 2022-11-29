import { Box, Typography, useTheme, Button } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataInvoices } from "../../data/mockData";
import Header from "../../components/Header";
import { useState } from "react";
import { useEffect } from "react";
import { authApi } from "../../api/authApi";
import OrdersFormModal from "./OrdersFormModal";
import IconButton from '@mui/material/IconButton';
import DeleteIcon from '@mui/icons-material/Delete';

const Orders = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [orders, setOrders] = useState([]);
    const [openFormModal, setOpenFormModal] = useState(false);

    const onDeleteBtnClick = async (id) => {
        try {
            await authApi.deleteOrder(id);
            const newOrders = orders.filter(order => order.id !== id)
            setOrders(newOrders)
        } catch (error) {
            console.log(error)
        }
    }

    const columns = [
        { field: "id", headerName: "ID" },
        {
            field: "broker",
            headerName: "Broker",
            flex: 1,
            cellClassName: "name-column--cell",
        },
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
            field: "type",
            headerName: "Type",
            flex: 1,
            renderCell: (params) => (
                <Typography color={colors.greenAccent[500]}>
                    {params.value}
                </Typography>
            ),
        },
        {
            field: "description",
            headerName: "Description",
            flex: 1,
        },
        {
            field: "created_at",
            headerName: "Created At",
            flex: 1,
        },
        {
            field: "",
            headerName: "Delete",
            flex: 1,
            renderCell: (params) => (
                <IconButton onClick={() => onDeleteBtnClick(params.id)} color="error" aria-label="delete" size="large" >
                    <DeleteIcon fontSize="inherit" />
                </IconButton>
            ),
        },
    ];

    useEffect(() => {
        async function fetchMyAPI() {
            try {
                const orders = await authApi.getOrders()
                const modified = orders.map((order) => ({
                    ...order,
                    description: order.description || "-",
                    created_at: new Date(order.created_at).toLocaleString()
                }))

                setOrders(modified)
            } catch (error) {
                console.log(error)
            }
        }

        fetchMyAPI()
    }, [openFormModal])

    return (
        <>
            <Box m="20px">
                <Header title="ORDERS" subtitle="List of Orders" />
                <Button onClick={() => setOpenFormModal(true)} variant="contained" sx={{ background: colors.blueAccent[700] }}>Create order</Button>
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
                    <DataGrid rows={orders} columns={columns} />
                </Box>
            </Box>
            <OrdersFormModal open={openFormModal} setOpen={setOpenFormModal} setOrders={setOrders} />
        </>
    );
};

export default Orders;
