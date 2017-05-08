filename = '/home/ashok/project/mockupStudio/blender3droom/blender_room_mockup.py'
exec(compile(open(filename).read(), filename, 'exec'))

# import psycopg2
#
#
# try:
#     conn = psycopg2.connect("dbname='mockup' user='ashok' host='localhost' password=''")
#
# except:
#     print("I am unable to connect to the database")
#
# cur = conn.cursor()
# try:
#     cur.execute("select * from room")
#     records = cur.fetchall()
#     for r in records:
#         print(r)
#     print(records)
#
# except:
#     print("I can't create table")

#sys.path.append('/home/ashok/.virtualenvs/machine_learning/lib/python3.5/site-packages')