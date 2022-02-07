from nudenet.classifier import Classifier
from math import dist

FUZZY="fuzzy"
SAFE="safe"
UNSAFE="unsafe"

classifier = Classifier()

def classify(filepath: str, precision=0.3):
    result = classifier.classify(filepath)[filepath]
    safe = result["safe"]
    unsafe = result["unsafe"]
    if (dist([safe], [unsafe]) < precision):
        return FUZZY
    elif (safe > unsafe):
        return SAFE
    else:
        return UNSAFE


if __name__ == "__main__":
    print(classify('test/one.jpg'))
    print(classify('test/onecrop.jpg'))
    print(classify('test/one1000.jpg'))
    print(classify('test/one.webp'))
    print(classify('test/two.jpeg'))