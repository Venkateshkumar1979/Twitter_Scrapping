# Importing necessary libraries
import snscrape.modules.twitter as sntwitter
import pandas as pd
import streamlit as st
import pymongo

#Connecting with MongoDB Atlas 
client = pymongo.MongoClient('mongodb+srv://VenkateshKumar:Venkat1234@cluster0.rzrutfu.mongodb.net/?retryWrites=true&w=majority')
db=client['twitter']
collection=db['tweets']

def main():
    # Deleting the previous records in Mongodb and ready for new search
    collection.delete_many({})
    
    # Collect the keyword, start date, end date, and number of tweets from the user using streamlit.
    st.title("Twitter Data Scraping")
    keyword = st.text_input("Enter a keyword / Hashtag")
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")
    num_tweets = st.number_input("Number of tweets", min_value=1)
    
    # Using TwitterSearchScraper to scrape data and append tweets to list.
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}").get_items()):
        if i >= num_tweets:
            break
        tweets_list.append([keyword,
                            tweet.date,
                            tweet.user.created,
                            tweet.id,
                            tweet.url,
                            tweet.rawContent,
                            tweet.user.username,
                            tweet.lang,            
                            tweet.replyCount,
                            tweet.retweetCount,
                            tweet.likeCount,
                            tweet.source]
                           )
            
    # Storing the scraped data to a dataframe.
    tweets_df=pd.DataFrame(tweets_list,columns=['Scraped_Word','Date','Created_Date','ID','URL','Content','User','Language','ReplyCount','RetweetCount','LikeCount','Source'])
    # Viewing the data as Dataframe in Streamlit
    if st.button('View as DataFrame'):
        st.write('DataFrame of Scraped Data from Twitter')
        st.dataframe(tweets_df)
    
    # Writing the Scraped data into MongoDB Collections.
    dct=tweets_df.to_dict(orient='records')
    collection.insert_many(dct)
    
    # Viewing the data as MongoDB Collections in Streamlit
    if st.button('View as MongoDB Database'):
        cursor=collection.find()
        for document in cursor:
            st.write(document)
            
    # Downloading the data
    
    # Download this scraped data in the form of CSV format.
    if st.button("Download Data as CSV"):
        tweets_df.to_csv(f"{keyword}.csv", index=False)
        st.success(f"Data downloaded successfully as {keyword}.csv")
    
    # Download this scraped data in the form of JSON format.
    if st.button('Download as JSON'):
        tweets_df.to_json(f'{keyword}.json',orient='records')
        st.success(f'Data Downloaded successfully as {keyword}.json')
        
           
# Calling the main function

main()        






    
    
    
    
    
    
    
    