from src.api.endpoints import auth, debug

routers = {
    "/auth": auth.router,
    "/debug": debug.router
}