import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom';
import { authApi } from '../../api/authApi';

import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { Box } from "@mui/material";

import Chip from '@mui/material/Chip';
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress';
import BarChart from '../../components/BarChart';

const card = (data) => (
    <React.Fragment>
        <CardContent>
            <img style={{ marginBottom: "15px" }} src={data.logo.url} alt="Company logo" />
            <Typography sx={{ fontSize: 16 }}>
                Company Name: {data.companyName}
            </Typography>
            <Typography sx={{ fontSize: 16 }}>
                Company CEO: {data.CEO}
            </Typography>
            <Typography sx={{ fontSize: 16, mb: 1.5 }} gutterBottom>
                Company Address: {data.country}, {data.state}, {data.city}, {data.address}
            </Typography>
            <Typography sx={{ fontSize: 16, mb: 1.5 }} color="text.secondary">
                {data.description}
            </Typography>
            <Typography sx={{ fontSize: 16 }}>
                Employees Count: {data.employees}
            </Typography>
            <Typography sx={{ fontSize: 16 }}>
                Exchange: {data.exchange}
            </Typography>
            <Typography sx={{ fontSize: 16, mb: 1.5 }}>
                Industry: {data.industry}
            </Typography>
            {data.tags && <Stack direction="row" spacing={1}>
                {data.tags.map(tag => <Chip key={tag} label={tag} />)}

            </Stack>}

            <Typography sx={{ mt: 4 }} color="text.secondary">
                +{data.phone},{" "}
                {data.website},{" "}
                zip-code: {data.zip}
            </Typography>
        </CardContent>
    </React.Fragment>
);

const Company = () => {
    const params = useParams();
    const [data, setData] = useState({ logo: {} });
    const [shares, setShares] = useState({ chart: [] });
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        async function fetchMyAPI() {
            try {
                setLoading(true);
                const data = await authApi.getCompanyDataById(params.companyId);
                setData(data)

                const shares = await authApi.getCompanySharesById(params.companyId);

                setShares(shares)
            } catch (error) {
                console.log(error)
            } finally {
                setLoading(false)
            }
        }

        fetchMyAPI()
    }, [])

    return (
        <div>
            <div style={{ width: "95%", margin: "40px auto 0px auto" }}>
                <Card variant="outlined" sx={{ minHeight: "400px" }}>
                    {loading ?
                        <div style={{
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            height: "400px"
                        }}>
                            <CircularProgress />
                        </div>
                        :
                        card(data)}
                </Card>
            </div>
            {!loading && <Box height="75vh" style={{ marginBottom: "40px" }}>
                <BarChart graphData={shares.chart.slice(0, 100)} />
            </Box>}
        </div>
    )
}

export default Company;