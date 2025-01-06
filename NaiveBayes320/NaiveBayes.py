from math import sqrt
from math import exp
from math import pi
from statistics import mean
from statistics import stdev
from scipy.stats import norm
import csv

#calculates the mean of the values given and returns that value
def getMean(allValues):
	#add up all the values in allValues and then divide by the amount of values in allValues to get the mean
	temp = mean(allValues)
	return temp

#calculates the standard deviation of the values given and returns that value
def getStandardDeviation(allValues):
	#we assign a value to equal the summation of the mean subtracted from each individual value in allValues
	#then we divide that number by the amount of objects in allValues 
	#then do the square root
	temp = stdev(allValues)
	return temp

#this function uses a distriubtion function called the Gaussian Probability Distribution Function
#it is used to determine the probability of a given variable using the mean and standard deviation
#the function has been divided in two for slightly better readability
def getProbability(x, mean, standardDeviation):
	temp = exp(-((x-mean)**2 / (2 * standardDeviation**2)))
	temp =  (1 / (sqrt(2*pi) * standardDeviation)) * temp
	return temp

#cycles through the columns of data in the provided lists of lists and returns a summary of all their stats, including
#mean, median, and length
def getStats(data):
	#the stats list is initalized with the data that is made through the for loop, which cycles through all the columns of data
	#that are found using the zip command, and gets their mean, standard deviation, and length, and adds them to stats as a list
	stats = [(getMean(column), getStandardDeviation(column), len(column)) for column in zip(*data)]
	#we delete the first one as the first element is the identifying element for the type, and therefore does not need any stats
	del(stats[0])
	return stats

#calculates which key has the largest associated value and returns the key associated with it
def getMaxDictionaryKey(d):
	return max(d, key = d.get)

#takes the data table and creates a dictionary that is sorted by type, and creates a new empty dictionary
#that will hold the stats of said types, still sorted by types
def statsTypeSorted(data):
	#create an empty dictionary to hold the sorted type in
	typeSorted = dict()
	
    #loop through all the lists in the larger list provided (data)
	for i in range(len(data)):
		#holds the current list
		temp = data[i]
		#checks what type the current list belongs to, should be in the first position
		typeNumberTemp = temp[0]
		#checks the dictionary, if the type of the current list is already in the dictionary, it just appends the current list
        #to the list of lists associated with the key value. otherwise, it adds the key value with an uninitalized list, and then
        #appends the list to said empty list, making it a list of lists
		if (typeNumberTemp not in typeSorted):
			typeSorted[typeNumberTemp] = list()
		typeSorted[typeNumberTemp].append(temp)

	#create an empty dictionary to hold the stats sorted by type
	stats = dict()
	#for each key in the typeSorted dictionary, iterate through the rows and add the stats of each to the dictionary
	for typeNumber, rows in typeSorted.items():
		stats[typeNumber] = getStats(rows)
	#return the complete dictionary
	return stats

#the final piece, this function will take take the return of statsTypeSorted and compare each type
#to a given piece of data to determine the probability of that piece of data belonging to that type
def getTypeProbability(stats, row):
	#get the total amount of objects in the stats
	totalTypes = sum([stats[desc][0][2] for desc in stats])
	#make ANOTHER dictionary to hold the final result
	probabilities = dict()
	#loop through the keys in stats, incrementing two variables as it goes
	for typeNumber, typeStats in stats.items():
		#initalizes the key typeNumber
		probabilities[typeNumber] = stats[typeNumber][0][2]/float(totalTypes)
		#loops through and multiplies the total probability times the probability of the
		#mean or standard deviation fitting with the current ctype being compared
		#leangth is -1 and row is +1 due to the type being the first argument
		for i in range(len(typeStats)):
			mean, stdev, _ = typeStats[i]
			probabilities[typeNumber] *= getProbability(row[i], mean, stdev)
	return probabilities


#THE MAIN OF THE FUNCTION IS AS FOLLOWS

#initialize the data array
data = []
#open the csvfile, this name can be changed as needed
with open("Weather.csv") as csvfile:
    #opens the entire csv file into reader, converting anything not in quotation marks into floats
    reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)
    #loops through all rows in the csv file and prints each as a list entry in the array
    for row in reader:
        data.append(row)

#initalize the stats variable with all the stats sorted by type
stats = statsTypeSorted(data)

#initalize the probablilities dictionary with the final results of the naive bayes comparison
#input.csv - 4.7232434942,4.29652422675
#baseballinput.csv - 400,120,25
#Weather.csv - 40,60,0.75
probabilites = getTypeProbability(stats,[50, 35, 0.4])

#print the results
#the results of the program describe how likely it is that the data given in the call of getTypeProbability belongs to each type
#the one with the highest number is the most likely when compared to the mean and median of each type, aka the stats
#want to change the program to allow the user to input their own data to compare to the data given, maybe even add the option
#of the user inputting their own data to be used
for i, j in probabilites.items():
	print("Probability of ", i, ": ", j)

#computes the most probable outcome based off naive bayes theorem and prints out which class it is
print("The most probable outcome is: ",getMaxDictionaryKey(probabilites))
	