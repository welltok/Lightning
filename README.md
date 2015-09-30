Welcome to the Lightning project!!!

Contributors : Max, Laksh, Vin

This project tracks all works associated with Watson Natural Language Classifier (NLC). Here's a layout of the repository:

root
 - Python (All Python Modules and Projects)
 - Scripts (ANT, Maven or other scripts)
 - Resources (Resource files for training and testing purposes)
    - Training
    - Tests
 - Java (All Java sources)
 - Web (All Web resources)

For Python Modules

Step 1 : Use python/Extract.py to convert ground truth snapshot into CSVs

Step 2 : Use python/split.py to split train and test set

Step 3 : Use python/nlc.py to train NLC using the train set

Step 4 : Use python/test.py to test NLC using the test set

Have fun!!! 
