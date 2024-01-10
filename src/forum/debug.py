from telethon.types import ForumTopic

def debug_topics(topics: [ForumTopic]) -> None:
    for i, topic in enumerate(topics, start=1):
        print(f"{i} - ID: {topic.id} — {topic.title}")

    return