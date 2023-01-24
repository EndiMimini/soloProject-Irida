import mysql.connector


def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)


def readBLOB(id, image):
    print("Reading BLOB data from python_employee table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='devsOnDeck',
                                            user='root',
                                            password='root')

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from frameworks where id = %s"""

        cursor.execute(sql_fetch_blob_query, (id,))
        record = cursor.fetchall()
        for row in record:
            print("id = ", row[0], )
            print("name = ", row[1])
            image = row[2]
            print("Storing employee image and bio-data on disk \n")
            write_file(image, image)

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


readBLOB(1, r"C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\html.JPG")
readBLOB(2, r"C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\css.JPG")
# readBLOB(3, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\ruby.JPG")
# readBLOB(4, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\python.JPG")
# readBLOB(5, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\sql.JPG")
# readBLOB(6, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\js.JPG")
# readBLOB(7, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\java.JPG")
# readBLOB(8, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\c.JPG")
# readBLOB(9, "C:\Users\User\Desktop\Dojo_Assignements\Projects & Algorithms\Solo Project\flask_app\static\images\go.JPG")
