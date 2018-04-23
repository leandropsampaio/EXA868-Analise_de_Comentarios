import sqlite3
import re


class DatabaseController:

    def __init__(self):
        self.__connection = sqlite3.connect('../reviews_database.db')

        self.__connection.execute(
            'CREATE TABLE IF NOT EXISTS Reviews(review_id integer not null, comment varchar(250), rating real, PRIMARY KEY(review_id))')
        self.__connection.commit()

    def insert_reviews(self, review_list):
        for tuples in review_list:
            floater = 0.0

            if (type(tuples[0]) == type("String")):
                find = re.findall(r"[-+]?\d*,\d+|\d+", tuples[0])
                floater = float(find[0].replace(",", "."))
            elif (type(tuples[0]) == "float"):
                floater = float(tuples[0])

            self.__connection.execute("INSERT INTO Reviews(comment, rating) VALUES('%s', %f)" % (tuples[1], floater))
            self.__connection.commit()
