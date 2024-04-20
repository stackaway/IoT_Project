from dotenv import load_dotenv
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib
from collections import Counter
from keras.models import load_model
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import nltk
import pandas as pd

test_document = r'C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[E1TA2] ECE352\IoT_Project\Speech\Dataset\output.csv'

# Try to read the CSV file without headers
try:
    test_doc = pd.read_csv(test_document, header=None)
except pd.errors.EmptyDataError:
    print(f"No data in {test_document}")
    test_doc = pd.DataFrame()

# If the DataFrame is not empty, rename the column and convert to lowercase
if not test_doc.empty:
    test_doc.columns = ['text']
    test_doc['text'] = test_doc['text'].str.lower()
else:
    print("The DataFrame is empty.")

# If you haven't downloaded the tokenizer package, uncomment the line below to download
# nltk.download('punkt')


def tokenize_text(text):
    return nltk.word_tokenize(text)


# Apply the function to the 'text' column
if not test_doc.empty:
    test_doc['tokenized_text'] = test_doc['text'].apply(tokenize_text)
else:
    print("The DataFrame is empty.")


# Create a tokenizer
tokenizer = Tokenizer()

# Fit the tokenizer on the text
# This will create the vocabulary
if not test_doc.empty:
    tokenizer.fit_on_texts(test_doc['tokenized_text'].tolist())

# Convert the tokens into integers
test_doc['encoded_text'] = test_doc['tokenized_text'].apply(lambda x: tokenizer.texts_to_sequences([x])[0])

print(test_doc['encoded_text'])


# Pad the sequences
# This will make all sequences the same length
if not test_doc.empty:
    test_doc['padded_text'] = pad_sequences(test_doc['encoded_text'].tolist()).tolist()

print(test_doc['padded_text'])


# Load the pre-trained model
# model = load_model('my_model.h5')
model = load_model(r'Speech\Model\my_model.h5')

# Convert the 'padded_text' column to a numpy array
X = np.array(test_doc['padded_text'].tolist())

# Use the model to make predictions
predictions = model.predict(X)

print(predictions)

# Define a dictionary to map indices to class names
index_to_class = {
    0: 'sad',
    1: 'happy',
    2: 'love',
    3: 'anger',
    4: 'fear'
}

# Find the index of the maximum probability for each sequence
max_indices = np.argmax(predictions, axis=1)

# Map the indices to class names
predicted_classes = [index_to_class[index] for index in max_indices]

print(predicted_classes)


# Count the occurrences of each class
counter = Counter(predicted_classes)

# Find the class with the highest count
overall_class = counter.most_common(1)[0][0]

print(overall_class)


load_dotenv()
# Check if the overall class is 'sadness'
# Email settings
subject = "Emotional Diagnosis of Patient"
body = "The patient is predicted to be feeling " + overall_class + ". Please find the attached CSV file for more details on your patient."
sender_email = os.getenv("SENDER")
receiver_email = os.getenv("RECEIVER")
password = os.getenv("PASSWORD")
filename = r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[E1TA2] ECE352\IoT_Project\Speech\Dataset\output.csv"
# Create a multipart message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = subject
# Add the email body
msg.attach(MIMEText(body, "plain"))
# Open the file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-streamm
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
# Encode file in ASCII characters to send by email
encoders.encode_base64(part)
# Add header as pdf attachment
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)
# Add attachment to message and convert message to string
msg.attach(part)
text = msg.as_string()
# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
