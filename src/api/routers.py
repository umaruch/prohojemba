from src.api.endpoints import auth, users, titles, activities

routers = {
    "/auth": auth.router,
    "/users": users.router,
    "/titles": titles.router,
    "/activities": activities.router
}