import os
import json
from azure.data.tables import TableServiceClient
from datetime import datetime


class MemoryManager:

    def __init__(self):
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

        self.conversation_table = "conversations"
        self.state_table = "sessionstate"

        if connection_string:
            service = TableServiceClient.from_connection_string(connection_string)

            self.convo_client = service.get_table_client(self.conversation_table)
            self.state_client = service.get_table_client(self.state_table)
        else:
            self.convo_client = None
            self.state_client = None

    # =====================================
    # Conversation Storage
    # =====================================

    def save_message(self, session_id, role, content):
        if not self.convo_client:
            return

        entity = {
            "PartitionKey": session_id,
            "RowKey": datetime.utcnow().isoformat(),
            "role": role,
            "content": content
        }

        self.convo_client.create_entity(entity=entity)

    def load_conversation(self, session_id):
        if not self.convo_client:
            return []

        entities = self.convo_client.query_entities(
            query_filter=f"PartitionKey eq '{session_id}'"
        )

        history = []
        for entity in entities:
            history.append({
                "role": entity["role"],
                "content": entity["content"],
                "timestamp": entity["RowKey"]
            })

        # Correct sorting by timestamp
        history.sort(key=lambda x: x["timestamp"])
        return history

    # =====================================
    # Session Mood State Storage
    # =====================================

    def load_state(self, session_id):
        if not self.state_client:
            return {"moodScores": []}

        try:
            entity = self.state_client.get_entity(
                partition_key=session_id,
                row_key="state"
            )

            return {
                "moodScores": json.loads(entity.get("moodScores", "[]"))
            }

        except:
            return {"moodScores": []}

    def save_state(self, session_id, mood_scores):
        if not self.state_client:
            return

        entity = {
            "PartitionKey": session_id,
            "RowKey": "state",
            "moodScores": json.dumps(mood_scores)
        }

        try:
            self.state_client.upsert_entity(entity=entity)
        except:
            pass

    # =====================================
    # Emotional Profile Storage (NEW)
    # =====================================

    def load_profile(self, session_id):
        if not self.state_client:
            return {}

        try:
            entity = self.state_client.get_entity(
                partition_key=session_id,
                row_key="profile"
            )

            return json.loads(entity.get("profileData", "{}"))

        except:
            return {}

    def save_profile(self, session_id, profile_data):
        if not self.state_client:
            return

        entity = {
            "PartitionKey": session_id,
            "RowKey": "profile",
            "profileData": json.dumps(profile_data)
        }

        try:
            self.state_client.upsert_entity(entity=entity)
        except:
            pass