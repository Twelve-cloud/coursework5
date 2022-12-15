import { Box } from "@mui/material";
import { DataGrid, GridToolbar } from "@mui/x-data-grid";
import { tokens } from "../../theme";
import { mockDataContacts } from "../../data/mockData";
import Header from "../../components/Header";
import { useTheme } from "@mui/material";
import { useEffect, useState } from "react";
import { authApi } from "../../api/authApi";
import Button from '@mui/material/Button';


export const Followers = () => {
    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const [followers, setFollowers] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedFollowers, setSelectedFollowers] = useState([]);

    useEffect(() => {
        setLoading(true);
        async function fetchMyAPI() {
            try {
                const followers = await authApi.getFollowers()
                const modifiedFollowers = followers.map((follower) => {
                    return {
                        ...follower,
                        first_name: follower.first_name || "-",
                        last_name: follower.last_name || "-",
                        date_joined: new Date(follower.date_joined).toLocaleString()
                    }
                })

                setFollowers(modifiedFollowers)
            } catch (error) {
                console.log(error)
            } finally {
                setLoading(false);
            }
        }

        fetchMyAPI()
    }, [])

    const onBtnClick = async () => {
        try {
            await authApi.removeAllFollowers({
                followers: selectedFollowers
            })

            const newFollowers = followers.filter((follower) => !selectedFollowers.includes(follower.id))

            setFollowers(newFollowers)
        } catch (error) {
            console.log(error)
        }
    }

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
    ];

    return (
        <Box m="20px">
            <Header
                title="Followers"
                subtitle="List of Followers for Future Reference"
            />
            <Button
                color="error"
                size="large"
                variant="contained"
                onClick={onBtnClick}
            >
                Remove followers
            </Button >
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
                    checkboxSelection
                    onSelectionModelChange={(selectionModel) => setSelectedFollowers(selectionModel)}
                    loading={loading}
                    rows={followers}
                    columns={columns}
                    components={{ Toolbar: GridToolbar }}
                />
            </Box>
        </Box>
    );
}

export default Followers;