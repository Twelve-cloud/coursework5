import { useState } from "react";
import { useEffect } from "react";
import {
    Box, Button, TextField, Alert, Select, MenuItem, InputLabel, FormControl, Autocomplete
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import Modal from '@mui/material/Modal';
import { authApi } from "../../api/authApi";

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 500,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

const OrdersFormModal = ({ open, setOpen }) => {
    const handleClose = () => {
        setError(false);
        setOpen(false);
    }
    const [error, setError] = useState(false);
    const [companies, setCompanies] = useState([]);
    const [brokers, setBrokers] = useState([]);

    const handleFormSubmit = async (values) => {
        const finalValues = {
            user: localStorage.getItem('user_id'),
            ...values
        }

        try {
            await authApi.createOrder(finalValues);
            handleClose();
        } catch (error) {
            console.log(error);
            setError(true);
        }
    };


    useEffect(() => {
        async function fetchMyAPI() {

            try {
                const companies = await authApi.getCompanies()
                const modified = Object.keys(companies).map(key => ({ id: key, label: companies[key] }))
                setCompanies(modified)

                const brokers = await authApi.getBrokers();
                setBrokers(brokers);
            } catch (error) {
                console.log(error)
            }
        }

        fetchMyAPI()
    }, [])

    return (
        <div>

            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <Formik
                        onSubmit={handleFormSubmit}
                        initialValues={initialValues}
                        validationSchema={checkoutSchema}
                    >
                        {({
                            values,
                            errors,
                            touched,
                            handleBlur,
                            handleChange,
                            handleSubmit,
                            setFieldValue
                        }) => (
                            <form onSubmit={handleSubmit}>
                                <Box
                                    display="grid"
                                    gap="30px"
                                    gridTemplateColumns="repeat(4, minmax(0, 1fr))"

                                >
                                    <TextField
                                        sx={{ width: 400 }}
                                        className="px-2 my-2"
                                        variant="outlined"
                                        name="type"
                                        select
                                        label="Type"
                                        value={values.type}
                                        onChange={handleChange}
                                        onBlur={handleBlur}
                                        error={!!touched.type && !!errors.type}
                                        helperText={touched.type && errors.type}
                                    >
                                        <MenuItem value="buy">Buy</MenuItem>
                                        <MenuItem value="sel">Sell</MenuItem>

                                    </TextField>
                                    <TextField
                                        fullWidth
                                        variant="filled"
                                        type="text"
                                        label="Description"
                                        onBlur={handleBlur}
                                        onChange={handleChange}
                                        value={values.description}
                                        name="description"
                                        error={!!touched.description && !!errors.description}
                                        helperText={touched.description && errors.description}
                                        sx={{ gridColumn: "span 4", width: 400 }}
                                    />
                                    <TextField
                                        fullWidth
                                        variant="filled"
                                        type="number"
                                        label="Amount"
                                        onBlur={handleBlur}
                                        onChange={handleChange}
                                        value={values.amount}
                                        name="amount"
                                        error={!!touched.amount && !!errors.amount}
                                        helperText={touched.amount && errors.amount}
                                        sx={{ gridColumn: "span 4", width: 400 }}
                                    />
                                    <Autocomplete
                                        disablePortal
                                        onChange={(e, value) => setFieldValue("company", value.id)}
                                        renderOption={(props, option) => (
                                            <li {...props} key={option.id}>
                                                {option.label}
                                            </li>
                                        )}
                                        options={companies}
                                        sx={{ width: 400, gridColumn: "span 4" }}
                                        onBlur={handleBlur}
                                        name="company"
                                        renderInput={(params) => <TextField
                                            label="Company"
                                            fullWidth
                                            name="company"
                                            {...params}
                                        />}
                                    />
                                    <TextField
                                        sx={{ width: 400, gridColumn: "span 4" }}
                                        select
                                        className="px-2 my-2"
                                        variant="outlined"
                                        type="text"
                                        label="Broker"
                                        onBlur={handleBlur}
                                        onChange={handleChange}
                                        value={values.broker}
                                        name="broker"
                                        error={!!touched.broker && !!errors.broker}
                                        helperText={touched.type && errors.type}
                                    >
                                        {brokers.map((broker) => (<MenuItem key={broker.id} value={broker.id}>{broker.name}</MenuItem>))}

                                    </TextField>
                                </Box>
                                {error && (
                                    <Alert sx={{ marginTop: "15px" }} severity="error">
                                        Do not have enough money or stocks
                                    </Alert>
                                )}
                                <Box display="flex" justifyContent="end" mt="20px">
                                    <Button type="submit" color="secondary" variant="contained">
                                        Create order
                                    </Button>
                                </Box>
                            </form>
                        )}
                    </Formik>
                </Box>
            </Modal>
        </div>
    );

}

const checkoutSchema = yup.object().shape({
    type: yup.string().required("required"),
    amount: yup.string().required("required"),
    // company: yup.string().required("required"),
    broker: yup.string().required("required")
});

const initialValues = {
    type: "",
    description: "",
    amount: "",
    company: "",
    broker: "",
};


export default OrdersFormModal;
