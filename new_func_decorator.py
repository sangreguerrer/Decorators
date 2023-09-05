from psycopg2 import connect
from config import host,user,password,db_name


try:
    connection=connect(
        host=host,
        user=user,
        password=password,
        database=db_name

    )
    with connection.cursor() as cursor:
        cursor.execute("SELECT users.name  from users "
                       "WHERE rights = 'Authorized'")
        connection.commit()
        authorized_rights = cursor.fetchall()
        cursor.execute("SELECT users.name  from users "
                       "WHERE rights = 'Guest'")
        guest_rights = cursor.fetchall()
        cursor.execute("SELECT users.name  from users "
                       "WHERE rights = 'Admin'")
        admin_rights = cursor.fetchall()

except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL",_ex)
permission=[admin_rights,guest_rights,authorized_rights]
def check_permission(status):
    def wrapper_permission(func):
        def check_wrapper():
            if status in permission:
                func()
                print(status)
            else:
                raise ValueError('Ошибка доступа')
        return check_wrapper
    return wrapper_permission




@check_permission(admin_rights)
def for_admin():
    print('Расширенные возможности')
@check_permission(guest_rights)
def for_guest():
    print('Только чтение')
@check_permission(admin_rights)
def for_authorized_users():
    print('Для авторизованных пользователей')

if __name__ == '__main__':
    for_admin()
    for_guest()
