import time
import pandas as pd
import numpy as np
from datetime import date # library to handle dates
from difflib import SequenceMatcher # library to compare sequences of characters

# dictionary CITY_DATA that assigns corresponding files to the cities.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

def get_filters():
    """ 
    Function that asks user to specify a city, month and day to analyze. 
    output: 
        city (str): name of the city (chicago, new york city or washington) to analyze
        month (str): name of the month (january, february, march, april, may or june) to filter by, or "all" to apply no month filter
        day (str): name of the day of week (monday, tuesday, wednesday, thursday, friday, saturday or sunday) to filter by, or "all" to apply no day filter  
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    while True: # while loop that allows to change the input if it does not match the desired input 
        
        # get user input for city:
        while True: # repeat the input for the city until successful
            city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower() 

            # repeat the input for the city if it does not match any allowed cities, otherwise continue:
            possible_citys = ['chicago', 'new york city', 'washington']
            if city not in possible_citys:
                # handle unexpected input:
                similarity  = np.array([SequenceMatcher(None, city, city_candidate).ratio() for city_candidate in possible_citys])
                candidate_similarity = np.max(similarity)
                city_candidate = possible_citys[np.argmax(similarity)]
                if candidate_similarity < 0.6: # if similarity is below 0.6 request a new input
                    print('No valid input for the city!\n')
                else: # otherwise ask if the city_candidate was meant by the input
                    right_input = input('\nNo valid input for the city! Do you mean "{0}"? This city has a {1:.3g}% match with the input. Enter yes or no.\n'.format(city_candidate.title(), candidate_similarity*100)).lower() 
                    if right_input.lower() == 'yes':
                        city = city_candidate # then set the city as the city_candidate
                        break
            else:
                break 
        
        # get user input for the filter:
        while True: # repeat the input for the filter until successful
            filter = input('\nWould you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n').lower()

            # repeat the input for the filter if it does not match any allowed filters, otherwise continue
            if filter != 'month' and filter != 'day' and filter != 'both' and filter != 'none':
                print('No valid input for the filter!')
            else:
                break 
        
        # get user input for month:
        if filter == 'month' or filter == 'both': 
            while True: # repeat the input for the month until successful
                month = input('\nWhich month - January, February, March, April, May, or June?\n').lower()

                # repeat the input for the month if it does not match any allowed months, otherwise continue
                if month != 'january' and month != 'february' and month != 'march' and month != 'april' and month != 'may' and month != 'june':
                    print('No valid input for the month!')
                else:
                    break
        else: # if you do not want to filter by month, set month to 'all months'
            month = 'all months'

        # get user input for day of week:
        if filter == 'day' or filter == 'both': 
            while True: # repeat the input for the day until successful
                day = input('\nWhich day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n').lower()

                # repeat the input for the day if it does not match any days of the week, otherwise continue
                if day != 'monday' and day != 'tuesday' and day != 'wednesday' and day != 'thursday' and day != 'friday' and day != 'saturday' and day != 'sunday':
                    print('No valid input for the day!')
                else:
                    break
        else: # if you do not want to filter by day, set day to 'all days'
            day = 'all days'

        restart = input('\nYou selected to look at {} data in {} and on {}. Is that correct? Enter yes or no.\n'.format(city.title(), month, day))
        
        if month == 'all months':
            month = 'all'
        
        if day == 'all days':
            day = 'all'
        
        if restart.lower() == 'yes':
            break # continue when the input matches the desired input 

    print('-'*40)

    return city, month, day

def load_data(city, month, day):
    """ 
    Loads data for the specified city and filters by month and day if applicable.
    input: 
        city (str): name of the city (chicago, new york or washington) to analyze
        month (str): name of the month (january, february, march, april, may or june) to filter by, or "all" to apply no month filter
        day (str): name of the day of week (monday, tuesday, wednesday, thursday, friday, saturday or sunday) to filter by, or "all" to apply no day filter
    output: 
        data (Pandas DataFrame): DataFrame containing city data filtered by month and day
    """

    print('Loading the data ...')
    start_time = time.time()

    # load data for the specified city:
    if city.lower() == 'chicago':
        data = pd.read_csv(CITY_DATA['chicago'])
    elif city.lower() == 'new york city':
        data = pd.read_csv(CITY_DATA['new york city'])
    elif city.lower() == 'washington':
        data = pd.read_csv(CITY_DATA['washington'])

    # append the month, weekday and hour of the start time to the dataframe:
    data['Month'] = pd.to_datetime(data['Start Time']).apply(lambda x: x.strftime("%B"))
    data['Weekday'] = pd.to_datetime(data['Start Time']).apply(lambda x: x.strftime("%A"))
    data['Hour'] = pd.to_datetime(data['Start Time']).apply(lambda x: x.strftime("%H"))
    
    # filter data by month:
    if month != 'all':
        data = data[data['Month'] == month.title()] 

    # filter data by day:
    if day != 'all':
        data = data[data['Weekday'] == day.title()] 

    # reset the index of the data frame
    data.reset_index(inplace=True)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    return data

def time_stats(data, month, day):
    """ 
    Displays statistics on the most frequent times of travel.
    input: 
        data (Pandas DataFrame): DataFrame containing city data filtered by month and day
        month (str): name of the month by which the data was filtered or "all" if no month filter was applied
        day (str): name of the day of week by which the data was filtered or "all" if no month filter was applied
    """
    
    print('\nCalculating The Most Frequent Times of Travel ...')
    start_time = time.time()

    # display the most common month
    if month == 'all': 
        most_common_month = data['Month'].value_counts().idxmax() # counts how often a month appears and selects the most frequent 
        most_common_month_count = data['Month'].value_counts().max() # number of times the the most frequent month appears
        print('   - Most popular month for traveling: {}, Count: {}'.format(most_common_month, most_common_month_count))

    # display the most common day of week
    if day == 'all':
        most_common_weekday = data['Weekday'].value_counts().idxmax() # counts how often a weekday appears and selects the most frequent 
        most_common_weekday_count = data['Weekday'].value_counts().max() # number of times the the most frequent weekday appears
        print('   - Most popular day of week for traveling: {}, Count: {}'.format(most_common_weekday, most_common_weekday_count))

    # display the most common start hour
    most_common_hour = data['Hour'].value_counts().idxmax() # counts how often a hour appears and selects the most frequent 
    most_common_hour_count = data['Hour'].value_counts().max() # number of times the the most frequent hour appears
    print('   - Most popular start hour for traveling: {}, Count: {}'.format(most_common_hour, most_common_hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(data):
    """ 
    Displays statistics on the most popular stations and trip.
    input: 
        data (Pandas DataFrame): DataFrame containing city data filtered by month and day
    """

    print('\nCalculating The Most Popular Stations and Trip ...')
    start_time = time.time()

    # display most commonly used start station
    most_common_start = data['Start Station'].value_counts().idxmax() # counts how often a start station appears and selects the most frequent 
    most_common_start_count = data['Start Station'].value_counts().max() # number of times the the most frequent start station appears
    print('   - Most commonly used start station: {}, Count: {} '.format(most_common_start, most_common_start_count))

    # display most commonly used end station
    most_common_end = data['End Station'].value_counts().idxmax() # counts how often a end station appears and selects the most frequent 
    most_common_end_count = data['End Station'].value_counts().max() # number of times the the most frequent end station appears
    print('   - Most commonly used end station: {}, Count: {}'.format(most_common_end, most_common_end_count))

    # display most frequent combination of start station and end station trip
    most_common_trip = data[['Start Station','End Station']].value_counts().idxmax() # counts how often a trip appears and selects the most frequent 
    most_common_trip_count = data[['Start Station','End Station']].value_counts().max() # number of times the the most frequent trip appears
    print('   - Most frequent trip: from {} to {}, Count: {}'.format(most_common_trip[0],most_common_trip[1], most_common_trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(data):
    """ 
    Displays statistics on the total and average trip duration.
    input: 
        data (Pandas DataFrame): DataFrame containing city data filtered by month and day
    """

    print('\nCalculating Trip Duration ...')
    start_time = time.time()

    # display total travel time
    total_travel_time = data['Trip Duration'].sum() # sums up over all travel times
    print('   - Total travel time: {} seconds'.format(total_travel_time))
    
    # display mean travel time
    mean_travel_time = data['Trip Duration'].mean() # calculates the average of all travel times
    print('   - Average travel time: {} seconds'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(data, city):
    """ 
    Displays statistics on bikeshare users.
    input: 
        data (Pandas DataFrame): DataFrame containing city data filtered by month and day
        city (str): name of the city by which the data was filtered
    """

    print('\nCalculating User Stats ...')
    start_time = time.time()

    # display counts of user types:
    user_types_count = data['User Type'].value_counts() # counts how often a user type appears
    print('Counts of User Types:')
    for user_type in user_types_count.index: 
        print('   - ', user_type, ':', user_types_count[user_type]) # output of the count for each user type

    # display counts of gender:
    if city != 'washington':
        gender_count = data['Gender'].value_counts() # counts how often a gender appears
        print('Counts of Gender of the Users:')
        for gender in gender_count.index: 
            print('   - ', gender, ':', gender_count[gender]) # output of the count for each gender

    # display earliest, most recent, and most common year of birth:
    if city != 'washington':
        print('Year of Birth of the Users')
        earliest_birthyear = data['Birth Year'].min() # determines the earliest year of birth 
        print('   - earliest year of birth: ', int(earliest_birthyear))
        most_recent_birthyear = data['Birth Year'].max() # determines the latest year of birth 
        print('   - most recent year of birth: ', int(most_recent_birthyear))
        most_common_birthyear = data['Birth Year'].value_counts().idxmax() # counts how often a birthyear appears and selects the most frequent
        print('   - most common year of birth: ', int(most_common_birthyear))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_trip_data(data):
    """ 
    Displays individual trips.
    input: 
        data (Pandas DataFrame): DataFrame containing city data filtered by month and day
    """
    
    go_on = True # termination condition
    idx = 0 # start index
    while go_on:
        see_data = input('\n Would you like to see individual trip data? Enter yes or no.\n').lower() 
        
        # output the next 5 trips starting at idx:
        if see_data == 'yes':
            print(data.iloc[idx:idx+5]) 
            idx = idx + 5 # update idx

        # stop when see_data is set to 'no' or the end of the data frame is reached:
        if see_data != 'yes' or idx>=data.shape[0]:
            go_on = False

def main():
    while True:
        
        city, month, day = get_filters()

        data = load_data(city, month, day)

        time_stats(data, month, day)
        station_stats(data)
        trip_duration_stats(data)
        user_stats(data, city)
        print_trip_data(data)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower() 
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()