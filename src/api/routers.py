from src.api.endpoints import auth, users

routers = {
    "/auth": auth.router,
    "/users": users.router
}