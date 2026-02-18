# Question 8: GDPR Right to be Forgotten

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🔴 Advanced

## 📝 Question

### Setup

A user in the EU exercises their **GDPR "Right to be Forgotten"**. They want ALL their data deleted:

- Conversations (10,000 messages)
- Uploaded files (PDFs, images)
- Audit logs
- Cached data (Redis)
- Database backups
- Log files on servers
- ML training data

**Legal requirement:** Complete deletion within **30 days**, verifiable via audit.

**The Challenge:**

```python
# Naive approach
db.conversations.delete_many({"user_id": user_id})  # ❌ Not enough!
```

**Questions:**

1. How do you ensure COMPLETE deletion across all systems?
2. How do you handle backups? (Can't just delete from backups!)
3. How do you prove deletion to auditors?
4. What data can you legally keep?

---

## 🎓 What I'm Looking For

- Understanding of GDPR requirements
- Handling of backups and archives
- Soft delete vs hard delete trade-offs
- Audit trail requirements
- Exception handling (what data you can keep)

---

## ✅ Good Answer Should Include

### Step 1: Soft Delete First (Immediate)

```python
from datetime import datetime, timedelta

@app.route('/api/user/delete-request', methods=['POST'])
@require_auth
def request_deletion(user_id):
    """
    User requests account deletion
    """
    # Mark user for deletion (immediate)
    db.users.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "deletion_requested": datetime.now(),
                "deletion_scheduled": datetime.now() + timedelta(days=30),
                "status": "pending_deletion"
            }
        }
    )

    # Immediately revoke access
    revoke_all_tokens(user_id)

    # Send confirmation email
    send_email(user_id, "Your deletion request has been received")

    return {"status": "Deletion scheduled for 30 days"}


# Middleware blocks deleted users
def require_active_user(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        user = db.users.find_one({"user_id": kwargs['user_id']})

        if user.get('status') == 'pending_deletion':
            return {"error": "Account scheduled for deletion"}, 403

        return f(*args, **kwargs)
    return decorated
```

### Step 2: Complete Data Deletion (Batch Job)

```python
class UserDataDeletion:
    """
    Comprehensive user data deletion
    """

    def __init__(self, user_id):
        self.user_id = user_id
        self.deletion_log = []

    def execute(self):
        """
        Delete all user data across systems
        """
        try:
            # 1. Delete conversations
            self._delete_conversations()

            # 2. Delete uploaded files
            self._delete_files()

            # 3. Delete cache
            self._delete_cache()

            # 4. Anonymize audit logs
            self._anonymize_audit_logs()

            # 5. Remove from ML training data
            self._remove_from_ml_data()

            # 6. Delete user profile
            self._delete_user_profile()

            # 7. Mark backups for exclusion
            self._mark_backups()

            # 8. Create deletion certificate
            self._create_deletion_certificate()

            return {"status": "completed", "log": self.deletion_log}

        except Exception as e:
            logger.error(f"Deletion failed for {self.user_id}: {e}")
            raise

    def _delete_conversations(self):
        """Delete all conversations and messages"""
        # Get all conversations
        conversations = db.conversations.find({"user_id": self.user_id})
        conv_ids = [c['_id'] for c in conversations]

        # Delete messages
        result = db.messages.delete_many({"conversation_id": {"$in": conv_ids}})
        self.deletion_log.append({
            "step": "delete_messages",
            "count": result.deleted_count,
            "timestamp": datetime.now()
        })

        # Delete conversations
        result = db.conversations.delete_many({"user_id": self.user_id})
        self.deletion_log.append({
            "step": "delete_conversations",
            "count": result.deleted_count,
            "timestamp": datetime.now()
        })

    def _delete_files(self):
        """Delete uploaded files from S3"""
        # Get all file references
        files = db.files.find({"user_id": self.user_id})

        for file in files:
            # Delete from S3
            s3_client.delete_object(
                Bucket='chatbot-uploads',
                Key=file['s3_key']
            )

            self.deletion_log.append({
                "step": "delete_file",
                "file_id": file['file_id'],
                "s3_key": file['s3_key']
            })

        # Delete file metadata
        db.files.delete_many({"user_id": self.user_id})

    def _delete_cache(self):
        """Delete cached data from Redis"""
        # Find all cache keys for this user
        pattern = f"*:{self.user_id}:*"
        cursor = 0
        deleted = 0

        while True:
            cursor, keys = redis_client.scan(cursor, match=pattern, count=100)
            if keys:
                redis_client.delete(*keys)
                deleted += len(keys)
            if cursor == 0:
                break

        self.deletion_log.append({
            "step": "delete_cache",
            "keys_deleted": deleted
        })

    def _anonymize_audit_logs(self):
        """
        Anonymize audit logs (can't delete - needed for security)
        """
        # Replace user_id with anonymized version
        anonymized_id = f"deleted_user_{hashlib.sha256(self.user_id.encode()).hexdigest()[:16]}"

        db.audit_logs.update_many(
            {"user_id": self.user_id},
            {
                "$set": {
                    "user_id": anonymized_id,
                    "anonymized": True,
                    "anonymized_at": datetime.now()
                },
                "$unset": {
                    "email": "",
                    "name": "",
                    "ip_address": ""
                }
            }
        )

        self.deletion_log.append({
            "step": "anonymize_audit_logs",
            "anonymized_id": anonymized_id
        })

    def _remove_from_ml_data(self):
        """
        Remove user data from ML training datasets
        """
        # Mark user queries as excluded from future training
        db.ml_training_data.update_many(
            {"user_id": self.user_id},
            {"$set": {"excluded": True, "reason": "user_deletion"}}
        )

        # Trigger model retraining (if user data was significant)
        user_query_count = db.ml_training_data.count_documents({"user_id": self.user_id})
        if user_query_count > 1000:
            trigger_model_retraining()

        self.deletion_log.append({
            "step": "remove_ml_data",
            "queries_excluded": user_query_count
        })

    def _delete_user_profile(self):
        """Delete user profile (final step)"""
        db.users.delete_one({"user_id": self.user_id})

        self.deletion_log.append({
            "step": "delete_user_profile",
            "user_id": self.user_id
        })

    def _mark_backups(self):
        """
        Mark user in backup exclusion list
        Backups will exclude this user on restore
        """
        db.backup_exclusions.insert_one({
            "user_id": self.user_id,
            "excluded_at": datetime.now(),
            "reason": "gdpr_deletion"
        })

        self.deletion_log.append({
            "step": "mark_backups",
            "user_id": self.user_id
        })

    def _create_deletion_certificate(self):
        """
        Create audit certificate proving deletion
        """
        certificate = {
            "user_id": self.user_id,
            "deletion_completed_at": datetime.now(),
            "deletion_log": self.deletion_log,
            "certificate_id": str(uuid.uuid4()),
            "verified_by": "automated_system"
        }

        db.deletion_certificates.insert_one(certificate)

        self.deletion_log.append({
            "step": "create_certificate",
            "certificate_id": certificate['certificate_id']
        })


# Daily batch job
def process_pending_deletions():
    """
    Run daily: Delete users whose 30-day grace period expired
    """
    cutoff = datetime.now()

    pending_users = db.users.find({
        "status": "pending_deletion",
        "deletion_scheduled": {"$lte": cutoff}
    })

    for user in pending_users:
        logger.info(f"Processing deletion for user {user['user_id']}")

        deleter = UserDataDeletion(user['user_id'])
        result = deleter.execute()

        logger.info(f"Deletion completed: {result}")

        # Send confirmation
        send_email(user['email'], "Your data has been deleted")
```

### Step 3: Handling Backups

**Problem:** Can't delete data from existing backups (they're immutable!)

**Solution: Backup Exclusion List**

```python
def restore_from_backup(backup_date):
    """
    Restore database from backup, excluding deleted users
    """
    # Get exclusion list (users deleted AFTER backup date)
    excluded_users = db.backup_exclusions.find({
        "excluded_at": {"$gt": backup_date}
    })

    excluded_user_ids = [u['user_id'] for u in excluded_users]

    # Restore backup
    restore_database(backup_date)

    # Re-delete excluded users
    for user_id in excluded_user_ids:
        logger.info(f"Re-deleting user {user_id} (was in backup)")
        deleter = UserDataDeletion(user_id)
        deleter.execute()

    logger.info(f"Restored backup with {len(excluded_user_ids)} users re-deleted")
```

**Alternative: Encrypted Backups with Key Destruction**

```python
# Each user's data encrypted with unique key
def backup_user_data(user_id):
    user_data = get_all_user_data(user_id)

    # Generate unique encryption key
    encryption_key = generate_key()

    # Encrypt data
    encrypted_data = encrypt(user_data, encryption_key)

    # Store encrypted data in backup
    store_backup(encrypted_data)

    # Store key separately
    db.encryption_keys.insert_one({
        "user_id": user_id,
        "key": encryption_key,
        "created_at": datetime.now()
    })


def delete_user_with_key_destruction(user_id):
    # Delete data
    delete_all_data(user_id)

    # Destroy encryption key
    db.encryption_keys.delete_one({"user_id": user_id})

    # Now backup is useless (can't decrypt without key)
```

---

## 🔴 Common Mistakes to Avoid

### Mistake 1: Not anonymizing audit logs

```python
# ❌ Bad: Delete audit logs entirely
db.audit_logs.delete_many({"user_id": user_id})
# Violates security requirements!

# ✅ Good: Anonymize but keep logs
db.audit_logs.update_many(
    {"user_id": user_id},
    {"$set": {"user_id": "anonymized_user_xyz"}}
)
# Can still detect security issues without PII
```

### Mistake 2: Forgetting third-party systems

```python
# ❌ Bad: Only delete from your database
delete_from_mongo(user_id)

# ✅ Good: Delete from all systems
delete_from_mongo(user_id)
delete_from_redis(user_id)
delete_from_s3(user_id)
delete_from_elasticsearch(user_id)
delete_from_analytics(user_id)  # Google Analytics, Mixpanel, etc.
delete_from_crm(user_id)  # Salesforce, HubSpot, etc.
```

### Mistake 3: No proof of deletion

```python
# ❌ Bad: Just delete, no audit trail
db.users.delete_one({"user_id": user_id})

# ✅ Good: Create deletion certificate
certificate = {
    "user_id": user_id,
    "deleted_at": datetime.now(),
    "deleted_data": [
        {"type": "conversations", "count": 1500},
        {"type": "files", "count": 45},
        {"type": "cache_keys", "count": 230}
    ],
    "certificate_id": uuid.uuid4()
}
db.deletion_certificates.insert_one(certificate)
```

---

## 🤔 Follow-Up Questions

### Q1: "What data can you legally keep under GDPR?"

**Good Answer:**
```
Data you CAN keep:
────────────────────
1. Anonymized audit logs (no PII)
   - "User X logged in at 10:00 AM" → "anonymized_user_abc logged in at 10:00 AM"

2. Aggregated analytics
   - "Total messages sent: 10,000" (no individual data)

3. Financial records (legal requirement)
   - Invoices, payments (but only for 7 years)

4. Legal hold data
   - If user involved in ongoing lawsuit

5. Security incident data
   - If user was victim of attack (reasonable period)

Data you MUST delete:
────────────────────
1. Personal identifiers
   - Name, email, phone, address

2. User-generated content
   - Conversations, messages, comments

3. Behavioral data
   - Search history, click patterns

4. Biometric data
   - Voice recordings, photos
```

### Q2: "User deletes account, but their company still exists. What happens to shared conversations?"

**Good Answer:**
```python
# Scenario: User A (employee) deletes account
# Conversation X is shared between User A and User B (both at Company C)

def handle_shared_conversation_deletion(user_id):
    """
    Replace user data with placeholder in shared conversations
    """
    # Find conversations owned by user
    owned_conversations = db.conversations.find({"owner_id": user_id})

    for conv in owned_conversations:
        # Check if shared with others
        if conv.get('shared_with'):
            # Transfer ownership to first shared user
            new_owner = conv['shared_with'][0]

            db.conversations.update_one(
                {"_id": conv['_id']},
                {
                    "$set": {
                        "owner_id": new_owner,
                        "original_owner": "deleted_user"
                    },
                    "$pull": {"shared_with": user_id}
                }
            )

            # Anonymize user's messages in conversation
            db.messages.update_many(
                {
                    "conversation_id": conv['_id'],
                    "sender_id": user_id
                },
                {
                    "$set": {
                        "sender_id": "deleted_user",
                        "sender_name": "[Deleted User]"
                    }
                }
            )
        else:
            # Not shared - safe to delete
            db.conversations.delete_one({"_id": conv['_id']})
```

---

## 💡 Key Takeaways

1. **30-day grace period**
   - Soft delete immediately (revoke access)
   - Hard delete after 30 days
   - Allows undo if mistake

2. **Comprehensive deletion checklist**
   - Primary database
   - Cache (Redis)
   - File storage (S3)
   - Search indexes (Elasticsearch)
   - Third-party services
   - ML training data

3. **Backup exclusion list**
   - Can't delete from immutable backups
   - Maintain exclusion list
   - Re-delete on restore

4. **Anonymize don't delete**
   - Audit logs (security requirement)
   - Aggregated analytics
   - Keep structure, remove PII

5. **Audit trail is critical**
   - Deletion certificate with timestamp
   - Detailed log of what was deleted
   - Verifiable by external auditors

---

## 🔗 Related Questions

- [Question 6: Multi-Tenancy & Data Isolation](./06_multi_tenancy.md)
- [Question 9: Debugging Production Latency](./09_latency_debugging.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./09_latency_debugging.md)
