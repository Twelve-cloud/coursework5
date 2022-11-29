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
    getStocks: () => requests.get("/shares/stocks/"),
    getCompanies: () => requests.get("/pyex/data/companies/")
}