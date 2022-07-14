from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xyz'



@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

T_Ques = ''
student_ans = ''

total_grade = 0
avg=0
curr_grade =0

TName = ''
SName = ''
AName = ''

total_q = list()
total_ans = list()

allGrades = list()

timer=0

need_help_opt =''
admin_hint =''

@app.route("/index", methods=['GET', 'POST'])
def Home():
    global TName
    global SName
    global AName

    if request.method == 'POST':
        Name = str(request.form['Name'])
        select = request.form['select']

        if select =='Teacher':
            TName=Name
            return redirect(url_for('Teacher'))

        if select=='Student':
            SName=Name
            return redirect(url_for('Student'))

        if select=='Admin':
            AName=Name
            return redirect(url_for('admin',num=0))

    else:
      return render_template('index.html')


@app.route('/Teacher', methods=['POST','GET'])
def Teacher():

    global total_grade
    global avg
    global T_Ques
    global curr_grade

    if request.method == 'POST':
        if request.form['submit'] == 'task1':
            Q = str(request.form['Q'])
            T_Ques = Q
            total_q.append(T_Ques)

    if student_ans != '':
        if request.method == 'POST':
            if request.form['submit'] == 'task2':
                curr_grade = int(request.form['grade'])
                total_grade = total_grade + curr_grade
                allGrades.append(curr_grade)
                avg = total_grade / len(allGrades)

    return render_template('Teacher.html', Sname=SName, Tname=TName,
                                   student_ans=student_ans)

@app.route('/Student', methods=['POST','GET'])
def Student():
    global need_help_opt
    global student_ans

    if request.method == 'POST':

        if request.form['submit'] == 'task1':
                ans = str(request.form['ans'])
                student_ans = ans
                total_ans.append(student_ans)
        if request.form['submit'] == 'task2':
                    opt = request.form['opt']
                    need_help_opt = opt

    return render_template('Student.html', SName=SName, TName=TName,T_Ques=T_Ques,
                           curr_grade=curr_grade, total_grade=total_grade, avg=avg
                        )


@app.route('/Admin<int:num>', methods=['POST','GET'])
def admin(num):


    admin_infor =''

    admin_infor = zip(total_q,total_ans)
    return render_template('Admin.html',admin_infor=admin_infor,num=timer)

@app.route('/closeApp',methods=['POST','GET'])
def kill_app():
    global T_Ques
    global s_answer
    global total_grade
    global avg
    global curr_grade
    global TName
    global SName
    global AName
    global total_q
    global total_ans
    global allGrades
    global timer
    global admin_hint
    if request.method =='POST':
        kill = str(request.form['kill']).lower()
        if kill =='yes':
            T_Ques = ''
            s_answer = ''
            admin_hint =''
            total_grade = 0
            avg = 0
            curr_grade = 0
            timer =0

            TName = ''
            SName = ''
            AName = ''

            total_q = list()
            total_ans = list()
            allGrades = list()

            return render_template("index.html")
    return render_template("closeApp.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
