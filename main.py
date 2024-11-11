# Name: Chris Torrey
# Project: neetTutor
# Last Edited Date: 11/10/2024

### Included Libraries ###
from transformers import pipeline;
#from transformers import AutoModelWithLMHead, AutoTokenizer;
from transformers import logging;
import os;
import wikipediaapi; # Using this as our PoC information for gathering the context page

### "Macro" Defintiions ###
NUM_OF_RESPONSES = 5
MAX_RESPONSE_LEN = 128

# This should supress the excess levels of warnings pytorch spits out
logging.set_verbosity_error(); 

wiki = wikipediaapi.Wikipedia("neetTutor (cwtorrey@mtu.edu)", "en")

def toCamelCase(string):
    words = string.replace('\ ', "").replace('-', "").replace('_', "").split();

    return words[0].lower() + "".join(word.capitalize() for word in words[1:]);

def getSimpleContext(conceptName):
    page = wiki.page(conceptName);

    if page.exists():
        return page.summary
    else:
        return "No context found!"

def fillContextPages(rootDir, concept):
    for subdir, dirs, files in os.walk(rootDir):
        dirName = os.path.basename(subdir);
        
        # print("dirName = ", dirName);
        # print("conceptName = ", toCamelCase(concept));

        if "context.txt" in files and dirName == toCamelCase(concept):
            filePath = os.path.join(subdir, "context.txt");
           
            with open(filePath, 'w') as file:
                context = getSimpleContext(concept);
                file.write(context +"\n\n");

generator = pipeline("text2text-generation", model="valhalla/t5-base-e2e-qg")

# Going to read an entire file in as context for the question generation...
# Eventually this will need to be changed to utilze the resources mined(?) for
# information

Concepts = ["Merge Sort", "Selection Sort", "Quick Sort", "Insertion Sort", "Bubble Sort"];

rootDirectory = "RAG/algorithims/sorting/comparisonBased/";

filename = "context.txt";

for concept in Concepts:
    fillContextPages(rootDirectory, concept);

j = 0;
for subdir, dirs, files in os.walk(rootDirectory):
    if filename in files:
        filePath = os.path.join(subdir, filename);

        with open(filePath, 'r') as file:
            context = file.read();

        outputs = generator(
                  context,
                  max_length=MAX_RESPONSE_LEN,
                  num_return_sequences=NUM_OF_RESPONSES,
                  do_sample=True,
                  );

        ### Outputs ###
        print("");
        print(Concepts[j]);
        for i in range(NUM_OF_RESPONSES):
            print("\nResponse ", i+1, ":");
            genText = outputs[i]['generated_text'].replace("<sep>", "").strip();

            genQuestions = [question.strip() + '?' for question in genText.split('?')
                    if question.strip()];

            print("\n".join(genQuestions));

        print("")
        j += 1;

