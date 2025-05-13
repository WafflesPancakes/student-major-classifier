import matplotlib.pyplot as plt
from matplotlib_venn import venn3

# Create a value to check if a proper file name was received.
completed = False

# Create SENTINEL value in case user wants to quit without a file.
SENTINEL = "QUIT" 

namesList = []

# Creates a dictionary that assigns the labels associated to each major.
usernamesMajorNum = {
    "Civil Engineering": "1",
    "Computer Engineering": "2",
    "Electrical Engineering": "3",
    "Mechanical Engineering": "4",
    "Other": "0"
}

# Creates a dictionary to store a count for each major
countOfMajors = {
    "Civil Engineering": 0,
    "Computer Engineering": 0,
    "Electrical Engineering": 0,
    "Mechanical Engineering": 0,
    "Other": 0
}

# Set variables for the keys of the dictionary countOfMajors
majorNamesGraph = list(usernamesMajorNum.keys())

# Creates a set for each major to later be able to compare them to each other (for venn diagram)
civilEngSet = set()
computerEngSet = set()
electricalEngSet = set()
mechanicalEngSet = set()

# Loops until completed
while not completed:
    requestFileName = input("Enter the name of the text file you want to open (including .txt): ")
    
    # If SENTINEL is received, breaks the loop.
    if requestFileName == SENTINEL:
        print("Quitting.")
        quit()

    print("Opening", requestFileName)

    # Checks to see if given file can be opened
    try:
        openFile = open(requestFileName, "r")
        print("File reading successful.")
        completed = True

    # Allows code to run in the event the file could not be found.
    except FileNotFoundError:
        print("Could not find the file, please try again or type 'QUIT' to quit.")

# Generates the outputFile that will be written to.
outputFileName = requestFileName.replace(".txt", "-out.txt")

# Iterates through each line of the file opened.
for line in openFile:
    searching = True
    listOfMajorNum = []

    # Checks for each " " space within the given string as it separates the names
    space = line.index(" ")

    # Grabs the first name up to the space character.
    firstName = line[0:space]

    # Searches for other names (i.e last names, middle names) beyond just the first name.
    while searching:

        # Iterates to the next space character
        nextSpace = line.index(" ", space + 1)

        # Stops searching for names once a semicolon indicates the separation of names and majors.
        if line[nextSpace - 1] == ";":
            break

        # Sets the nextName from the initial space to the next space character.
        nextName = line[space:nextSpace]

        # Adds the names together with spaces inbetween; "firstName nextName nextName...".
        firstName = firstName + nextName

        # sets the initial space as the nextSpace to iterate to next name.
        space = nextSpace
    
    # Checks for semicolon to separate majors within the .txt file
    firstSemiColon = line.index("; ")

    # Split everything after the semicolon by with " ; " to separate the majors into several substrings.
    majors = line[firstSemiColon + 2:].split(" ; ")

    # Creates a unique indentifier based on line number to ensure duplicate names are counted (mainly for venn diagram)
    UID = (firstName, line)

    # Iterates through the substring of majors.
    for i in majors:

        try:
            # Replaces each \n value within each major.
            temp = i.replace("\n", "")

            # Adds the student's uniqued identifier under each of their major's set.
            # Ex. "bob ; Mechanical Engineering ; Electrical Engineering"
            # will set bob to both mechE and electricalE sets.
            if temp == "Civil Engineering":
                civilEngSet.add(UID)
            elif temp == "Computer Engineering":
                computerEngSet.add(UID)
            elif temp == "Electrical Engineering":
                electricalEngSet.add(UID)
            elif temp == "Mechanical Engineering":
                mechanicalEngSet.add(UID)

            # Adds and creates the labels for the major to listOfMajorNum using the dictionary usernamesMajorNum.
            listOfMajorNum.append(usernamesMajorNum[temp])

            # Increases count of that major.
            countOfMajors[temp] += 1
        
        # In the case where a major that isn't in the dictionary is processed, instead categorize as "Other"
        except KeyError:
            listOfMajorNum.append(usernamesMajorNum["Other"])
            countOfMajors["Other"] += 1
    
    # Join all majors into one string, separating with spaces, stripping any leading or trailling spaces.
    fullMajor = " ".join(listOfMajorNum).strip()  

    # Append full name and majors together to `namesList`
    namesList.append(firstName + " " + fullMajor + "\n")
    
# Opens the outputFile as a write.
open(outputFileName, "w")

# Adds each name from namesList and writes it to the outputFile.
with open(outputFileName, "a") as file:
    for name in namesList:
        file.write(name)

# Sets the list of major counts.
majorCountGraph = list(countOfMajors.values())


# Prints for each major their count using a dictionary to assign counts to each major.
# Writes to the outputFile.
print("The number of Civil Engineering students: ", countOfMajors["Civil Engineering"], file=open(outputFileName, "a"))
print("The number of Computer Engineering students: ", countOfMajors["Computer Engineering"], file=open(outputFileName, "a"))
print("The number of Electrical Engineering students: ", countOfMajors["Electrical Engineering"], file=open(outputFileName, "a"))
print("The number of Mechanical Engineering students: ", countOfMajors["Mechanical Engineering"], file=open(outputFileName, "a"))

# Creates a bar graph, setting the x and y values, as well as the colors for each bar, width of each bar.
# Need to manually add more colors if more bars are added.
fig = plt.figure(1, figsize = (12, 5))
plt.bar(majorNamesGraph, majorCountGraph, color = ['cyan', 'blue', 'purple', 'red', 'green'], width = 0.4)

# Create an array to represent each bar. (1st bar = 0, 2nd bar = 1...)
xLabel = [0, 1, 2, 3, 4]

# Loops through for each major in the dictionary countOfMajors.
for i in range(len(countOfMajors)):

    # Sets the count labels above each bar.
    plt.text(x = xLabel[i] - 0.05, y = majorCountGraph[i], s = majorCountGraph[i], size = 10)

# Labels the graph.
plt.xlabel("Student Majors")
plt.ylabel("No. of students enrolled")
plt.title("Enrolled Student Information")

fig2 = plt.figure(2, figsize = (5, 5))
# Creates a venn diagram, compares each set with each other using the venn3 function.
v1 = venn3([computerEngSet, electricalEngSet, mechanicalEngSet], ("Computer Engineering", "Electrical Engineering", "Mechanical Engineering"))

fig3 = plt.figure(3, figsize = (5, 5))
v2 = venn3([civilEngSet, electricalEngSet, mechanicalEngSet], ("Civil Engineering", "Electrical Engineering", "Mechanical Engineering"))

fig4 = plt.figure(4, figsize = (5, 5))
v2 = venn3([civilEngSet, computerEngSet, electricalEngSet], ("Civil Engineering", "Computer Engineering", "Electrical Engineering"))

plt.show()

# Can use the line below if you want to print the count of other major students as well.
# print("The number of Other major students: ", countOfMajors["Other"], file=open(outputFileName, "a"))
