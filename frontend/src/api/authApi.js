import { requests } from "./baseApi";

export const authApi = {
    signIn: (values) => requests.post("/auth/jwt/sign_in/", values),
    signUp: (values) => requests.post("/user/users/", values),
    getUserById: (id) => requests.get(`/user/users/${id}/`),
    editUser: (values, id) => requests.put(`/user/users/${id}/`, values),
    getUsers: () => requests.get("/user/users/"),
    getBrokers: () => requests.get("/shares/brokers/"),
    createBrokerAccount: (values) => requests.post("/shares/accounts/", values),
    getBalances: () => requests.get("/shares/accounts/"),
    getOrders: () => requests.get("/shares/orders/"),
    deleteOrder: (id) => requests.delete(`/shares/orders/${id}`),
    createOrder: (values) => requests.post("/shares/orders/", values),
    getStocks: () => requests.get("/shares/stocks/"),
    getCompanies: () => requests.get("/pyex/data/companies/"),
    getCompanyDataById: (id) => requests.get(`/pyex/data/company_data?symbol=${id}`),
    getCompanySharesById: (id) => requests.get(`/pyex/data/company_shares?symbol=${id}`),
    getBalancesHistory: (account) => requests.get(`/shares/accounts-history?account=${account}`),
    followUser: (id) => requests.patch(`/user/users/${id}/follow/`)
}