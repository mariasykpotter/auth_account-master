import auth

authenticator = auth.Authenticator()

while True:

    commands_list = ['CREATE-SUPERUSER',
                     'CREATE-USER',
                     'LOGIN',
                     'LOGOUT']

    for i in commands_list:
        print(i)

    x = input('Please, enter command from list above: ').upper()

    if x == 'CREATE-SUPERUSER':
        if not authenticator.check_root():
            name = input('Create SUPERUSER login: ')
            passw = input('Create SUPERUSER password: ')
            superuser = True
            authenticator.add_user(name, passw, superuser)
        else:
            print('Superuser role is already exists')

    if x == 'CREATE-USER':
        name = input('Please enter SUPERUSER login: ')
        passw = input('Please enter SUPERUSER password: ')
        if authenticator.root[name].check_password(passw):
            name = input('Please enter user\'s login: ')
            if name in authenticator.users:
                print('User already exists! Please try again.')
            passw = input('Please enter user\'s password: ')
            authenticator.add_user(name, passw)
            print('User {} was created!'.format(name))

    if x == 'LOGIN':
        name = input('Login: ')
        if authenticator.is_logged_in(name):
            print('User {} already logged in.')
        else:
            passw = input('Password: ')
            authenticator.login(name, passw)
            print('You\'re login sucessful!')

    if x == 'LOGOUT':
        name = input('Login: ')
        authenticator.logout(name)