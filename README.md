# Project: Predicting Car Price

### Business Use Case
CarWax is a used vehicle retailer based in the United States that has decided to start selling used Japanese domestic market (JDM) vehicles. CarWax plans on restocking their JDM vehicle inventory each month, and they would like to have an automated system that can quickly calculate how much money they will need to spend next month based on the types of vehicles that are needed. Specifically, CarWax would like to have a machine learning model which can take a set of inputs (engine size, body type, number of seats, etc...) and return an estimated price for the vehicle.

**Note:** CarWax has partnered with Car From Japan Co. (https://carfromjapan.com/) and will only use data from this vendor.

### Project Description

To fufill CarWax's request we underwent the following steps:

1) Scraped the Car From Japan website for all available used car listings using a python script.
2) Performed an Exploratory Data Analysis
  a) Cleaned data and removed potentially erroneous entries
  b) Looked at the relationships between variables
  c) Observed distribution of variables
  c) Performed dimensionality reduction analysis
  d) Saved cleaned dataset for modeling
3) Modeling
  a) Trained and tested several machine learning algorithms using n-fold cross validation
  b) Identified best-performing model and saved model


### Running Code

The entire analysis can be run including the web scraper although a few libraries may need to be installed beforehand.

Dependencies: pandas, numpy, BeautifulSoup, sklearn, matplotlib, seaborn

Files:
- `scraper.py`: Generates dataset used in EDA analysis by scraping all used car postings on https://carfromjapan.com/
- `Car_Price_EDA.ipynb`: Jupyter notebook with EDA results and saves cleaned dataset to file for the modeling step
- `Modeling.ipynb`: Jupyter notebook with modeling results and saves best-performing model to file for delivering to the client

The entire project can be recreated by running the three files in the order they are listed.


### Conclusion

Our recommendation is that CarWax implents a Random Forest model to help automate their method for calculating restocking costs. This algorithm had the lowest root mean square error (RMSE) compared to other algorithms tested after 10-fold cross validation. We chose RMSE as the metric for identifying the best model because RMSE more heavily penalizes models with larger errors; a major concern CarWax has is greatly over or underestimating the dollar amount they need to spend next month.

Our EDA also brought up some concerns with the data posted on Car From Japan's website. Namely, there were several listings for used JDM cars which were going for $100M+. Similarly, we observed a few cars with absurdly large mileages (3M+ mi) and absurdly large engines (64,000+ cubic centimeters). We had no way of confirming if these entries were erroneously entered, but it is something that we would like to communicate to Car From Japan. 

Some next steps that we propose after this modeling analysis would be to create a linear programming model. Linear programming is a mathematical modeling method that allows us to minimize or maximize some function. We could create a function for the amount of profit a certain car is projected to return and constraints for the types of cars we need to order each month. Our plan would then be to have the linear program automatically tell CarWax what types of cars they need to buy, and the Random Forest model would recieve those inputs and calculate how much needs to be spent on restocking.
