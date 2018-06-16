# export FLASK_APP=green_layer.py
# flask run --host=0.0.0.0
#flask run --host=127.0.0.1

#navigation buttons
#add cols
#del cols
#edit row data
#search
#hardcoded host, user, password


from flask import Flask
from flask import render_template
from flask import request
import re
import accounts_control
import word_stats

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/account-control", methods=['POST', 'GET'])
def database():

    if request.method == 'POST':
        if 'add' in request.form:
            status = accounts_control.create_account(request.form['type'], request.form['email'], request.form['user'], request.form['password'], request.form['vertical'],
                                    request.form['first_name'], request.form['last_name'], request.form['notes'])
        if 'delete' in request.form:
            pass
            """
                Code to remove user here
            """

    delete_db_form1 = ""
    delete_db_form2 = ""
    #delete_db_form1 = '<form action="/database" method="post" style="display: inline;"><input type="hidden" name="delete" value="'
    #delete_db_form2 = '"><input type="image" src="static/delete.png" alt="Submit"></form>'

    create_table_form1 = ""
    create_table_form1 = create_table_form1 + '<table><tr><td>Type</td><td>Email</td><td>User</td><td>Password</td><td>Vertical</td><td>First Name</td><td>Last Name</td><td>Notes</td><tr><tr>'
    create_table_form1 += '<form action="/account-control" method="post" style="display: inline;">'
    create_table_form1 += '<input type="hidden" name="add" value="">'
    create_table_form1 += '<td><input type="text" name="type"></td>'
    create_table_form1 += '<td><input type="text" name="email"></td>'
    create_table_form1 += '<td><input type="text" name="user"></td>'
    create_table_form1 += '<td><input type="text" name="password"></td>'
    create_table_form1 += '<td><input type="text" name="vertical"></td>'
    create_table_form1 += '<td><input type="text" name="first_name"></td>'
    create_table_form1 += '<td><input type="text" name="last_name"></td>'
    create_table_form1 += '<td><input type="text" name="notes"></td>'
    create_table_form1 += '<td><input type="image" src="static/menu.png" alt="Submit"></td></form></tr></table>'

    account_list = accounts_control.accounts_by_vertical()

    ac = ""
    ac = ac + create_table_form1
    for i in account_list[1]:
        ac = ac + "<table>"
        ac = ac + '<th>' + i + '</th>'
        for n in account_list[1][i]:
            ac = ac + "<tr>"
            first = 0
            for j in n:
                if first > 0:
                    ac = ac + "<td>" + str(j) + "</td>"
                first = 1

            ac = ac + "</tr>"
        ac = ac + "</table><br><br>"

    return render_template('account-control.html', ac=ac)

@app.route("/site-stats", methods=['POST', 'GET'])
def site_stats():
    page_data = ""

    if request.method == 'POST':
        if 'update' in request.form:
            output = word_stats.report1()
            print output
            page_data = page_data + output


    page_data = page_data + '<form action="/site-stats" method="post"><input type="hidden" name="update" value=""><input type="image" src="static/menu.png" alt="Submit"></td></form>'
    return render_template('site-stats.html', page_data=page_data)


if __name__ == "__main__":
    app.run()


















