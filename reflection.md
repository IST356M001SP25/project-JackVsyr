# Reflection

Student Name:  name
Student Email:  email

## Instructions

Reflection is a key activity of learning. It helps you build a strong metacognition, or "understanding of your own learning." A good learner not only "knows what they know", but they "know what they don't know", too. Learning to reflect takes practice, but if your goal is to become a self-directed learner where you can teach yourself things, reflection is imperative.

- Now that you've completed the assignment, share your throughts. What did you learn? What confuses you? Where did you struggle? Where might you need more practice?
- A good reflection is: **specific as possible**,  **uses the terminology of the problem domain** (what was learned in class / through readings), and **is actionable** (you can pursue next steps, or be aided in the pursuit). That last part is what will make you a self-directed learner.
- Flex your recall muscles. You might have to review class notes / assigned readings to write your reflection and get the terminology correct.
- Your reflection is for **you**. Yes I make you write them and I read them, but you are merely practicing to become a better self-directed learner. If you read your reflection 1 week later, does what you wrote advance your learning?

Examples:

- **Poor Reflection:**  "I don't understand loops."   
**Better Reflection:** "I don't undersand how the while loop exits."   
**Best Reflection:** "I struggle writing the proper exit conditions on a while loop." It's actionable: You can practice this, google it, ask Chat GPT to explain it, etc. 
-  **Poor Reflection** "I learned loops."   
**Better Reflection** "I learned how to write while loops and their difference from for loops."   
**Best Reflection** "I learned when to use while vs for loops. While loops are for sentiel-controlled values (waiting for a condition to occur), vs for loops are for iterating over collections of fixed values."

`--- Reflection Below This Line ---`

For my final project, I built a streamlit application that has a full ETL pipeline that uses real world aircraft listing data from ASO.com. The main objective of this project was to gain hands on experience with the data scraping, transformation, and visualization skills we covered this semester. My goal was to create an interactive tool that can help identify which states have the most aircraft listings, and where brokers tend to concentrate their sales activity.

The Extraction step involved using a custom Python scraper I built with playwright to collect aircraft listing data directly from the ASO website. The scraper was in a separate file and executed using function calls from the main transform file. The Transformation process involved cleaning the raw scraped data, handling nulls, removing excess characters, and making sure the data was cohesive across fields like location and aircraft model. This was done in a dedicated transform file and included a function to dynamically grab the CSV file that matches todays date The Loading step was handled by the Streamlit app, which displayed a map of the U.S. with listings in each state using pydeck_chart. My original intent was to allow users to click directly on the state to view listings, but I found a limitation in streamlit where pydeck doesn’t support clicking on the map. To work around that I made a dropdown menu that lets users select a state instead.

This project helped me better understand function reuse and figuring out the user experience in applications. I also practiced adding docstrings, using __main__ blocks, and organizing my code in modules like we did in class. If I had more time, I would extend the scraper to pull more detailed data for each aircraft and make more visualizations, such as timeline trends.