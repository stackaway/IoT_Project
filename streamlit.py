# import streamlit as st
# import subprocess
# import threading

# # Function to start emotion recognition process


# def start_emotion_recognition():
#     subprocess.Popen(["python", "Emotion-detection/src/emotions_streamlit.py", "--mode", "display"])

# # Function to start speech recognition process


# def start_speech_recognition():
#     subprocess.Popen(["python", "Speech/Model/speech.py"])


# # Streamlit UI


# def main():
#     st.title("Emotion and Speech Recognition")

#     # Create buttons to start the processes
#     if st.button("Start Emotion Recognition"):
#         threading.Thread(target=start_emotion_recognition).start()

#     if st.button("Start Speech Recognition"):
#         threading.Thread(target=start_speech_recognition).start()


# if __name__ == "__main__":
#     main()

import streamlit as st
import subprocess
import threading

# Function to start emotion recognition process


def start_emotion_recognition():
    emotion_process = subprocess.Popen(["python", "Emotion-detection/src/emotions_streamlit.py", "--mode", "display"])

# Function to start speech recognition process


def start_speech_recognition():
    # global speech_process
    # speech_process = subprocess.Popen(["python", "Speech/Model/speech.py"])

    import csv
    import os
    import time
    import speech_recognition as sr

    # Define the directory path where the file will be saved
    directory = r"C:\Users\Jahnavi\Documents\3rd_Year\Y3S2\[E1TA2] ECE352\IoT_Project\Speech\Dataset"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a unique filename based on the current timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    csv_filename = os.path.join(directory, f"speech_to_text_{timestamp}.csv")

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    # Open the CSV file
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)

        # Start an infinite loop
        while True:
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

                # writing to csv file
                writer.writerow([text])
                # Flush the buffer to ensure data is written immediately
                file.flush()

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                st.write("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))
                st.write("Could not request results from Google Speech Recognition service; {0}".format(e))

            except KeyboardInterrupt:
                print("Interrupted by user")
                st.write("Interrupted by user")
                break

            except Exception as e:
                print("An error occurred: {0}".format(e))
                st.write("An error occurred: {0}".format(e))

    # Close the CSV file outside the loop
    file.close()

    # Print the path to the saved CSV file
    print("CSV file saved at:", csv_filename)


# Function to stop emotion recognition process


# Streamlit UI


def main():
    st.title("Emotion and Speech Recognition")

    # Create buttons to start the processes
    if st.button("Start Emotion Recognition"):
        threading.Thread(target=start_emotion_recognition).start()

    if st.button("Start Speech Recognition"):
        start_speech_recognition()


if __name__ == "__main__":
    main()
