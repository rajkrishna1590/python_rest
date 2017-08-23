import MySQLdb
import web
import json
import auth

#Auth = auth.Authentication()

db=MySQLdb.connect("localhost","root","","raj")
c=db.cursor()

urls = (
    '/users', 'users',     
    '/create_user', 'users',
    '/users/(.*)', 'get_user'
)

app = web.application(urls, globals())

class users:

    @auth.Authentication
    def POST(self):
        data = json.loads(web.data())
        print(data)
        sql = "insert into users(name,password,age) VALUES ('%s','%s', %d)" % (data["name"],data["password"], data["age"])
        print(sql)
        try:            
            c.execute(sql)
            db.commit()
            success = {'message':'New user added'}
            return success
        except:
            print "Error: unable to insert data"
            error = {'error':'unable to insert the data'}
            return error 

    @auth.Authentication
    def GET(self):
        sql = "select * from users"
        output = {'users':[]}       
        try:            
            c.execute(sql)
            results = c.fetchall()
            if len(results) ==0:
                empty = {'message':'user list empty'}
                return empty
            for row in results:
                print(row)
                mapObj={}
                mapObj["id"] = row[0]
                mapObj["name"] = row[1]
                mapObj["age"] = row[2]
                output["users"].append(mapObj)
            return json.dumps(output)
        except:
            print "Error: unable to fecth data"
            error = {'error':'unable to fecth data'}
            return error

class get_user:
    @auth.Authentication
    def GET(self, user):
        sql = "select * from users where id="+user
        try:            
            c.execute(sql)
            results = c.fetchall()
            if len(results) ==0:
                empty = {'message':'user not found'}
                return empty
            mapObj={}        
            for row in results:
                mapObj["id"] = row[0]
                mapObj["name"] = row[1]
                mapObj["age"] = row[2]
            return json.dumps(mapObj)
        except:
            print "Error: unable to fecth data"
            error = {'error':'unable to fecth data'}
            return error
        
if __name__ == "__main__":
    app.run()
    
