import { useLayoutEffect, useState } from "react";
import { Routes, Route, useLocation } from "react-router-dom";
import Topbar from "./scenes/global/Topbar";
import Sidebar from "./scenes/global/Sidebar";
import Dashboard from "./scenes/dashboard";
import Team from "./scenes/brokers";
import Invoices from "./scenes/invoices";
import Contacts from "./scenes/users";
import Bar from "./scenes/bar";
import Form from "./scenes/form";
import Line from "./scenes/line";
import Pie from "./scenes/pie";
import FAQ from "./scenes/faq";
import Geography from "./scenes/geography";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { ColorModeContext, useMode } from "./theme";
import Calendar from "./scenes/calendar/calendar";
import SignInForm from "./scenes/auth/SignInForm"
import SignUpForm from "./scenes/auth/SignUpForm"
import Orders from "./scenes/orders";
import Stocks from "./scenes/stocks";
import Companies from "./scenes/companies";
import Company from "./scenes/companies/Company";

function App() {
  const [theme, colorMode] = useMode();
  const [isSidebar, setIsSidebar] = useState(true);
  const [showTopbar, setShowTopbar] = useState(true);
  const [showSidebar, setShowSidebar] = useState(true);
  const location = useLocation();

  useLayoutEffect(() => {
    if (location.pathname === "/sign-in" || location.pathname === "/sign-up") {
      setShowTopbar(false)
    } else {
      setShowTopbar(true);
    }

    if (location.pathname === "/sign-in" || location.pathname === "/sign-up") {
      setShowSidebar(false);
    } else {
      setShowSidebar(true)
    }
  }, [location.pathname]);

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div className="app">
          <Sidebar show={showSidebar} isSidebar={isSidebar} />
          <main className="content">
            <Topbar show={showTopbar} setIsSidebar={setIsSidebar} />
            <Routes>
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/sign-in" element={<SignInForm />} />
              <Route path="/sign-up" element={<SignUpForm />} />
              <Route path="/team" element={<Team />} />
              <Route path="/stocks" element={<Stocks />} />
              <Route path="/contacts" element={<Contacts />} />
              <Route path="/companies" element={<Companies />} />
              <Route exact path="/companies/:companyId" element={<Company />} />
              <Route path="/invoices" element={<Invoices />} />
              <Route path="/orders" element={<Orders />} />
              <Route path="/form" element={<Form />} />
              <Route path="/bar" element={<Bar />} />
              <Route path="/pie" element={<Pie />} />
              <Route path="/line" element={<Line />} />
              <Route path="/faq" element={<FAQ />} />
              <Route path="/calendar" element={<Calendar />} />
              <Route path="/geography" element={<Geography />} />
            </Routes>
          </main>
        </div>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App;
