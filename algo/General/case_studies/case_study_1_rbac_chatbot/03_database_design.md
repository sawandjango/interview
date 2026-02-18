# Question 3: Database Design for Conversations

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟢 Core Concept

## 📝 Question

### Setup

You need to design a database schema for storing chatbot conversations. Each conversation has:

- Multiple messages (back and forth between user and bot)
- Message metadata (timestamp, sender, status)
- Conversation branching (user can edit previous messages and create new branches)
- File attachments (images, PDFs)
- Conversation metadata (title, created_at, last_updated, tags)
- User permissions (who can view/edit)

**Questions:**

1. **MongoDB or PostgreSQL?** Defend your choice.
2. **Design the schema** for your chosen database.
3. **How do you handle branching?** (User edits message #3, conversation splits into two paths)
4. **How do you query "last 20 conversations for user"** efficiently?

---

## 🎓 What I'm Looking For

- Understanding of relational vs document database trade-offs
- Schema design skills (normalization, indexing)
- Handling of hierarchical data (conversation trees)
- Query optimization thinking
- Scalability considerations

---

## ✅ Good Answer Should Include

### Part 1: MongoDB vs PostgreSQL

**My Recommendation: MongoDB (with caveats)**

```
Why MongoDB fits better:
──────────────────────────
1. Conversations are naturally nested/hierarchical
   - Conversation → Messages → Attachments
   - This maps well to embedded documents

2. Schema flexibility
   - Different message types (text, image, code, chart)
   - Metadata can vary per conversation
   - Easy to add new fields without migrations

3. Fast writes for chat (append-only workload)
   - Each new message is an array push
   - No joins needed to fetch conversation

4. Branching is easier
   - Store conversation as a tree structure
   - Each branch is a separate path in the tree

When PostgreSQL is better:
─────────────────────────
✓ Complex queries across conversations
✓ Strong consistency requirements (financial transactions)
✓ Need ACID guarantees for multi-step operations
✓ Heavy use of JOINs (user analytics, reporting)
✓ Team is more familiar with SQL
```

### Part 2: MongoDB Schema Design

**Option 1: Embedded Messages (Recommended for < 1000 messages)**

```javascript
// conversations collection
{
  _id: ObjectId("..."),
  user_id: "user123",
  title: "Q1 Sales Analysis",
  created_at: ISODate("2024-11-02T10:00:00Z"),
  updated_at: ISODate("2024-11-02T14:30:00Z"),
  tags: ["sales", "q1", "urgent"],
  permissions: {
    owner: "user123",
    viewers: ["user456", "user789"],
    editors: []
  },

  // Embedded messages array
  messages: [
    {
      message_id: "msg1",
      parent_id: null,  // Root message
      sender: "user",
      content: "What were Q1 sales?",
      timestamp: ISODate("2024-11-02T10:00:00Z"),
      attachments: [
        {
          type: "pdf",
          filename: "report.pdf",
          url: "s3://bucket/files/abc123.pdf",
          size_bytes: 1048576
        }
      ],
      branch_path: [0]  // Index path in tree
    },
    {
      message_id: "msg2",
      parent_id: "msg1",
      sender: "bot",
      content: "Q1 sales were $1.2M...",
      timestamp: ISODate("2024-11-02T10:00:05Z"),
      attachments: [],
      branch_path: [0, 0]
    },
    {
      message_id: "msg3",
      parent_id: "msg2",
      sender: "user",
      content: "Show breakdown by region",
      timestamp: ISODate("2024-11-02T10:01:00Z"),
      attachments: [],
      branch_path: [0, 0, 0]
    },
    // User edits msg3, creates branch
    {
      message_id: "msg3_v2",
      parent_id: "msg2",  // Same parent
      sender: "user",
      content: "Show breakdown by product",  // Different question
      timestamp: ISODate("2024-11-02T10:05:00Z"),
      attachments: [],
      branch_path: [0, 0, 1]  // Different branch
    }
  ],

  // Metadata
  message_count: 4,
  active_branch: [0, 0, 1]  // Currently viewing this path
}
```

**Indexes:**
```javascript
db.conversations.createIndex({ user_id: 1, updated_at: -1 })
db.conversations.createIndex({ "permissions.viewers": 1 })
db.conversations.createIndex({ tags: 1 })
```

**Pros of embedded:**
- ✅ Single query to fetch entire conversation
- ✅ Atomic updates (one document)
- ✅ Fast for chat UI (no joins)

**Cons:**
- ❌ 16MB document size limit
- ❌ Hard to query individual messages
- ❌ Inefficient for very long conversations

**Option 2: Separate Messages Collection (For > 1000 messages)**

```javascript
// conversations collection
{
  _id: ObjectId("conv123"),
  user_id: "user123",
  title: "Q1 Sales Analysis",
  created_at: ISODate("2024-11-02T10:00:00Z"),
  updated_at: ISODate("2024-11-02T14:30:00Z"),
  message_count: 1500,
  latest_message_id: "msg1500"
}

// messages collection (separate)
{
  _id: ObjectId("msg123"),
  conversation_id: ObjectId("conv123"),
  message_id: "msg1",
  parent_id: null,
  sender: "user",
  content: "What were Q1 sales?",
  timestamp: ISODate("2024-11-02T10:00:00Z"),
  branch_path: [0],
  attachments: [...]
}
```

**Indexes:**
```javascript
db.messages.createIndex({ conversation_id: 1, timestamp: 1 })
db.messages.createIndex({ conversation_id: 1, branch_path: 1 })
```

### Part 3: Handling Branching

**Strategy: Branch Path Array**

```
Conversation tree visualization:

msg1 (root)
  ├─ msg2
  │   ├─ msg3 (original)
  │   │   └─ msg4
  │   └─ msg3_v2 (edited branch)
  │       └─ msg5
  └─ msg2_v2 (alternative)
      └─ msg6

Branch paths:
msg1:      [0]
msg2:      [0, 0]
msg3:      [0, 0, 0]
msg4:      [0, 0, 0, 0]
msg3_v2:   [0, 0, 1]  ← Alternative branch
msg5:      [0, 0, 1, 0]
msg2_v2:   [0, 1]     ← Alternative branch
msg6:      [0, 1, 0]
```

**Implementation:**

```python
def get_active_branch(conversation_id, branch_path):
    """
    Fetch all messages in a specific branch
    Example: branch_path = [0, 0, 1] gets msgs: msg1 → msg2 → msg3_v2
    """
    messages = db.messages.find({
        "conversation_id": conversation_id,
        "branch_path": {"$regex": f"^{','.join(map(str, branch_path))}"}
    }).sort("timestamp", 1)

    return list(messages)

def create_branch(conversation_id, parent_message_id, new_content):
    """
    User edits a message, creating a new branch
    """
    # Get parent message
    parent = db.messages.find_one({"message_id": parent_message_id})

    # Calculate new branch path
    # If parent has path [0, 0, 0], and already has 1 child,
    # new branch is [0, 0, 1]
    siblings_count = db.messages.count_documents({
        "conversation_id": conversation_id,
        "parent_id": parent_message_id
    })

    new_branch_path = parent["branch_path"] + [siblings_count]

    # Create new message
    new_message = {
        "message_id": generate_id(),
        "conversation_id": conversation_id,
        "parent_id": parent_message_id,
        "sender": "user",
        "content": new_content,
        "timestamp": datetime.now(),
        "branch_path": new_branch_path
    }

    db.messages.insert_one(new_message)

    return new_message
```

### Part 4: Query "Last 20 Conversations"

```python
def get_recent_conversations(user_id, limit=20):
    """
    Fetch last 20 conversations for a user
    Sorted by most recently updated
    """
    conversations = db.conversations.find(
        {
            "$or": [
                {"user_id": user_id},
                {"permissions.viewers": user_id},
                {"permissions.editors": user_id}
            ]
        }
    ).sort("updated_at", -1).limit(limit)

    return list(conversations)

# Index makes this fast:
# db.conversations.createIndex({ user_id: 1, updated_at: -1 })
# db.conversations.createIndex({ "permissions.viewers": 1, updated_at: -1 })
```

**For embedded messages approach:**

```python
def get_conversations_with_preview(user_id, limit=20):
    """
    Get conversations with latest message preview
    """
    conversations = db.conversations.aggregate([
        {
            "$match": {
                "$or": [
                    {"user_id": user_id},
                    {"permissions.viewers": user_id}
                ]
            }
        },
        {"$sort": {"updated_at": -1}},
        {"$limit": limit},
        {
            "$project": {
                "title": 1,
                "updated_at": 1,
                "message_count": 1,
                # Get last message only
                "latest_message": {"$arrayElemAt": ["$messages", -1]}
            }
        }
    ])

    return list(conversations)
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Not planning for document size limit

```javascript
// ❌ Bad: Unbounded array growth
{
  messages: [
    // ... 10,000 messages → exceeds 16MB!
  ]
}

// ✅ Good: Cap embedded messages or use separate collection
{
  messages: [...],  // Max 1000 messages
  overflow_messages_collection: "messages_overflow"
}
```

### Mistake 2: No indexes on permissions

```javascript
// ❌ Bad: Slow query for shared conversations
db.conversations.find({ "permissions.viewers": "user123" })
// → Full collection scan!

// ✅ Good: Index on nested field
db.conversations.createIndex({ "permissions.viewers": 1 })
```

### Mistake 3: Not using projection

```python
# ❌ Bad: Fetching entire conversation when you only need metadata
conversations = db.conversations.find({"user_id": user_id})
# → Loads all messages (megabytes of data!)

# ✅ Good: Project only needed fields
conversations = db.conversations.find(
    {"user_id": user_id},
    {"title": 1, "updated_at": 1, "message_count": 1}
)
```

### Mistake 4: Not handling attachment storage

```javascript
// ❌ Bad: Storing file content in MongoDB
{
  attachments: [
    {
      filename: "report.pdf",
      content: "<base64 encoded 50MB file>"  // NO!
    }
  ]
}

// ✅ Good: Store in S3, reference in MongoDB
{
  attachments: [
    {
      filename: "report.pdf",
      url: "s3://bucket/files/abc123.pdf",
      size_bytes: 52428800,
      content_type: "application/pdf"
    }
  ]
}
```

---

## 🤔 Follow-Up Questions

### Q1: "How do you handle deleted messages?"

**Good Answer:**
```javascript
// Option 1: Soft delete (recommended)
{
  message_id: "msg3",
  content: "[Message deleted by user]",
  deleted: true,
  deleted_at: ISODate("2024-11-02T15:00:00Z"),
  original_content_backup: "Original text...",  // For audit
}

// Option 2: Hard delete (problematic for branching)
// Don't do this - breaks parent_id references!

// Option 3: Mark as deleted but keep in tree
{
  message_id: "msg3",
  content: null,
  deleted: true,
  // Keep parent_id and branch_path intact
  parent_id: "msg2",
  branch_path: [0, 0, 0]
}

Why soft delete is better:
✓ Preserves conversation tree structure
✓ Allows "undo delete"
✓ Keeps audit trail
✓ Branch paths remain valid
```

### Q2: "How do you handle search across conversations?"

**Good Answer:**
```javascript
// Option 1: MongoDB text index
db.conversations.createIndex({
  "title": "text",
  "messages.content": "text"
})

// Search
db.conversations.find({
  $text: { $search: "Q1 sales revenue" }
})

// Option 2: Elasticsearch (better for large scale)
// Index conversation data in Elasticsearch
POST /conversations/_search
{
  "query": {
    "multi_match": {
      "query": "Q1 sales",
      "fields": ["title", "messages.content"]
    }
  },
  "highlight": {
    "fields": {
      "messages.content": {}
    }
  }
}

// Option 3: Vector embeddings for semantic search
{
  message_id: "msg3",
  content: "What were Q1 sales?",
  embedding: [0.12, -0.45, ...],  // 1536-dim vector
}

// Query with vector similarity
db.messages.aggregate([
  {
    "$vectorSearch": {
      "queryVector": user_query_embedding,
      "path": "embedding",
      "numCandidates": 100,
      "limit": 10
    }
  }
])
```

### Q3: "How do you handle conversation sharing between users?"

**Good Answer:**
```javascript
{
  _id: ObjectId("conv123"),
  user_id: "user123",  // Owner
  permissions: {
    owner: "user123",

    // Can view only
    viewers: ["user456", "user789"],

    // Can edit and add messages
    editors: ["user999"],

    // Public link (anyone with link can view)
    public_access: {
      enabled: true,
      access_token: "abc123xyz",  // Secret token
      expires_at: ISODate("2024-12-31T23:59:59Z")
    },

    // Organization-wide access
    org_access: {
      org_id: "org456",
      role: "viewer"  // All org members can view
    }
  }
}

// Query: Find all conversations user can access
db.conversations.find({
  "$or": [
    {"user_id": user_id},  // Owner
    {"permissions.viewers": user_id},  // Explicit viewer
    {"permissions.editors": user_id},  // Explicit editor
    {
      "permissions.org_access.org_id": user_org_id,
      "permissions.org_access.role": {"$in": ["viewer", "editor"]}
    }
  ]
})

// Index for performance
db.conversations.createIndex({ "permissions.viewers": 1 })
db.conversations.createIndex({ "permissions.editors": 1 })
db.conversations.createIndex({ "permissions.org_access.org_id": 1 })
```

---

## 📊 MongoDB vs PostgreSQL Comparison

| Factor | MongoDB | PostgreSQL |
|--------|---------|------------|
| **Nested data** | ⭐⭐⭐⭐⭐ Native | ⭐⭐⭐ JSONB |
| **Schema flexibility** | ⭐⭐⭐⭐⭐ Schemaless | ⭐⭐ Migrations |
| **Consistency** | ⭐⭐⭐ Eventual | ⭐⭐⭐⭐⭐ ACID |
| **Joins** | ⭐⭐ $lookup | ⭐⭐⭐⭐⭐ Native |
| **Full-text search** | ⭐⭐⭐ Basic | ⭐⭐⭐⭐ Advanced |
| **Horizontal scaling** | ⭐⭐⭐⭐⭐ Sharding | ⭐⭐⭐ Complex |

---

## 💡 Key Takeaways

1. **Choose MongoDB for conversations**
   - Naturally nested data structure
   - Fast writes (chat is append-heavy)
   - Schema flexibility for different message types

2. **Use embedded documents for small conversations**
   - < 1000 messages → embed
   - > 1000 messages → separate collection

3. **Branch path arrays work well**
   - Easy to query specific branches
   - Preserves tree structure
   - Simple to understand

4. **Always index permissions**
   - Users query "my conversations" frequently
   - Shared conversations need fast lookup

5. **Store files externally**
   - S3 for attachments
   - Only reference URLs in database

6. **Plan for search early**
   - Text indexes for basic search
   - Elasticsearch for advanced search
   - Vector embeddings for semantic search

---

## 🔗 Related Questions

- [Question 5: Cache Invalidation Strategy](./05_cache_invalidation.md)
- [Question 6: Multi-Tenancy & Data Isolation](./06_multi_tenancy.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./04_async_processing.md)
