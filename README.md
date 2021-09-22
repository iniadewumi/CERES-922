# CERES-922
This is a program to pull oil prices, latest analysis and lattest news articles from multiple sources and combine them into an email.

SOURCES:
  1. CME Group: The official commodities exchange for oil commodities
  2. Investing.com: Keeps abreast of news and has live price updates
  3. OilPrice.com: Most popular industry website for oil prices. 
  
  
 FILES:
  HTML FILES: Contain Email MarkUp and styling (HTML & CSS)
  hasher.py: For Passwords if you decide to use
  EmailMain: This is the email SMTP server code. It collects all the info needed to generate and send email
  main.py: Pulls all the code together, calls the needed commands to compile info from all sources and calls the EmailMain file to generate and send email.
  OilReport.py: File that contains the different classes and class methods that pull information from all sources. Can be modified to collect specifics from each website without affecting the others. 
  
 
 More details to come soon...
 
 
