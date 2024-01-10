from telethon.sync import TelegramClient
from telethon import functions
from telethon.tl.types import ForumTopic

from dotenv import load_dotenv

import random

# Load environment variables from .env file
load_dotenv()

async def get_all_topics(channel_id: int, session: str, api_id: str, api_hash: str, get_pinned : bool = False) -> [ForumTopic] :
    async with TelegramClient(session, api_id, api_hash) as client:
        try:
            topics = []
            date = 0
            offset = 0
            offset_topic = 0
            total = 0

            while True:
                r = await client(functions.channels.GetForumTopicsRequest(
                    channel=channel_id,
                    offset_date=date,
                    offset_id=offset,
                    offset_topic=offset_topic,
                    limit=100,
                ))

                if not total:
                    total = r.count

                topic_list = r.topics
                if not topic_list or len(topics) >= total:
                    break

                topics.extend(topic_list)
                last = topic_list[-1]

                offset_topic, offset = last.id, last.top_message
                date = {m.id: m.date for m in r.messages}.get(offset, 0)

            filtered_topics = [topic for topic in topics if topic.pinned == get_pinned]
            return filtered_topics
             
        except Exception as e:
            print(f"Error: {type(e).__name__}: {e}")


def random_topics(count: int, topics: [ForumTopic]) -> [ForumTopic]:
    # Ensure we have at least num_topics non-pinned topics
    re_count = min(count, len(topics))

    # Randomly select num_topics from the non_pinned_topics list
    random_topics = random.sample(topics, re_count)

    return random_topics
