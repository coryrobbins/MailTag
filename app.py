"""from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    # Load the CSV file into a Pandas dataframe
    df = pd.read_csv('email_body.csv')

    # Get the next email to label
    email = get_next_email(df)

    # If there are no more emails to label, return a message
    if email is None:
        return 'No emails to label'

    # Render the template with the email and the labels
    return render_template('index.html', email=email, labels=['Label 1', 'Label 2', 'Label 3', 'Label 4', 'Label 5', 'Label 6', 'Label 7'])

@app.route('/label', methods=['POST'])
def label():
    # Load the CSV file into a Pandas dataframe
    df = pd.read_csv('emails.csv')

    # Get the label from the form data
    label = request.form['label']

    # Get the index of the email to label
    index = get_next_email_index(df)

    # Update the label in the dataframe
    df.loc[index, 'label'] = label

    # Save the dataframe back to the CSV file
    df.to_csv('emails.csv', index=False)

    # Redirect back to the index page to show the next email
    return redirect(url_for('index'))

def get_next_email(df):
    # Find the first email that hasn't been labeled yet
    email = df.loc[df['label'].isna(), 'body'].iloc[0]

    return email

def get_next_email_index(df):
    # Find the index of the first email that hasn't been labeled yet
    index = df.loc[df['label'].isna(), 'body'].index[0]

    return index

if __name__ == '__main__':
    app.run(debug=True)
    """
from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
#import pdb; pdb.set_trace()

app = Flask(__name__)
labels = ['Label 1','Label 2','Label 3', 'Label 4', 
          'Label 5', 'Label 6','Label 7', 'Label 8',
          'Label 9', 'Label 10','Label 11', 'Label 12',
          'Label 13', 'Label 14','Non-Technical'
          ]

def load_dataframe():
    df = pd.read_csv('email_body.csv')
    return df

def get_email_by_index(df, index):
    email = df.loc[df.index == index, 'body'].iloc[0]
    return email

def get_previous_email_index(df, index):
    previous_index = df.index[df.index < index][-1]if df.index[df.index < index].size > 0 else index
    return previous_index

@app.route('/')
@app.route('/index/<int:index>')
def index(index=None):
    df = load_dataframe()
    if index is None:
        index = get_next_email_index(df, -1)
    if index is None:
        return "No more emails to label."
    email = get_email_by_index(df, index)
    assigned_label = df.loc[index, 'label']
    if pd.isna(assigned_label):
        assigned_label = 'Not Assigned'
    return render_template("index.html", email=email, labels=labels, assigned_index=index, assigned_label=assigned_label)

def get_next_email_index(df, index):
        if df.empty: 
            return None
        next_index = df.index[df.index > index] 
        if next_index.empty:
            return None
        return next_index[0]
    
@app.route('/label', methods=['POST'])
def label():
    df = load_dataframe()
    index = request.form.get('index', 0)
    index = int(index)
    print(f"Index: {index}")
    if 'label' in request.form:
        label = request.form['label'].strip()
        if label in labels:
            print(f"Index: {index}")
            df.loc[index, 'label'] = label
            df.to_csv('emails.csv', index=False)
            next_index = get_next_email_index(df, index)
            print(f"Next Index: {next_index}")
            return redirect(url_for('index', index=next_index))
    elif 'next_email' in request.form:
        next_index = get_next_email_index(df, index)
        print(f"Next Index: {next_index}")
        return redirect(url_for('index', index=next_index))

    elif 'previous_email' in request.form:
        previous_index = get_previous_email_index(df, index)
        print(f"Previous Index: {previous_index}")
        return redirect(url_for('index', index=previous_index))
    return redirect(url_for('index', index=index))

if __name__ == '__main__':
    app.run(debug=True)
