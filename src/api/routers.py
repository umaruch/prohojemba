from src.api.endpoints import auth, users, titles, reviews, activity

routers = {
    "/auth": auth.router,
    "/users": users.router,
    "/titles": titles.router,
    "/reviews": reviews.router,
    "/activity": activity.router
}