import sqlite3


class SQLiteDatabase:

    # connect to db
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # get list of active watchers
    def get_users(self, status=True):
        with self.connection:
            sql = 'SELECT * FROM `users` WHERE `status` = ?'
            return self.cursor.execute(sql, (status,)).fetchall()

    # check if person exists in db
    def user_exists(self, user_id):
        with self.connection:
            sql = 'SELECT * FROM `users` WHERE `user_id` = ?'
            result = self.cursor.execute(sql, (user_id,)).fetchall()
            return bool(len(result))

    # add watcher (watching status)
    def add_user(self, user_id, status=True, my_path='text'):
        with self.connection:
            return self.cursor.execute('INSERT INTO `users` (`user_id`, `status`, `my_path`) VALUES(?,?,?)',
                                       (user_id, status, my_path))

    # update watching status and path
    def update_path(self, user_id, status, my_path):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `status` = ? ,
                          `my_path` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (status, my_path, user_id))

    # update testing status
    def update_status(self, user_id, status, checks_since_last=1, failures_since_last=1,
                      detect_failures=True, failure_mute=False):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `status` = ? ,
                          `checks_since_last` = ? ,
                          `failures_since_last` = ? ,
                          `detect_failures` = ? ,
                          `failure_mute` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (status, checks_since_last,
                                             failures_since_last, detect_failures,
                                             failure_mute, user_id))

    # setting notifications period
    def update_notifications_period(self, user_id, status, notifications_period=300):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `status` = ? ,
                          `notifications_period` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (status, notifications_period, user_id))

    # setting failure period
    def update_failures_period(self, user_id, status, failures_period=30):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `status` = ? ,
                          `failures_period` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (status, failures_period, user_id))

    # muting or unmuting failure notifications
    def update_mute(self, user_id, failure_mute):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `failure_mute` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (failure_mute, user_id))

    # if false, then only scheduled notifications
    def update_defects_detect(self, user_id, detect_failures):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `detect_failures` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (detect_failures, user_id))

    # updates the number of predictions
    def update_checks_since_last(self, user_id, checks_since_last):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `checks_since_last` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (checks_since_last, user_id))

    # updates the current number of defects detected
    def update_failures_since_last(self, user_id, failures_since_last):
        with self.connection:
            sql = ''' UPDATE `users`
                      SET `failures_since_last` = ?
                      WHERE `user_id` = ?'''
            return self.cursor.execute(sql, (failures_since_last, user_id))

    # get user path
    def get_user_path(self, user_id):
        with self.connection:
            sql = 'SELECT `my_path` FROM `users` WHERE `user_id` = ?'
            result = self.cursor.execute(sql, (user_id,)).fetchall()
            return result[0][0]

    # close db connection
    def close(self):
        self.connection.close()
