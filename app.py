import pickle
from flask import Flask,render_template,request

app = Flask(__name__)
pickle_model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['GET','POST'])
def predict():
    return render_template('prediction.html')

@app.route('/process_input', methods = ['POST'])
def process_input():
    input1 = request.form['input1']
    input2 = request.form['input2']
    input3 = request.form['input3']
    input4 = request.form['input4']
    input5 = request.form['input5']
    input6 = request.form['input6']
    input7 = request.form['input7']
    input8 = request.form['input8']
    input9 = request.form['input9']
    input10 = request.form['input10']
    input11 = request.form['input11']
    input12 = request.form['input12']
    input13 = request.form['input13']
    raw_input = []
    raw_input.append(input1)
    raw_input.append(input2)
    raw_input.append(input3)
    raw_input.append(input4)
    raw_input.append(input5)
    raw_input.append(input6)
    raw_input.append(input7)
    raw_input.append(input8)
    raw_input.append(input9)
    raw_input.append(input10)
    raw_input.append(input11)
    raw_input.append(input12)
    raw_input.append(input13)
    single_input = []
    job_mapping = {'admin.': [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       'blue-collar': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       'entrepreneur': [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                       'housemaid': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                       'management': [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                       'retired': [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                       'self-employed': [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                       'services': [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                       'student': [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                       'technician': [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                       'unemployed': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                       'unknown': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]}

    marital_mapping = {'divorced': [1, 0, 0], 'married': [0, 1, 0], 'single': [0, 0, 1]}

    education_mapping = {'primary': [1, 0, 0, 0], 'secondary': [0, 1, 0, 0], 'tertiary': [0, 0, 1, 0],
                             'unknown': [0, 0, 0, 1]}

    contact_mapping = {'cellular': [1, 0, 0], 'telephone': [0, 1, 0], 'unknown': [0, 0, 1]}

    poutcome_mapping = {'failure': [1, 0, 0, 0], 'other': [0, 1, 0, 0], 'success': [0, 0, 1, 0],
                            'unknown': [0, 0, 0, 1]}

    age_mapping = {'18-25': [1, 0, 0, 0, 0, 0, 0, 0], '26-35': [0, 1, 0, 0, 0, 0, 0, 0],'36-45': [0, 0, 1, 0, 0, 0, 0, 0], '46-55': [0, 0, 0, 1, 0, 0, 0, 0],
                    '56-65': [0, 0, 0, 0, 1, 0, 0, 0], '66-75': [0, 0, 0, 0, 0, 1, 0, 0],
                    '76-85': [0, 0, 0, 0, 0, 0, 1, 0], '86-95': [0, 0, 0, 0, 0, 0, 0, 1]}

    for i in range(0, 7):
        single_input.append(raw_input[i])
    for i in range(7, 13):
        if raw_input[i] in ['management', 'technician', 'entrepreneur', 'blue-collar','unknown', 'retired', 'admin.', 'services', 'self-employed','unemployed', 'housemaid', 'student']:
            one_hot_input = job_mapping[raw_input[i]]
            for j in one_hot_input:
                single_input.append(j)
        elif raw_input[i] in ['married', 'single', 'divorced']:
            one_hot_input = marital_mapping[raw_input[i]]
            for j in one_hot_input:
                single_input.append(j)
        elif raw_input[i] in ['tertiary', 'secondary', 'unknown', 'primary']:
            one_hot_input = education_mapping[raw_input[i]]
            for j in one_hot_input:
                single_input.append(j)
        elif raw_input[i] in ['unknown', 'cellular', 'telephone']:
            one_hot_input = contact_mapping[raw_input[i]]
            for j in one_hot_input:
                single_input.append(j)
        elif raw_input[i] in ['unknown', 'failure', 'other', 'success']:
            one_hot_input = poutcome_mapping[raw_input[i]]
            for j in one_hot_input:
                single_input.append(j)
        elif raw_input[i] in ['56-65', '36-45', '26-35', '46-55', '18-25', '66-75', '76-85','86-95']:
            one_hot_input = age_mapping[raw_input[i]]
            for j in one_hot_input:
                single_input.append(j)

    if pickle_model.predict([list(single_input)]) == 1:
        result = "Higher chance for buy"
    elif pickle_model.predict([list(single_input)]) == 0:
        result = "Lesser chance for buy"

    return render_template('prediction.html',result=result)


if __name__ == '__main__':
    app.run(debug=True,port=4343)