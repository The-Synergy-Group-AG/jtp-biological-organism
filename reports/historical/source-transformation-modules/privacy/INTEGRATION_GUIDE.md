# Privacy System Integration Guide

## Overview

The privacy system in Job Tracker Pro consists of three interconnected components that work together to provide comprehensive privacy controls:

1. **Selective Memory Deletion** (TASK-025)
2. **Data Export System** (TASK-026)
3. **Ephemeral Conversation Mode** (TASK-027)

## Component Integration

### 1. Memory System Foundation

All privacy components build on the Agent Memory System:

```python
from agents.agent_memory_management import AgentMemorySystem

# Shared memory system instance
memory_system = AgentMemorySystem()

# Each privacy component uses the same memory system
deletion_system = SelectiveMemoryDeletion(memory_system)
export_system = DataExportSystem(memory_system)
ephemeral_mode = EphemeralConversation(memory_system)
```

### 2. Data Flow

```
User Request → Natural Language Parser → Privacy Component → Memory System
                                                ↓
                                          Sanitization
                                                ↓
                                          Output/Action
```

### 3. Integration Examples

#### Export Before Deletion
```python
# User wants to export data before deleting it
async def export_then_delete(query: str):
    # First, export the data
    export_result = export_interface.export(
        f"export {query} as encrypted backup"
    )
    
    # Then delete it
    deletion_result = deletion_interface.delete(
        f"delete {query}", 
        confirm=True
    )
    
    return {
        "exported": export_result,
        "deleted": deletion_result
    }
```

#### Privacy-Aware Exports
```python
# Export with automatic PII removal based on deletion history
def privacy_aware_export(export_options):
    # Check what user has previously deleted
    deletion_patterns = deletion_system.get_deletion_patterns()
    
    # Apply similar sanitization to exports
    if deletion_patterns.includes_pii:
        export_options.sanitization = SanitizationLevel.STRICT
    
    return export_system.export(export_options)
```

#### Ephemeral Mode Integration
```python
# In ephemeral mode, exports are temporary
class EphemeralExport:
    def export_temporarily(self, data):
        # Create export in memory only
        result = export_system.export_to_memory(data)
        
        # Auto-delete after download
        def cleanup():
            time.sleep(300)  # 5 minutes
            result.destroy()
        
        threading.Thread(target=cleanup).start()
        return result
```

## Privacy Levels

The system supports unified privacy levels across all components:

| Level | Deletion | Export | Ephemeral |
|-------|----------|---------|-----------|
| Basic | Recent data | Remove passwords | Short retention |
| Moderate | PII removal | Sanitize emails/phones | No persistence |
| Strict | Complete wipe | Remove all PII | RAM only |

## Natural Language Understanding

All components share the same NLP patterns:

```python
# Shared patterns
PRIVACY_PATTERNS = {
    'temporal': ['last week', 'yesterday', 'past month'],
    'entities': ['company', 'application', 'conversation'],
    'privacy': ['private', 'sanitize', 'secure', 'encrypt'],
    'actions': ['delete', 'export', 'forget', 'backup']
}
```

## Security Considerations

### Encryption Keys
- Same key derivation across all components
- User passphrase never stored
- Keys derived on-demand

### Audit Trail
- All privacy actions logged
- Unified audit format
- Privacy-preserving analytics

### Data Consistency
- Atomic operations
- Rollback support
- Recovery windows

## Best Practices

1. **Always Export Before Delete**
   ```python
   # Good practice
   export_id = await export_critical_data()
   await verify_export(export_id)
   await delete_data_safely()
   ```

2. **Use Templates for Consistency**
   ```python
   # Privacy template
   PRIVACY_TEMPLATE = {
       'export': {'sanitization': 'moderate'},
       'deletion': {'cascade': True},
       'ephemeral': {'duration': 300}
   }
   ```

3. **Implement Privacy by Default**
   ```python
   # Default to privacy-preserving options
   DEFAULT_OPTIONS = {
       'sanitization': SanitizationLevel.BASIC,
       'encryption': True,
       'audit': True
   }
   ```

## Testing Privacy Features

```python
# Comprehensive privacy test
async def test_privacy_integration():
    # 1. Create test data
    test_data = create_sensitive_test_data()
    
    # 2. Export with sanitization
    export_result = await export_system.export(
        ExportOptions(
            format=ExportFormat.JSON,
            sanitization=SanitizationLevel.STRICT
        )
    )
    
    # 3. Verify no PII in export
    assert not contains_pii(export_result.file_data)
    
    # 4. Delete selectively
    deletion_result = await deletion_system.delete(
        "forget all test data"
    )
    
    # 5. Verify deletion
    remaining_data = memory_system.search("test")
    assert len(remaining_data) == 0
```

## Future Enhancements

1. **Unified Privacy Dashboard**
   - Single interface for all privacy controls
   - Visual privacy score
   - One-click privacy actions

2. **Privacy Policies**
   - User-defined privacy rules
   - Automatic enforcement
   - Policy templates

3. **Cross-Component Sync**
   - Deletion triggers export
   - Export includes deletion history
   - Ephemeral mode affects both

## Support

For privacy-related questions:
- Use natural language queries
- Check audit logs for history
- Review privacy settings
- Contact privacy support team