import argparse
import pymysql
from datetime import datetime


class todo:
    cursor = None
    conn = None

    def __init__(self,args):
        self.args= args
        # for i in vars(self.args):
        #     print(i , getattr(self.args, i))
        print(self.args)
        
        #for creating task
        if self.args.create is not None:
            self.createTask(self.args.create)

        #for edit title
        elif self.args.edit_title is not None:
            self.edit_title(self.args.edit_title)
        #for edit status
        elif self.args.edit_status is not None:
            self.edit_status(self.args.edit_status)
        #for delete task
        elif self.args.delete is not None:
            self.deletion(self.args.delete)
        #for search by title
        elif self.args.search is not None:
            self.search(self.args.search)
        #for search by date
        elif self.args.date is not None:
            self.date(self.args.date)
        #retieve all list of taks
        else:
            self.showList(self.args.list)
        
    def connection(self):
        try:
            todo.conn = pymysql.connect(
                host='localhost',
                user='root', 
                password = "ttn",
                db='todo',
            )
            todo.cursor = todo.conn.cursor()
            return True

        except Exception as e:
            print(e)
            return False
    
    #for creating task
    def createTask(self,title):
        if self.connection():
            sql = """insert into todolist(title,created_at) values (%s,%s)"""
            title = " ".join(title)
            tuple = (title,datetime.now())
            try:
                todo.cursor.execute(sql,tuple)
                todo.conn.commit()
                todo.conn.close()
                print("Your task has been created !!")
            except Exception as e:
                print(e)
                todo.conn.rollback()
                todo.conn.close()
    #for edit in titles 
    #update when id is not in database
    def edit_title(self,arr):
        if self.connection():
            arr = sorted(arr)
            id = int(arr[0])
            updated_title = " ".join(arr[1:])
            sql = "update todolist set title = %s where id=%s"
            try:
                tuple = (updated_title,id)
                todo.cursor.execute(sql,tuple)
                todo.conn.commit()
                rowcount = todo.cursor.rowcount
                if rowcount == 0:
                    print(f'There is no task avaliable for id: {id}')
                else:
                    print(f'Your have updated your title of task id: {id}')
                todo.conn.close()
            except Exception as e:
                print(e)
                todo.conn.rollback()
                todo.conn.close()
    #edit status
    def edit_status(self,arr):
        if self.connection():
            arr = sorted(arr)
            id = int(arr[0])
            if arr[1] == 'completed' or arr[1] == 'Completed' or arr[1] == 'COMPLETED':
                sql = "update todolist set status = %s , completed_at = %s where id=%s"
                try:
                    tuple = (arr[1].lower(),datetime.now(),id)
                    todo.cursor.execute(sql,tuple)
                    todo.conn.commit()
                    rowcount = todo.cursor.rowcount
                    if rowcount == 0:
                        print(f'There is no task avaliable for id: {id}')
                    else:
                        print(f'Your have updated the status of task id: {id}')
                    
                    todo.conn.close()
                except Exception as e:
                    print(e)
                    todo.conn.rollback()
                    todo.conn.close()
            else:
                print("status should be like 'completed' or 'Completed' or 'COMPLETED'")
            
    #for deletion
    def deletion(self,id):
        if self.connection():
            for i in range(0,len(id)):
                key = id[i]
                sql = "delete from todolist where id = '%d'" %(key)
                try:
                    todo.cursor.execute(sql)
                    todo.conn.commit()
                    rowcount = todo.cursor.rowcount
                    if rowcount == 0:
                        print(f'There is no task avaliable for id: {key}')
                    else:
                        print(f'Your have deleted task from your todolist id: {key}')
                except Exception as e:
                    print(e)
                    todo.conn.rollback()
                    todo.conn.close()
            todo.conn.close()

    # for show all the list
    def showList(self,status):
        if self.connection():
            if status is None:
                sql = "select * from todolist order by created_at desc"
                try:
                    todo.cursor.execute(sql)
                    results = todo.cursor.fetchall()
                    print("id","title","created_at","completed_at","status")
                    for i in results:
                        id = i[0]
                        title = i[1]
                        created_at = i[2]
                        completed_at = i[3]
                        status = i[4]
                        print(f'{id},{title},{created_at},{completed_at},{status}')
                    todo.conn.close()
                except Exception as e:
                    print(e)
                    todo.conn.close()
            else:
                sql = "select * from todolist where status = %s order by created_at desc"
                print(sql)
                try:
                    todo.cursor.execute(sql,status)
                    results = todo.cursor.fetchall()
                    print("id","title","created_at","completed_at","status")
                    for i in results:
                        id = i[0]
                        title = i[1]
                        created_at = i[2]
                        completed_at = i[3]
                        status = i[4]
                        print(f'{id},{title},{created_at},{completed_at},{status}')
                    todo.conn.close()
                except Exception as e:
                    print(e)
                    todo.conn.close()

    #seach by title
    def search(self,key):
        if self.connection():
            sql = "select * from todolist where title like '%{key}%'".format(key = key[0])
            try:
                todo.cursor.execute(sql)
                results = todo.cursor.fetchall()
                print("id","title","created_at","completed_at","status")
                for i in results:
                    id = i[0]
                    title = i[1]
                    created_at = i[2]
                    completed_at = i[3]
                    status = i[4]
                    print(f'{id},{title},{created_at},{completed_at},{status}')
                todo.conn.close()
            except Exception as e:
                print(e)
                todo.conn.close()

    #search by date
    def date(self,key):
        if self.connection():
            sql = "select * from todolist where created_at like '%{key}%'".format(key = key[0])
            print(sql)
            try:
                todo.cursor.execute(sql)
                results = todo.cursor.fetchall()
                print("id","title","created_at","completed_at","status")
                for i in results:
                    id = i[0]
                    title = i[1]
                    created_at = i[2]
                    completed_at = i[3]
                    status = i[4]
                    print(f'{id},{title},{created_at},{completed_at},{status}')
                todo.conn.close()
            except Exception as e:
                print(e)
                todo.conn.close()

if __name__=='__main__':

    parser = argparse.ArgumentParser(description='Welcome to the todo cli app')
    parser.add_argument('-l','--list',
    type = str,
    choices = ['completed','incomplete'],
    nargs="?",
    help="Get all the list or you can pass complete or incomplete as an argument"
    )
    parser.add_argument('-c','--create',
    type = str,
    nargs='+',
    help="Pass title along with task id"
    )
    parser.add_argument('--edit-title',
    nargs='+',
    help="Pass two argument first is todo list id and second one is to update the title"
    )
    parser.add_argument('--edit-status',
    nargs=2,
    help="Pass two argument first is todo list id and second one is update status"
    )
    parser.add_argument('-d','--delete',
    type=int,
    nargs='+',
    help="Pass the id of task that you wants to delete"
    )
    parser.add_argument('-s','--search',
    type=str,
    nargs=1,
    help="Pass key that you want to search in all the task list"
    )
    parser.add_argument('--date',
    type=str,
    nargs=1,
    help="Pass date as a argument in YYYY-MM-DD format"
    )
    args = parser.parse_args()
    a = todo(args)
    a.connection()

