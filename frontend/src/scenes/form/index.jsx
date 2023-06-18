import {
  Box, Button, TextField, Slide,
  Snackbar, Alert
} from "@mui/material";
import { Formik } from "formik";
import * as yup from "yup";
import useMediaQuery from "@mui/material/useMediaQuery";
import Header from "../../components/Header";
import { authApi } from '../../api/authApi';
import { useState } from "react";
import AlertNotification from "../common/AlertNotification";
import { useEffect } from "react";

const Form = () => {
  const isNonMobile = useMediaQuery("(min-width:600px)");
  const [error, setError] = useState(false);
  const [showNotification, setShowNotification] = useState(false);
  const [user, setUser] = useState({
    first_name: "",
    last_name: "",
    email: "",
    username: "",
    password: "",
    date_joined: "",
    last_login: "",
    is_blocked: false
  });
  const [loading, setLoading] = useState(false);


  const handleNotificationClose = () => {
    setShowNotification(false);
  };

  const handleFormSubmit = async (values) => {
    console.log(values)
    try {
      await authApi.editUser(values, localStorage.getItem('user_id'));
      setError(false);
      setShowNotification(true)
    } catch (error) {
      console.log(error)
      setError(true);
    }
  };

  useEffect(() => {
    async function fetchMyAPI() {
      setLoading(true)
      try {
        const user = await authApi.getUserById(localStorage.getItem('user_id'));
        setUser(user)
      } catch (error) {
        console.log(error)
      } finally {
        setLoading(false)
      }
    }

    fetchMyAPI()
  }, [])

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <Box m="20px">
      <Header title="EDIT USER" subtitle="Edit User Profile" />

      <Formik
        onSubmit={handleFormSubmit}
        initialValues={{
          first_name: user.first_name,
          last_name: user.last_name,
          email: user.email,
          username: user.username,
          password: user.password,
          date_joined: new Date(user.date_joined).toLocaleString(),
          last_login: new Date(user.last_login).toLocaleString(),
          is_blocked: user.is_blocked
        }}
        validationSchema={checkoutSchema}
      >
        {({
          values,
          errors,
          touched,
          handleBlur,
          handleChange,
          handleSubmit,
        }) => (
          <form onSubmit={handleSubmit}>
            <Box
              display="grid"
              gap="30px"
              gridTemplateColumns="repeat(4, minmax(0, 1fr))"
              sx={{
                "& > div": { gridColumn: isNonMobile ? undefined : "span 4" },
              }}
            >
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="First Name"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.first_name}
                name="first_name"
                error={!!touched.first_name && !!errors.first_name}
                helperText={touched.first_name && errors.first_name}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Last Name"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.last_name}
                name="last_name"
                error={!!touched.last_name && !!errors.last_name}
                helperText={touched.last_name && errors.last_name}
                sx={{ gridColumn: "span 2" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Email"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.email}
                name="email"
                disabled={true}
                error={!!touched.email && !!errors.email}
                helperText={touched.email && errors.email}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Username"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.username}
                name="username"
                disabled={true}
                error={!!touched.username && !!errors.username}
                helperText={touched.username && errors.username}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Join Date"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.date_joined}
                name="date_joined"
                disabled={true}
                error={!!touched.password && !!errors.password}
                helperText={touched.password && errors.password}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Last Login Date"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.last_login}
                name="last_login"
                disabled={true}
                error={!!touched.password && !!errors.password}
                helperText={touched.password && errors.password}
                sx={{ gridColumn: "span 4" }}
              />
              <TextField
                fullWidth
                variant="filled"
                type="text"
                label="Is Blocked?"
                onBlur={handleBlur}
                onChange={handleChange}
                value={values.is_blocked}
                name="is_blocked"
                disabled={true}
                error={!!touched.password && !!errors.password}
                helperText={touched.password && errors.password}
                sx={{ gridColumn: "span 4" }}
              />
            </Box>
            {error && (
              <Alert sx={{ marginTop: "15px" }} severity="error">
                User already exists
              </Alert>
            )}
            <Box display="flex" justifyContent="end" mt="20px">
              <Button type="submit" color="secondary" variant="contained">
                Edit User
              </Button>
            </Box>
          </form>
        )}
      </Formik>
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
    </Box>
  );
};

const phoneRegExp =
  /^((\+[1-9]{1,4}[ -]?)|(\([0-9]{2,3}\)[ -]?)|([0-9]{2,4})[ -]?)*?[0-9]{3,4}[ -]?[0-9]{3,4}$/;

const checkoutSchema = yup.object().shape({
  email: yup.string().email("invalid email").required("required"),
  username: yup.string().required("required"),
  password: yup.string().required("required"),
});
const initialValues = {
  first_name: "",
  last_name: "",
  email: "",
  username: "",
  password: "",
};

export default Form;
