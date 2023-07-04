### 04.07.2023 

# <center> BikeShare </center>

Bikeshare is an interactive python script that reads the data for city bike usage in Chicago, New York and Washington and calculates some statistics.<br>
Depending on the user's preferences, the data is first filtered by **city** and **day of the week** or **month**. Then the most frequent **travel times**, most frequently used **stations and connections**, the usual **travel duration** and **characteristics of the users** are determined.

### Installation:
Clone the [GitHub repository](https://github.com/LeaMeissner/pdsnd_github.git):
```
git clone https://github.com/LeaMeissner/pdsnd_github.git
cd pdsnd_github
```

Install required packages:
```
pip install numpy
pip install pandas
pip install cdifflib
```

### Files used:
- *chicago.csv*
- *new_york_city.csv*
- *wahington.csv*

### Usage:
Follow the instructions of the interactive script to read in the **city** and, if desired, a **day of the week** or **month**.

### Credits
The basic framework of *bikeshare.py* as well as the function *main()* was provided by Udacity.
