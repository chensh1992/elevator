import web
import json
import manager

urls = (
   '/reset', 'Reset',
   '/workload', 'WorkLoad'
)
app = web.application(urls, globals())


class Reset:
    def GET(self):
        return self.POST()

    def POST(self):
        manager.reset()
        return json.dumps(manager.current())


class WorkLoad:
    def POST(self):
        data = web.data()
        request = []
        goto = []
        if data:
            workload = json.loads(data)
            request = workload.get('request', [])
            goto = workload.get('goto', [])
            print data
        manager.process(request, goto)
        manager.dump()
        return json.dumps(manager.current())


if __name__ == "__main__":
    app.run()
