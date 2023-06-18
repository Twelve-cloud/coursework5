import { Field, Form } from 'react-final-form';
import {
    Card,
    Grid,
    TextField,
    Button,
    alpha,
    Typography,
    InputAdornment,
    IconButton,
    Alert,
    Divider,
    Slide,
    Snackbar,
} from "@mui/material";
import VisibilityIcon from "@mui/icons-material/Visibility";
import VisibilityOffIcon from "@mui/icons-material/VisibilityOff";
import { makeStyles } from "@mui/styles";
import { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { authApi } from '../../api/authApi';
import AlertNotification from "../common/AlertNotification";

const useStyles = makeStyles((theme) => ({
    rootCard: {
        padding: "20px",
        width: "550px",
    },
    cardTitle: {
        fontSize: "28px",
        fontWeight: 500,
        fontFamily: "Roboto",
    },
    gridItem: {
        paddingTop: "13px",
    },
    inputLabel: {
        color: alpha(theme.palette.text.primary, 0.54),
        fontSize: "16px",
        marginBottom: "8px",
    },
    errorText: {
        color: theme.palette.error.main,
        fontSize: "14px",
        marginTop: "8px",
    },
    button: {
        padding: "8px 0 8px 0",
        fontWeight: 500,
    },
    iconButton: {
        color: theme.palette.text.secondary,
    },
}));

const SignUpForm = () => {
    const classes = useStyles();
    const navigate = useNavigate();
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState(false);
    const [showNotification, setShowNotification] = useState(false);

    const handleNotificationClose = () => {
        setShowNotification(false);
    };

    const onSubmit = async (values) => {

        try {
            await authApi.signUp(values);
            setError(false);
            setShowNotification(true)
        } catch (error) {
            console.log(error)
            setError(true);
        }
    }

    return (
        <div style={{
            display: "flex",
            justifyContent: "center",
            marginTop: "150px"
        }}>
            <Card className={classes.rootCard}>
                <Form
                    onSubmit={onSubmit}
                    subscription={{ submitting: true, invalid: true }}
                    render={({ handleSubmit, submitting, invalid }) => (
                        <form onSubmit={handleSubmit} noValidate>
                            <Grid container direction="column">
                                <Grid item className={classes.gridItem}>
                                    <Typography
                                        className={classes.inputLabel}
                                    >Email</Typography>
                                    <Field name="email">
                                        {({ input, meta }) => (
                                            <>
                                                <TextField
                                                    {...input}
                                                    autoComplete="email"
                                                    size="small"
                                                    fullWidth
                                                    variant="outlined"
                                                    error={meta.touched && !!meta.error}
                                                />
                                            </>
                                        )}
                                    </Field>
                                </Grid>
                                <Grid item className={classes.gridItem}>
                                    <Typography
                                        className={classes.inputLabel}
                                    >Username</Typography>
                                    <Field name="username">
                                        {({ input, meta }) => (
                                            <>
                                                <TextField
                                                    {...input}
                                                    autoComplete="username"
                                                    size="small"
                                                    fullWidth
                                                    variant="outlined"
                                                    error={meta.touched && !!meta.error}
                                                />
                                            </>
                                        )}
                                    </Field>
                                </Grid>
                                <Grid item className={classes.gridItem}>
                                    <Typography
                                        className={classes.inputLabel}
                                    >Password</Typography>
                                    <Field name="password">
                                        {({ input, meta }) => (
                                            <>
                                                <TextField
                                                    {...input}
                                                    autoComplete="current-password"
                                                    type={showPassword ? "text" : "password"}
                                                    fullWidth
                                                    size="small"
                                                    margin="dense"
                                                    sx={{ marginTop: "0px" }}
                                                    InputProps={{
                                                        endAdornment: (
                                                            <InputAdornment
                                                                position="end"
                                                                style={{ marginRight: -8 }}
                                                            >
                                                                <IconButton
                                                                    className={classes.iconButton}
                                                                    onClick={() => setShowPassword((prev) => !prev)}
                                                                >
                                                                    {showPassword ? (
                                                                        <VisibilityIcon />
                                                                    ) : (
                                                                        <VisibilityOffIcon />
                                                                    )}
                                                                </IconButton>
                                                            </InputAdornment>
                                                        ),
                                                    }}
                                                />
                                            </>
                                        )}
                                    </Field>
                                </Grid>
                            </Grid>
                            {error && (
                                <Alert sx={{ marginTop: "15px" }} severity="error">
                                    User already exists
                                </Alert>
                            )}
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}
                                disabled={invalid}
                            >
                                Sign Up
                            </Button>
                            <Divider>OR</Divider>
                            <Button
                                onClick={() => navigate("/sign-in")}
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2 }}
                                disabled={invalid}
                            >
                                Sign In
                            </Button>
                        </form>
                    )}
                />
            </Card>
            <Snackbar
                anchorOrigin={{ vertical: "bottom", horizontal: "right" }}
                open={showNotification}
                TransitionComponent={Slide}
                onClose={handleNotificationClose}
                key="bottom right"
                autoHideDuration={4000}
            >
                <AlertNotification
                    onClose={handleNotificationClose}
                    severity="success"
                    sx={{ width: "100%" }}
                >
                    Sign up user successfully
                </AlertNotification>
            </Snackbar>
        </div>
    );
};

export default SignUpForm;
