# echo id: 109916824143808156094
# me id: 116409851376712775898
# conversation id: UgzNJJex_T7iGSKjkL14AaABAagBsOOEBA

import csv, json, re
import collections
stopwords = ['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an', 'and', 'any', 'are', 'aren', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can',          'couldn', "couldn't", 'd', 'did', 'didn', "didn't", 'do', 'does', 'doesn', "doesn't", 'doing', 'don', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'hadn', "hadn't", 'has', 'hasn', "hasn't", 'have', 'haven', "haven't", 'having', 'he',                          'her', 'here',           'hers', 'herself', 'him', 'himself', 'his', 'how',          'i',                               'if', 'in', 'into', 'is', 'isn', "isn't", 'it', "it's", 'its', 'itself', 'just', 'll', 'm', 'ma', 'me', 'mightn', "mightn't", 'more', 'most', 'mustn', "mustn't", 'my', 'myself', 'needn', "needn't", 'no', 'nor', 'not', 'now', 'o', 'of', 'off', 'on', 'once', 'only', 'or', 'other',          'our', 'ours', 'ourselves', 'out', 'over', 'own', 're', 's', 'same', 'shan', "shan't", 'she',                    "she's", 'should', "should've", 'shouldn', "shouldn't", 'so', 'some', 'such', 't', 'than', 'that', "that'll",           'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there',            'these', 'they',                                            'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 've', 'very', 'was', 'wasn', "wasn't", 'we',                                    'were', 'weren', "weren't", 'what',           'when',           'where',            'which', 'while', 'who',          'whom', 'why', 'will',          'with', 'won', "won't",          'wouldn', "wouldn't", 'y', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves']
# remove punctuation
stopwords = list(map(lambda x: re.sub('[^a-z]', '', x), stopwords))


echo_id = '109916824143808156094'
alyssa_id = '116409851376712775898'

# store the words as a list
echo_words = []
alyssa_words = []
both_words = []

# loop through each file
files = ['Hangouts.json']

for f in files:

    # import the data file
    with open(f) as json_file:
        data = json.load(json_file)

    # go through each conversation element
    for conversation in data['conversations']:

        # if both ids are present
        people = conversation['conversation']['conversation']['participant_data']
        people = list(map(lambda x: x['id']['chat_id'], people))
        if echo_id in people and alyssa_id in people:

            # go through each event element
            for event in conversation['events']:

                # filter relevant messages only
                sender = event['sender_id']['chat_id']
                if sender == alyssa_id or sender == echo_id:

                    # get the messages, only text ones
                    if 'chat_message' in event.keys():
                        if 'segment' in event['chat_message']['message_content'].keys():
                            messages = event['chat_message']['message_content']['segment']
                            messages = list(filter(lambda x: 'text' in x.keys(), messages))
                            messages = list(map(lambda x: x['text'].split(), messages))

                            # process the messages
                            # flatten the list
                            messages = [item for sublist in messages for item in sublist]
                            # lowercase
                            messages = list(map(lambda x: x.lower(), messages))
                            # remove punctuation
                            messages = list(map(lambda x: re.sub('[^a-z]', '', x), messages))
                            # remove stopwords
                            messages = list(filter(lambda x: x not in stopwords, messages))

                        else:
                            continue
                    else:
                        continue

                    # put in appropriate list
                    both_words.extend(messages)
                    if sender == alyssa_id:
                        alyssa_words.extend(messages)
                    else:
                        echo_words.extend(messages)


# turn these into frequency dicts
both_words = collections.Counter(both_words)
alyssa_words = collections.Counter(alyssa_words)
echo_words = collections.Counter(echo_words)

# save to csv
with open('both_words.csv', mode='w+') as file:
    write_file = csv.writer(file, delimiter=';')
    for word in both_words.keys():
        write_file.writerow([word, both_words[word]])

with open('alyssa_words.csv', mode='w+') as file:
    write_file = csv.writer(file, delimiter=';')
    for word in alyssa_words.keys():
        write_file.writerow([word, alyssa_words[word]])

with open('echo_words.csv', mode='w+') as file:
    write_file = csv.writer(file, delimiter=';')
    for word in echo_words.keys():
        write_file.writerow([word, echo_words[word]])
