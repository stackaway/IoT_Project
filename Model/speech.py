import csv
import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()

# Open the CSV file
with open('/Users/churnika/Desktop/Projects/IoT_Project/Dataset/speech_to_text.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    # Start an infinite loop
    while True:
        # Reading Microphone as source
        # listening the speech and store in audio_text variable
        with sr.Microphone() as source:
            print("Talk")
            audio_text = r.listen(source, timeout=10, phrase_time_limit=10)
            print("Time over, thanks")

        # recognize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            text = r.recognize_google(audio_text)
            print("Text: " + text)

            # writing to csv file
            writer.writerow([text])

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

        except KeyboardInterrupt:
            print("Interrupted by user")
            break

        except Exception as e:
            print("An error occurred: {0}".format(e))

    # Close the CSV file
    file.close()
