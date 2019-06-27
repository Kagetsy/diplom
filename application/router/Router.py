class Router:

    def __init__(self, app, web, mediator):

        self.web = web
        self.mediator = mediator
        self.TYPES = mediator.getTypes()
        
        routes = [
            ('GET', '/api/test', self.testHandler),
            ('GET', '/login/{login}/{password}', self.loginHandler),
            ('GET', '/logout/{token}', self.logoutHandler),
            ('*', '/', self.staticHandler)
        ]
        for route in routes:
            app.router.add_route(route[0], route[1], route[2])

        app.add_routes([self.web.static('/', path = './public')])

    async def testHandler(self, request):
        return self.web.json_response({ 'result': 'Hello!' })

    async def loginHandler(self, request):
        login = request.match_info.get('login')
        password = request.match_info.get('password')
        user = self.mediator.call(self.TYPES['LOGIN'],{ 'login': login, 'password': password})
        #return self.web.json_response({'result':{ 'login': login, 'password': password}})
        return self.web.json_response('yeees')

    def logoutHandler(self, request):
        token = request.match_info.get('token')
        #result = self.userManager.logout((token))
        return self.web.json_response(token)

    async def staticHandler(self, request):
        return self.web.FileResponse('./public/index.html')