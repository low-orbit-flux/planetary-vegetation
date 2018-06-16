import sys
import os
sys.path.append(os.path.abspath("/storage1/PROJECT_Terbium"))
import boulder_valley    


#account_types = 'yahoo', 'google', 'twitter', 'tumblr', 'pinterest', 'facebook', 'reddit', 'imgur', 'stumble-upon', 'linkedin'
account_types = ['twitter', 'tumblr', 'pinterest', 'facebook', 'google', 'reddit', 'other']
account_types_not_other = ['twitter', 'tumblr', 'pinterest', 'facebook', 'google', 'reddit']


def create_account(account_type, email, user, password, vertical, first_name, last_name, notes):
    """
        Everything here needs to be reworked
            The fields for each network might be different someday...
            Also each table maps to a different metrics table which has different fields....
    """


    """
    Use these definitions below
    """
    account_type_field = ('varchar', account_type)
    if account_type in account_types_not_other:
        account_type_table = account_type+ '_accounts'
    else:
        account_type_table = 'other_accounts'

    email_d = ('varchar', email)
    user_d = ('varchar', user)
    password_d = ('varchar', password)
    vertical_d = ('int', vertical)
    first_name_d = ('varchar', first_name)
    last_name_d = ('varchar', last_name)


    """
    creates tables - disable for now
    do something with this 
    """
    status1 = ""
    #status1 = boulder_valley.my_crud.create_table("127.0.0.1", "root", "xxxxxxxxxx", "campaigns", account_type + '_accounts',
    #                                              (('varchar', 'email'), ('varchar', 'user'), ('varchar', 'password'), ('int', 'vertical'), ('varchar', 'first_name'), ('varchar', 'last_name'), ('varchar', 'notes')))

    params = [account_type_field, ('varchar', email), ('varchar', user), ('varchar', password), ('int', vertical), ('varchar', first_name), ('varchar', last_name), ('varchar', notes)]
    status2 = boulder_valley.my_crud.insert_data("127.0.0.1", "root", "xxxxxxxxxx", "campaigns", account_type_table, params)
    return status1, status2


def accounts_by_type():
    results = ""
    for account_type in account_types:
        output = boulder_valley.my_crud.print_all("127.0.0.1", "root", "xxxxxxxxxx", "campaigns", account_type + '_accounts')
        results = results + "\n\n==========| " + account_type + "|==========\n"
        for i in output:
            results = results + str(i) + "\n"
    return results


def accounts_by_vertical():
    """
    return: text results, list results 
    """
    results = ""
    results2 = {}
    output = boulder_valley.my_crud.print_all("127.0.0.1", "root", "xxxxxxxxxx", "campaigns", "verticals")
    for v in output:
        results = results + "\n\n==========| " + v[1] + "|==========\n"
        data23 = {'vertical': ('int', str(v[0])), }
        results_temp = []
        for account_type in account_types:
            output2 = boulder_valley.my_crud.search("127.0.0.1", "root", "xxxxxxxxxx", "campaigns", account_type + '_accounts', data23)
            if output2:
                for z in output2:
                    results = results + str(z) + "\n"
                    results_temp.append(z)
        results2[v[1]] = results_temp
    return results, results2






if __name__ == "__main__":
    output1 = accounts_by_vertical()
    #output2 = accounts_by_type()
    print output1[1]
    for i in output1[1]:
        print i
        for x in output1[1][i]:
            print x







