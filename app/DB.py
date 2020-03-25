import pymysql
import hashlib


def ins(con, subj, date, file_name, uploader_nick, tags):
    with con:
        query = 'insert into files(subject, date, file_name, uploader_nick, tags) values("' + subj + '", "' + date + '", "'+ file_name + '", "' + uploader_nick +'", "' + tags + '");'
        print(query)
        cur = con.cursor()
        cur.execute(query)


def get(con, args):
    with con:
        if args['subject'] == 'all' and args['date'] == 'all':
            query = 'select * from files;'
        elif args['subject'] != 'all' and args['date'] == 'all':
            query = 'select * from files where subject = ' + '"' + args['subject'] + '"' + ';'
        elif args['subject'] == 'all' and args['date'] != 'all':
            query = 'select * from files where date = ' + '"' + args['date'] + '"' + ';'
        else:
            query = 'select * from files where date = ' + '"' + args['date'] + '"' + 'and subject = "' + args[
                'subject'] + '"' + ';'
        cur = con.cursor()
        cur.execute(query)

        return cur.fetchall()


def check_username(con, username):  # Возвращает True если такой пользователь уже зарегестрирован
    with con:
        cur = con.cursor()
        query = 'select * from users where nick = ' + '"' + username + '";'
        cur.execute(query)
        lst = cur.fetchall()
        return len(lst) > 0


def register(con, args):
    with con:
        cur = con.cursor()
        hash_pass = hashlib.md5(args['pass'].encode())
        query = 'insert into users(nick, pass) values(' + '"' + args['name'] + '", "' + hash_pass.hexdigest() + '");'
        cur.execute(query)


def sign(con, args):
    with con:
        cur = con.cursor()
        hash_pass = hashlib.md5(args['pass'].encode()).hexdigest()
        query = 'select * from users where nick = ' + '"' + args['name'] + '" and pass = ' + '"' + hash_pass + '";'
        cur.execute(query)
        lst = cur.fetchall()
        return len(lst) > 0


def insert_cookie(con, args):
    with con:
        cur = con.cursor()
        query = 'update users set hash = "' + args['cookie'] + '" where nick = "' + args['name'] + '";'
        cur.execute(query)


def check_cookie(con, args):
    with con:
        cur = con.cursor()
        query = 'select * from users where name = "' + args['name'] + '";'
        cur.execute(query)
        lst = cur.fetchall()
        return args['hash'] == lst[3]


def extended_search(con, args):
    with con:
        cur = con.cursor()
        query = 'select * from files where '
        if args['subject'] and not args['subject'] == 'Выберите предмет':
            query += 'subject = ' + '"' + args['subject'] + '" '
        else:
            query += 'not subject = "asdjoas" '
        if args['date']:
            query += 'and date = ' + '"' + args['date'] + '" '
        if args['uploader_nick']:
            query += 'and uploader_nick = ' + '"' + args['uploader_nick'] + '" '
        query += ';'

        print(query)
        cur.execute(query)

        lst = list(cur.fetchall())
        for i in range(len(lst)):
            lst[i] = list(lst[i])
        print(lst)
        for i in range(len(lst)):
            if lst[i][5]:
                lst[i][5] = lst[i][5].replace(' ', '').split(',')
        if args['tags']:
            ans = []
            for i in range(len(lst)):
                if lst[i][5]:
                    for tag in lst[i][5]:
                        for search_tag in args['tags']:
                            if search_tag == tag:
                                ans.append(lst[i])
                                break
            print(ans)
            return ans
        else:
            return lst





