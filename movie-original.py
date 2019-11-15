from scipy.io import arff
import sys
from decimal import Decimal

def getHighestActorRating(actor_likes_list):
    likes = max(actor_likes_list)

    if likes <= 7700:
        return 'F'
    elif likes > 7700 and likes <= 15400:
        return 'D'
    elif likes > 15400 and likes <= 23100:
        return 'C'
    elif likes > 23100 and likes <= 30800:
        return 'B'
    else:
        return 'A'


# Change the continuous data to discrete data for imdb_score (Column Z from excel)
def ratingGrade(rate):
    getRate = ''
    if rate >= 9.0:
        getRate = 'Excellent'
    elif rate >= 8.0 and rate < 9.0:
        getRate = 'Good'
    elif rate >= 7.0 and rate < 8.0:
        getRate = 'Above_Average'
    elif rate >= 6.0 and rate < 7.0:
        getRate = 'Average'
    elif rate >= 5.0 and rate < 6.0:
        getRate = 'Below_Average'
    elif rate >= 4.0 and rate < 5.0:
        getRate = 'Poor'
    elif rate > 0 and rate <4.0:
        getRate = 'Awful'
    return getRate

# Change the continuous data to discrete data for num_voted_users (Column M from excel)
def numVotedUsers(num):
    critic = ''
    # Less than 20K voters
    if num <= 20000:
        critic = 'Low'
    # Between 20K to 80K voters
    elif num > 20000 and num <= 80000:
        critic = 'Average'
    # More than 80K voters
    elif num > 80000:
        critic = 'High'
    return critic

# Get the appropriate content rating like if content rating is 'M', return 'PG'
def contentRating(rating):
    rate = rating
    if "Not Rated" == rating:
        rate = "Unrated"
    elif "X" == rating:
        rate = "NC-17"
    elif "M" == rating:
        rate = "PG"
    elif "GP" == rating:
        rate = "PG"
    elif "Passed" == rating:
        rate = "Approved"
    return rate

# Pick which genre comes first...
def getGenre(data):
	genre = ''

	if "Animation" in data:
		genre = "Animation"
	elif "Family" in data:
		genre = "Family"
	elif "Documentary" in data:
		genre = "Documentary"
	elif "Western" in data:
		genre = "Action"
	elif "Horror" in data:
		genre = "Horror"
	elif "Sci-Fi" in data:
		genre = "Sci-Fi"
	elif "Thriller" in data:
		genre = "Thriller"
	elif "Fantasy" in data and "Horror" in data:
		genre = "Horror"
	elif "Fantasy" in data:
		genre = "Romance"
	elif "Comedy" in data:
		genre = "Comedy"
	elif "War" in data:
		genre = "Action"
	elif "Romance" in data:
		genre = "Romance"
	elif "Drama" in data:
		genre = "Drama"
	elif "Action" in data:
		genre = "Action"
	elif "Adventure" in data:
		genre = "Action"
	else:
		genre = data[0]
	return genre

def budget(num):
    discBudget = ''
    # Less than 12 million dollars budget
    if num < 12000000:
        discBudget = 'Low'
    # Between 12 million to 35 million dollars budget
    elif num >= 12000000 and num < 35000000:
        discBudget = 'Medium'
    # More than 35 million dollars budget
    elif num >= 35000000:
        discBudget = 'High'
    return discBudget

# Categorize director Facebook likes low/avg/high
def getDirectorLikes(num):
    dirLikes = ''
    if num <= 300:
        dirLikes = 'Low'
    elif num > 300 and num <= 1100:
        dirLikes = 'Average'
    elif num > 1100:
        dirLikes = 'High'
    return dirLikes

# Open the csv file
def readCSVFile(fileName):
    csvData = []
    line = ''
    countNumber = []
    fileCSV = open(fileName, 'r')
    line = fileCSV.readline().strip()
    flag = True

    while line:
        # Skip the first row from excel [color, director_name, num_critic_for_reviews, duration, etc...]
        if flag:
            flag = False
        else:
            # Reading 2nd rows to 3721 rows
            getData = line.split(",") # new array

            # See column L for title. Some title movie have commas, place two elements in one element. For ex. ['War'], ['Inc.'] = ['War, Inc.']
            if len(getData) == 29:
                title = getData[11] + "," + getData[12]
                del getData[12]
                getData[11] = title[1:-1] # This ignore double quotation and keep single quote

            # Place three elements in one element for title. For ex. ['Sex'], ['Lies'], [' and Videotape'] = ['Sex, Lies, and Videotape']
            elif len(getData) == 30:
                title = getData[11] + "," + getData[12] + "," + getData[13]
                del getData[13]
                del getData[12]
                if '"' in title:
                    title.replace("\"", '', 2)
                getData[11] = title[1:-1]

            # Place four elements in one element for title. For ex. ['It's a Mad'], [' Mad'], [' Mad'], [' Mad World']= ['It's a Mad, Mad, Mad, Mad World']
            elif len(getData) == 31:
                title = getData[11] + "," + getData[12] + "," + getData[13] + "," + getData[14]
                if '"' in title:
                    title.replace("\"", '', 2)
                del getData[14]
                del getData[13]
                del getData[12]
                getData[11] = title[1:-1]

            # If genre is in element with '|'   for ex. ['Comedy|Drama|Mystery|Romance|Thriller']
            if "|" in getData[9]:
			    getData[9] = getGenre(getData[9].split("|"))
            else:
                getData[9] = getGenre(getData[9])

            # If each attributes for particular row has no empty value, then put it in 2d array
            if getData[4] and getData[5] and getData[7] and getData[9] and getData[12] and getData[21] and getData[22] and getData[24] and getData[25]:
                countNumber.append(int(getData[22]))
                 # Change it from continuous to discretize data
                getData[4] = getDirectorLikes(int(getData[4]))

                actor_ratings = [int(getData[5]), int(getData[7]), int(getData[24])]
                getData[5] = getHighestActorRating(actor_ratings)
                getData[12] = numVotedUsers(int(getData[12]))
                getData[21] = contentRating(getData[21])
                getData[22] = budget(int(getData[22]))
                getData[25] = ratingGrade(Decimal(getData[25]))
                csvData.append(getData)

        # Clear array and read next line
        line = fileCSV.readline().strip()
    fileCSV.close()
    print "Number of voters: " + str(len(set(countNumber)))
    return csvData

def write_data(fileName, dataInArray):
    data = "@RELATION movies\n\n@ATTRIBUTE director_facebook_likes \t{Low,Average,High}\n" \
    + "@ATTRIBUTE highest_actor_rating \t{A,B,C,D,F}}\n" \
    + "@ATTRIBUTE genre\t{Sci-Fi,Action,Animation,Family,Documentary,Romance,Comedy,Drama,Horror,Thriller}\n" \
    + "@ATTRIBUTE num_voted_users \t{Low,Average,High}\n@ATTRIBUTE content_rating \t{Approved,G,NC-17,PG,PG-13,R,Unrated}\n@ATTRIBUTE budget \t{Low,Medium,High}\n" \
    + "@ATTRIBUTE imdb_score\t{Excellent,Good,Above_Average,Average,Below_Average,Poor,Awful}\n\n@DATA"
    # create movie.arff file
    with open(fileName, "w") as fp:
        # Write on movie.arff for first line. For ex. @RELATION movies  @ATTRIBUTE director_facebook_likes REAL
        fp.write(''+ data + '' + '\n')

        # 2D array is read each group element. For ex. First group element ['Color', 'Bill Benenson', '1', '71', '0', '21', 'Dave Fennoy', '1000', etc...]
        for dataPrint in dataInArray:
            fp.write(str(dataPrint[4]) + "," + str(dataPrint[5]) + "," + str(dataPrint[9]) + "," + str(dataPrint[12]) + "," + str(dataPrint[21]) + "," + str(dataPrint[22]) + "," + str(dataPrint[25]) + "\n")
        fp.close()

# This execute at the beginning...
if __name__== "__main__":
    data = readCSVFile("movies_imdb.csv")
    write_data("movie.arff", data)
