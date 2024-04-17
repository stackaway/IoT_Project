import streamlit as st
import csv
import os
import time
import speech_recognition as sr

# Function to start speech recognition process


def start_speech_recognition(stop_flag):
    # Define the directory path where the file will be saved
    directory = r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[E1TA2] ECE352\IoT_Project\Speech\Dataset"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a unique filename based on the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    csv_filename = os.path.join(directory, f"output.csv")

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Open the CSV file
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Start an infinite loop
        while not stop_flag:
            # Reading Microphone as source
            # listening the speech and store in audio_text variable
            with sr.Microphone() as source:
                print("Talk")
                st.write("Talk")
                # Listen for up to 10 seconds of speech
                audio_text = r.listen(source, timeout=10, phrase_time_limit=10)
                print("Time over, thanks")
                st.write("Time over, thanks")

            # recognize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
                # using google speech recognition
                text = r.recognize_google(audio_text)
                print("Text: " + text)
                st.write(text)

                # writing to csv filex
                writer.writerow([text])
                # Flush the buffer to ensure data is written immediately
                file.flush()

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                st.write("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                st.write("Could not request results from Google Speech Recognition service; {0}".format(e))

            except sr.WaitTimeoutError as e:
                print("listening timed out while waiting for phrase to start")

            except Exception as e:
                print("An error occurred: {0}".format(e))
                st.write("An error occurred: {0}".format(e))

    # Close the CSV file outside the loop
    file.close()

    # Print the path to the saved CSV file
    print("CSV file saved at:", csv_filename)

# Streamlit UI


if __name__ == "__main__":
    st.title("Speech Recognition")
    stop_flag = False
    if st.button("Stop Speech Recognition"):
        stop_flag = True
    start_speech_recognition(stop_flag)
