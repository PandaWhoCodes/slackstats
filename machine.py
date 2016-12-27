from textblob.classifiers import NaiveBayesClassifier
train = [
    ('Will call you', 'pos'),
    ('Meet me tomorrow', 'pos'),
    ('Lets meet up', 'pos'),
    ('I\'ll send it tomorrow','pos'),
    ('Ill send it to you tomorrow', 'neg'),
    ('Will be at NHR today around 11:30 am', 'neg'),
    ('That is fine. They will take only about an hour each, right?', 'neg'),
    ('or should I ask both of them to come around', 'neg'),
    ('Used to have it. Kind of expensive. But worth getting one if the free tools don\'t measure up.', 'neg'),
    ('At what time should I ask the selected intern candidates to come.', 'neg'),
    ('Yes it would be good to have a wiki. Media wiki is quite good. I have not tried out any of the slack wikis', 'neg'),
    ('there was some issue with the app at my end and after the see you at 2 pm yesterday message...nothing else here...is that right?', 'neg'),
    ("Want to talk about the next beta release", 'pos'),
    ("http://www.", 'neg'),
     ("http://", 'neg'),
    ("https://", 'neg'),
    ("https://www.", 'neg')]
cl = NaiveBayesClassifier(train)
def main(text):
    if cl.classify(text)=="pos":
        return True
    else:
        return False
#print(main(input()))
