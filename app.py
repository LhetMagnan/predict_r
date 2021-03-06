import flask
import pickle
import re
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import load_model 

model = load_model("model/network_1.h5") 
# loading
with open('model/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

app = flask.Flask(__name__, template_folder='templates')
@app.route('/', methods=['GET', 'POST'])
def main():

    SEQUENCE_LENGTH = 29 

    def preprocess_text(sen):
        sentence = remove_tags(sen)
        sentence = re.sub('[^a-zA-Z]', ' ', str(sentence))
        sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', str(sentence))
        sentence = re.sub(r'\s+', ' ', str(sentence))

        return sentence
        
    TAG_RE = re.compile(r'<[^>]+>')
    def remove_tags(text):
        return TAG_RE.sub('', str(text))

    # def get_predictions(text):
    #     text = preprocess_text(text)
    #     sequence = tokenizer.texts_to_sequences([text])
    #     # pad the sequence
    #     sequence =  pad_sequences(sequence, padding='post', maxlen=SEQUENCE_LENGTH)

    #     # # get the prediction
    #     # prediction = model.predict(sequence)[0]
    #     # pred = list(prediction)
    #     # # one-hot encoded vector, revert using np.argmax
    #     # Test_Text = preprocess_text(Test_Text)
    #     # Test_Text = tok.texts_to_sequences([Test_Text])
    #     # Test_Text =  pad_sequences(Test_Text, padding='post', maxlen=max_length)

    #     # return  np.argmax(model.predict(sequence))

    #     return model.predict(sequence)[0][0],model.predict(sequence)[0][1],model.predict(sequence)[0][2]



        # return pred.indenp.argmax(list(prediction)))


    if flask.request.method == 'GET':
        return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        message = flask.request.form['message']
        text = preprocess_text(message)
        sequence = tokenizer.texts_to_sequences([text])
        # pad the sequence
        sequence =  pad_sequences(sequence, padding='post', maxlen=SEQUENCE_LENGTH)


        



        # prediction = np.argmax(model.predict(sequence))
        prediction = sequence[0][0],sequence[0][1],sequence[0][2],sequence[0][3],sequence[0][4]
        seriousness = ""
        if(prediction == 0):
            seriousness = "Our Model can't decide if this is relevant or not " 
        
        elif(prediction == 1):
            seriousness = "This tweet is not relevant to a disaster"

        else:
            seriousness = "This tweet is relevant to a disaster, you should consider investigating"

        return flask.render_template('main.html',
        original_input={
            "message":message,
                                                        
        },
                                        result=prediction

                                        )

if __name__ == '__main__':
    app.run()
