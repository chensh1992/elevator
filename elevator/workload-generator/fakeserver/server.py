import web
import json

urls = (
   '/reset', 'Reset',
   '/workload', 'WorkLoad'
)
app = web.application(urls, globals())

class Reset:     
   def GET(self):
      return self.POST()   

   def POST(self):
      return json.dumps({
         1: {'floor':0, "users":[]},
         2: {'floor':0, "users":[]},
         3: {'floor':0, "users":[]},
      })

class WorkLoad:        
   def POST(self):
      data = web.data()
      request = None
      goto = None
      if data: 
         workload = json.loads(data)
         request = workload.get('request', [])
         goto = workload('goto', [])
      print(request)
      print(goto)
      return json.dumps({
         1: {'floor':0, "users":[]},
         2: {'floor':0, "users":[]},
         3: {'floor':0, "users":[]},
      })

if __name__ == "__main__":
   app.run()
