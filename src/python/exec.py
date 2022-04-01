import pickle
import json
import nltk.classify.util
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def word_feature(words):
    useful_words = [lm.lemmatize(st.stem(word)) for word in words if word not in stop_words]
    my_dict= dict([(word, True) for word in useful_words])
    return my_dict

def remove_mentions_hastaghs(text):
    pattern = r'[0-9]'
    text = text.lower()
    text = re.sub(pattern, '', text)
    text = text.replace('â™¥', 'heartemoticon')
    final = ' '.join(word for word in text.split(' ') if not word.startswith('@') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('#') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('www') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('http') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('ð') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('ñ') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('î') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('å') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('ã') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('â') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('è') )
    final = ' '.join(word for word in final.split(' ') if not word.startswith('zã') )
    final = ' '.join(word for word in final.split(' ') if not word.isdigit())
    final = ' '.join(word for word in final.split(' ') if word.isalnum() )
    return final

def load_file():
    fileObject = open("data_source.json", encoding="utf-8")
    return json.load(fileObject)

def load_pickle():
    f = open('my_new_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier

def main():
    fileObject = load_file()
    classifier = load_pickle()

    for data in fileObject:
        data['full_text'] = remove_mentions_hastaghs(data['full_text'])

    negative_score = 0
    positive_score = 0
    vectorizer = pickle.load(open('K_Vectorizer.sav', 'rb'))
    model = pickle.load(open('K_SVM_classifier.sav', 'rb'))


    for data in fileObject:
        text = data['full_text']
        word = word_feature(word_tokenize(text))

        #testing
        text_vector = vectorizer.transform([text])
        result = model.predict(text_vector)
        predicted_score = model.predict_proba(text_vector)[0]
        neg_score = predicted_score[0] * 100
        pos_score = predicted_score[1] * 100
        if(neg_score > 75):
            data['category'] = 'Negative'
        elif(pos_score > 75):
            data['category'] = 'Positive'
        else:
            data['category'] = 'Neutral'
        ####
        #if(classifier.classify(word) == 'Negative'):
        #    negative_score = negative_score + 1
        #    data['category'] = 'Negative'
        #else:
        #    positive_score = positive_score + 1
        #    data['category'] = 'Positive'
            
    with open('result_data.json', 'w') as outfile:
        json.dump(fileObject, outfile)
    print('Finish')

if __name__ == '__main__':
    st = nltk.PorterStemmer()
    lm = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    new_stop_words = {"rt", "i'd", "isn't", 'gt', 'nt', 'amp'}
    stop_words = set.union(stop_words,new_stop_words)
    main()
