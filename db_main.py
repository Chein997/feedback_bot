import sqlite3

class BotDB:

    def __init__(self, db_file):
        self.conn=sqlite3.connect(db_file)
        self.cursor=self.conn.cursor()


    def words_exists(self,words):
        result = self.cursor.execute("SELECT `numbers` FROM `forb_words` WHERE `words` = ?", (words,))
        return (bool(len(result.fetchall())))

    def get_user_id(self, words):
        result = self.cursor.execute("SELECT `numbers` FROM `forb_words` WHERE `words` = ?", (words,))
        return result.fetchone()[0]

    def add_words(self, words):
        self.cursor.execute("INSERT INTO `forb_words` (`words`) VALUES (?)", (words,))
        return self.conn.commit()

    def add_id(self, id):
        self.cursor.execute("INSERT INTO `forb_words` (`id`) VALUES (?)", (id,))
        return self.conn.commit()

    def get_words(self):
        self.cursor.execute("SELECT * FROM forb_words")
        result = self.cursor.fetchall()
        return result


def close(self):
    self.connection.close()