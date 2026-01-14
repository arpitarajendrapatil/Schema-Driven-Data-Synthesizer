# Schema-Driven-Data-Synthesizer
> Tested on Python 3.12+ (Windows/Linux)

# Description 
A configuration-driven Python engine that automates the creation of high-volume synthetic datasets via XLSX templates. This system supports regex patterns and custom value sets to generate realistic information for stress-testing applications. 

# Project structure
project-root/
│── data_generation/
│   │── main.py                     # Entry point of the application
│   │── utility.py                  # Helper and utility functions
│   │── Input_Data_Details.xlsx     # Primary input Excel file
│   │── Input_Data_Details.csv      # Generated output CSV file
│   │── app-config.properties       # Application configuration file
│   │── data_generation_logs.logs   # Application log file
│   │
│   └── resources/
│       └── Input_Data_Details.xlsx # Backup copy of input Excel file
│
│── requirements.txt                # Python dependencies
│── README.md                       # Project documentation

# Prerequisites
Make sure the following software is installed on your system before running the project:
1. Python 3.10+
2. pip
3. Virtual Environment (recommended)

# Steps to Run the Project
1. Clone the Repository 
2. Create and Activate Virtual Environment (Recommended)
3. Install dependencies using requirements.txt : pip install -r requirements.txt
4. Run the Application : python3 main.py
5. Follow the user journey mentioned below

# Input:
Input_Data_Details.xlsx - An excel file (containing schema) given to the program as an input for Data Generation. This file contains Field names, Data types of the data to be generated. It also has other parameters like Size, Regex Pattern, Primary Key, Sequence etc which can be populated by the user based on their requirement for each field.

# Output:
Input_Data_Details.csv - A csv file containing large volumes of random data generated for the fields given in the Input_Data_Details.xlsx.

# User Journey:
1. Create an Input_Data_Details.xlsx file containing schema with names of all the fields for random data generation. 
2. Mention all the validation/parameters to be checked for data generation for each field.
3. Place the file in the project directory.
4. Run the main.py file using the python run main.py command.
5. Mention the total no.of records of data to be generated. Max : 9000 records
6. Receive an Input_Data_Details.csv file which gets downloaded in the project directory.
7. The csv file has random data generated of the total records mentioned by the user.

# Python Dependencies
- pandas
- rstr
- jproperties
- openpyxl






