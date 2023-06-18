import MuiAlert from "@mui/material/Alert";
import React from "react";

const AlertNotification = React.forwardRef(
    function Alert(props, ref) {
        return <MuiAlert elevation={10} ref={ref} variant="filled" {...props} />;
    }
);

export default AlertNotification;