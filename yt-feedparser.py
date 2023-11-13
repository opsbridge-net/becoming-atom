import feedparser
import time
import requests

def send_slack_message(link, author):

    slack_webhook_url = ''

    message = f"*Author:* {author}\n*Link:* {link}"

    payload = {
        'text': message
    }

    requests.post(slack_webhook_url, json=payload)

def parse_atom_feed(interval_minutes=30):

    atom_feed_urls = [
        # David Firth
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCaGev0JRG7Dp5c_R4ROADLw',
        # PilotRedSun
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCUzzFuijK8WH4zdbVu33BvA',
        # Academy of Ideas
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCiRiQGCHGjDLT9FQXFW0I3A',
        # Quanta Magazine
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCTpmmkp1E4nmZqWPS-dl5bg',
        # PolyMatter
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCgNg3vwj3xt7QOrcIDaHdFg',
        # The School of Life
        'https://www.youtube.com/feeds/videos.xml?channel_id=UC7IcJI8PUf5Z3zKxnZvTBog',
        # Geography Geek
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCFaSR7gUU39qJe-eDSiGY0A',
        # Ryan Chapman
        'https://www.youtube.com/feeds/videos.xml?channel_id=UC6FO-Up1-oLj5nNivCNHL-Q',
        # Kurzgesagt – In a Nutshell
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCsXVk37bltHxD1rDPwtNM8Q',
        # Financial Times
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCoUxsWakJucWg46KW5RsvPw',
        # TechLinked
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCeeFfhMcJa1kjtfZAGskOCA',
        # TLDR News Global
        'https://www.youtube.com/feeds/videos.xml?channel_id=UC-uhvujip5deVcEtLxnW8qg',
        # StreetCan
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCO8WCQsddotuNAH6-Pb_A0Q',
        # Therapy in a Nutshell
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCpuqYFKLkcEryEieomiAv3Q',
        # CaspianReport
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCwnKziETDbHJtx78nIkfYug',
        # Ethan Chlebowski
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCDq5v10l4wkV5-ZBIJJFbzQ',
        # Joel Haver
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCVIFCOJwv3emlVmBbPCZrvw',
        # Lex Clips
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCJIfeSCssxSC_Dhc5s7woww',
        # TLDR News EU
        'https://www.youtube.com/feeds/videos.xml?channel_id=UC-eegKVWEgBCa4OzjnK_PtA',
        # shiey
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCpXwMqnXfJzazKS5fJ8nrVw',
        # Yes Theory
        'https://www.youtube.com/feeds/videos.xml?channel_id=UCvK4bOhULCpmLabd2pDMtnA'
    ]

    processed_entry_ids = set()

    for url in atom_feed_urls:
        # Initial run to process existing entries in all urls
        feed = feedparser.parse(url)

        if feed.bozo:
            print('Error parsing feed:', feed.bozo_exception)
            return

        # Add all entry IDs to the set before processing
        for entry in feed.entries:
            entry_id = entry.id
            print(entry_id)
            processed_entry_ids.add(entry_id)

    while True:
        for url in atom_feed_urls:

            feed = feedparser.parse(url)

            if feed.bozo:
                print('Error parsing feed:', feed.bozo_exception)
                return

            if feed.entries:
                for entry in feed.entries:
                    entry_id = entry.id

                    # Check if entry ID has been processed
                    if entry_id not in processed_entry_ids:
                        send_slack_message(entry.link, entry.author)
                        # Remove entry ID from the set to avoid printing it again
                        processed_entry_ids.add(entry_id)
            else:
                print('No entries found in the feed.')

        # Sleep for the specified interval before fetching the feed again
        print('Loop ended, sleeping for 15 minutes....')
        time.sleep(interval_minutes * 60)

if __name__ == "__main__":
    parse_atom_feed()
