# Selective Memory Deletion System - TASK-025

## Overview

The Selective Memory Deletion System provides AI-first privacy control with natural language deletion interfaces. It enables users to selectively remove memories using conversational commands while maintaining data integrity and providing recovery options.

## Key Features

### 1. Natural Language Deletion Interface
Users can request deletions using natural language:
- "Forget everything about TechCorp"
- "Delete conversations from last week"
- "Remove all Python-related memories"
- "Clear my interview data"

### 2. Multiple Deletion Strategies

#### Entity Deletion
Remove all data about specific companies, people, or entities:
```python
interface.delete("forget everything about Company X")
```

#### Time Range Deletion
Delete memories from specific time periods:
```python
interface.delete("delete everything from 30 days ago")
interface.delete("remove data from 2024-01-01 to 2024-01-15")
```

#### Topic Deletion
Remove memories related to specific topics:
```python
interface.delete("delete all salary negotiation conversations")
interface.delete("forget about machine learning jobs")
```

#### Conversation Deletion
Delete specific conversations or current session:
```python
interface.delete("delete this conversation")
interface.delete("forget the discussion about benefits")
```

#### Pattern-Based Deletion
Delete using regex patterns:
```python
interface.delete("remove anything matching 'confidential.*project'")
```

#### Nuclear Option
Complete memory wipe (requires confirmation):
```python
interface.delete("delete everything")  # Requires confirmation token
```

### 3. Confirmation Mechanisms

High-impact deletions require explicit confirmation:
```python
# Request deletion
result = interface.delete("delete everything")
if result['requires_confirmation']:
    # Confirm with token
    success = interface.confirm(result['request_id'], result['confirmation_token'])
```

### 4. Recovery Window

Deleted memories can be recovered within a configurable time window:
```python
# Delete with 24-hour recovery window
result = interface.delete("forget about StartupXYZ", confirm=True)

# Later, recover the deletion
recovered = interface.undo(result['request_id'])
```

### 5. Secure Deletion

Implements data overwriting for true deletion:
- Memory content replaced with random data
- Embeddings overwritten with noise
- All indices cleared
- No trace left in system

### 6. Cascading Deletion

Automatically removes related memories:
- Memories referencing deleted content
- Memories with significant tag overlap
- Memories from same conversation timeframe

### 7. Scheduled Deletion

Set up automatic future deletions:
```python
# Delete after 30 days
scheduled = interface.schedule("delete all interview data", hours_from_now=720)
```

### 8. Deletion Analytics

Privacy-preserving analytics about deletion patterns:
```python
analytics = interface.analytics()
# Returns:
# - Privacy score (0-1)
# - Recent deletion count
# - Scheduled deletions
# - Recoverable deletions
```

## Architecture

### Core Components

1. **SelectiveMemoryDeletion**: Main deletion system
2. **NaturalLanguageParser**: Parses deletion requests
3. **DeletionInterface**: User-friendly API
4. **DeletionRequest**: Tracks deletion operations
5. **DeletionAuditEntry**: Audit trail

### Integration with Agent Memory System

The deletion system integrates seamlessly with the existing agent memory management:

```python
# Create memory system
memory_system = AgentMemorySystem()

# Create deletion system
deletion_system = SelectiveMemoryDeletion(memory_system)

# Create interface
interface = DeletionInterface(deletion_system)
```

## Usage Examples

### Basic Entity Deletion
```python
# Delete all memories about a company
result = interface.delete("forget everything about TechCorp", confirm=True)
```

### Time-Based Cleanup
```python
# Delete old data
result = interface.delete("delete memories older than 30 days", confirm=True)
```

### Privacy Conversation
```python
assistant = PrivacyAssistant(memory_system)

# User asks about their data
response = assistant.process_privacy_request("What do you know about me?")

# User requests deletion
response = assistant.process_privacy_request("Forget about my rejection from Google")
```

### Scheduled Auto-Deletion
```python
# Set up recurring cleanup
interface.schedule("delete conversations older than 7 days", hours_from_now=168)
```

## Natural Language Patterns

The system recognizes various deletion patterns:

### Entity Patterns
- "forget [everything] about [entity]"
- "delete [all] [memories/data] [about/from] [entity]"
- "remove [all] information [about/from] [entity]"
- "erase [all] [data/memories] [about/from] [entity]"

### Time Patterns
- "delete [everything/data] from [date]"
- "forget [everything/all] [from/since] [time expression]"
- "remove [memories/data] older than [duration]"
- "clear [all] [history/memories] [from/since] [date]"

### Topic Patterns
- "forget [all] [about/related to] [topic]"
- "delete [all] [topic] related [conversations/memories]"
- "remove [all] information about [topic]"
- "clear [all] [topic] [data/content/memories]"

## Privacy Best Practices

### 1. Regular Cleanup
Schedule automatic deletion of old data:
```python
# Weekly cleanup of old conversations
interface.schedule("delete conversations older than 30 days", hours_from_now=168)
```

### 2. Confirmation for Large Deletions
Always require confirmation for deletions affecting >100 memories

### 3. Recovery Windows
Keep 24-48 hour recovery windows for non-critical deletions

### 4. Audit Trail
All deletions are logged with:
- Timestamp
- Affected memory count
- Deletion strategy used
- User who requested
- Recovery availability

### 5. Secure Deletion by Default
Use secure overwriting for sensitive data

## Conversational Integration

The system integrates naturally into conversational AI:

```python
class PrivacyAssistant:
    def process_privacy_request(self, user_input: str) -> str:
        # Detect privacy intent
        # Parse deletion request
        # Provide appropriate response
        # Handle confirmations
```

Example conversation:
```
User: "I don't want you to remember anything about my interview at Google"
Assistant: "I understand. I found 3 memories related to your Google interview. 
           Would you like me to delete them? You'll have 24 hours to undo if needed."
User: "Yes, delete them"
Assistant: "✅ Done. I've deleted all Google interview information. 
           Say 'undo last deletion' within 24 hours if you change your mind."
```

## Security Considerations

1. **Authentication**: Ensure user identity before allowing deletions
2. **Rate Limiting**: Prevent mass deletion attacks
3. **Backup Strategy**: Consider external backups for critical data
4. **Compliance**: Align with GDPR/CCPA requirements
5. **Encryption**: Encrypt recovery storage

## Performance Optimization

1. **Batch Deletions**: Process multiple deletions together
2. **Index Cleanup**: Regularly clean orphaned indices
3. **Async Processing**: Handle large deletions asynchronously
4. **Memory Limits**: Set limits on recovery storage size

## Future Enhancements

1. **ML-Based Deletion Suggestions**: Proactively suggest data cleanup
2. **Differential Privacy**: Add noise to deletion analytics
3. **Federated Deletion**: Coordinate deletions across distributed systems
4. **Smart Cascading**: ML-powered related data detection
5. **Deletion Templates**: Pre-configured deletion patterns

## API Reference

### DeletionInterface Methods

```python
# Basic deletion
delete(query: str, confirm: bool = False) -> Dict[str, Any]

# Confirm with token
confirm(request_id: str, token: str) -> bool

# Undo deletion
undo(request_id: str) -> bool

# Schedule deletion
schedule(query: str, hours_from_now: int) -> Dict[str, Any]

# Get analytics
analytics() -> Dict[str, Any]
```

### Response Format

```python
{
    "request_id": "del_12345",
    "understood_as": "entity",  # Deletion strategy
    "will_delete": 42,          # Number of memories
    "summary": {                # Deletion summary
        "by_type": {...},
        "by_agent": {...},
        "date_range": {...}
    },
    "requires_confirmation": False,
    "confirmation_token": None
}
```

## Conclusion

The Selective Memory Deletion System provides comprehensive privacy control through natural language interfaces. It balances user privacy with system functionality, offering fine-grained control over data retention while maintaining usability through conversational interactions.