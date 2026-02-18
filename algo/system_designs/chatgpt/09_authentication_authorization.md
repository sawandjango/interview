# Diagram 9: Authentication & Authorization

## Overview
Security layer handling user authentication, API key management, permissions, and access control throughout the system.

## Architecture Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║                   AUTHENTICATION FLOW                         ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────┐
│  Client/User    │
└────────┬────────┘
         │
         │ POST /auth/login
         │ {email, password}
         ▼
┌─────────────────────────────────────────────────────────────┐
│  Authentication Service                                     │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. Validate Credentials                                │ │
│  │                                                        │ │
│  │  - Hash password (bcrypt)                             │ │
│  │  - Compare with stored hash                           │ │
│  │  - Check account status (active, suspended, etc.)     │ │
│  │  - Rate limit: 5 attempts per 15 min                  │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 2. Multi-Factor Authentication (MFA)                  │ │
│  │                                                        │ │
│  │  Optional/Required based on user settings:            │ │
│  │  - TOTP (Google Authenticator)                        │ │
│  │  - SMS code                                           │ │
│  │  - Email code                                         │ │
│  │  - WebAuthn (YubiKey, Touch ID)                       │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 3. Generate Tokens                                     │ │
│  │                                                        │ │
│  │  Access Token (JWT):                                   │ │
│  │  {                                                     │ │
│  │    "user_id": "usr_123",                              │ │
│  │    "org_id": "org_789",                               │ │
│  │    "tier": "pro",                                     │ │
│  │    "scopes": ["chat:read", "chat:write"],             │ │
│  │    "exp": 1640995200  // 15 min expiry                │ │
│  │  }                                                     │ │
│  │  Signed with RS256 (private key)                       │ │
│  │                                                        │ │
│  │  Refresh Token:                                        │ │
│  │  - Opaque token (random 256-bit)                      │ │
│  │  - Stored in database with user_id                    │ │
│  │  - Expiry: 30 days                                    │ │
│  │  - Rotated on use (single-use)                        │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 4. Session Creation                                    │ │
│  │                                                        │ │
│  │  Store in Redis:                                       │ │
│  │  session:{token_id} → {                               │ │
│  │    user_id, org_id, ip, user_agent,                   │ │
│  │    created_at, last_activity                          │ │
│  │  }                                                     │ │
│  │  TTL: 15 minutes (access token lifetime)              │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          │ Return: {access_token, refresh_token}
                          ▼
                   ┌─────────────┐
                   │   Client    │
                   │ (stores in  │
                   │  secure     │
                   │  storage)   │
                   └─────────────┘


╔═══════════════════════════════════════════════════════════════╗
║                   AUTHORIZATION FLOW                          ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────┐
│  Client Request │
│  Authorization: │
│  Bearer <JWT>   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  API Gateway - JWT Validation                               │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 1. Token Validation                                    │ │
│  │                                                        │ │
│  │  - Extract JWT from Authorization header              │ │
│  │  - Verify signature (RS256 public key)                │ │
│  │  - Check expiry (exp claim)                           │ │
│  │  - Check not before (nbf claim)                       │ │
│  │  - Validate issuer (iss claim)                        │ │
│  │                                                        │ │
│  │  Public key caching (Redis):                          │ │
│  │  - Fetch from auth service once                       │ │
│  │  - Cache for 1 hour                                   │ │
│  │  - Refresh on rotation                                │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 2. Session Verification (Optional)                     │ │
│  │                                                        │ │
│  │  Check Redis session:                                  │ │
│  │  - session:{token_id} exists?                         │ │
│  │  - Not revoked?                                        │ │
│  │  - Update last_activity                               │ │
│  │                                                        │ │
│  │  Skip for performance (rely on JWT expiry)            │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ 3. Extract User Context                                │ │
│  │                                                        │ │
│  │  From JWT claims:                                      │ │
│  │  - user_id                                            │ │
│  │  - org_id                                             │ │
│  │  - tier (free, pro, enterprise)                       │ │
│  │  - scopes (permissions)                               │ │
│  │                                                        │ │
│  │  Inject into request context for downstream services  │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  Downstream Services - Authorization Checks                 │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Permission Checks (Scope-based)                        │ │
│  │                                                        │ │
│  │  Required scopes by endpoint:                          │ │
│  │  - POST /v1/chat/completions → chat:write             │ │
│  │  - GET /v1/conversations → chat:read                  │ │
│  │  - DELETE /v1/conversations/:id → chat:delete         │ │
│  │  - POST /v1/fine-tuning → admin:fine-tune            │ │
│  │                                                        │ │
│  │  Check: user.scopes.includes(required_scope)          │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                     │
│                       ▼                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Resource-Level Authorization                           │ │
│  │                                                        │ │
│  │  Check ownership:                                      │ │
│  │  - Can user access conversation X?                    │ │
│  │    SELECT * FROM conversations                        │ │
│  │    WHERE id = X AND user_id = current_user_id         │ │
│  │                                                        │ │
│  │  Organization access:                                  │ │
│  │  - Can user access org resources?                     │ │
│  │    SELECT * FROM org_members                          │ │
│  │    WHERE org_id = Y AND user_id = current_user_id     │ │
│  │                                                        │ │
│  │  Row-Level Security (RLS):                            │ │
│  │  - PostgreSQL policies automatically enforce          │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════╗
║                      API KEY MANAGEMENT                       ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────┐
│  API Key Structure                                          │
│                                                             │
│  sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn012345     │
│  │   │    │                                                 │
│  │   │    └─ Random secret (256 bits)                      │
│  │   └────── Project ID                                    │
│  └────────── Prefix (identifies key type)                  │
│                                                             │
│  Storage:                                                   │
│  - Hash: SHA-256(secret)                                    │
│  - Store: {hash, user_id, scopes, created_at, last_used}   │
│  - Original key shown only once at creation                │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  API Key Permissions (Scopes)                               │
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Table: api_keys                                        │ │
│  │ ──────────────────────────────────────────────────────│ │
│  │ id              UUID PRIMARY KEY                       │ │
│  │ user_id         UUID NOT NULL                          │ │
│  │ key_hash        VARCHAR(64)  -- SHA-256 hash          │ │
│  │ prefix          VARCHAR(20)  -- "sk-proj-..."         │ │
│  │ name            TEXT         -- User-friendly name    │ │
│  │ scopes          TEXT[]       -- Permissions           │ │
│  │ rate_limit      INT          -- Requests per minute   │ │
│  │ created_at      TIMESTAMP                              │ │
│  │ last_used_at    TIMESTAMP                              │ │
│  │ expires_at      TIMESTAMP    -- Optional expiry       │ │
│  │ revoked         BOOLEAN DEFAULT FALSE                  │ │
│  │                                                        │ │
│  │ INDEX idx_key_hash (key_hash)                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  Example Scopes:                                            │
│  - chat:read, chat:write                                   │
│  - model:list, model:get                                   │
│  - fine-tune:create, fine-tune:list                        │
│  - admin:* (all permissions)                               │
└─────────────────────────────────────────────────────────────┘


╔═══════════════════════════════════════════════════════════════╗
║                   OAUTH 2.0 / SSO INTEGRATION                 ║
╚═══════════════════════════════════════════════════════════════╝

Third-party authentication options:
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│ Google OAuth   │  │ GitHub OAuth   │  │ SAML/OIDC SSO  │
│                │  │                │  │ (Enterprise)   │
└────────┬───────┘  └────────┬───────┘  └────────┬───────┘
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │ OAuth Provider Service   │
              │                          │
              │ 1. Redirect to provider  │
              │ 2. User authorizes       │
              │ 3. Receive auth code     │
              │ 4. Exchange for token    │
              │ 5. Fetch user profile    │
              │ 6. Create/link account   │
              │ 7. Issue our JWT         │
              └──────────────────────────┘
```

## Security Measures

### 1. Password Security
```python
# Password hashing (never store plaintext!)
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)  # Cost factor 12
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Password requirements:
# - Min 8 characters
# - At least 1 uppercase, 1 lowercase, 1 number
# - Optional: 1 special character
# - Check against common passwords list (HaveIBeenPwned API)
```

### 2. Token Security
```python
# JWT generation
import jwt
from datetime import datetime, timedelta

def generate_access_token(user_id, org_id, tier, scopes):
    payload = {
        'user_id': user_id,
        'org_id': org_id,
        'tier': tier,
        'scopes': scopes,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iss': 'chatgpt-api',
        'aud': 'chatgpt-clients',
    }
    return jwt.encode(payload, private_key, algorithm='RS256')

# Token validation
def validate_token(token):
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=['RS256'],
            audience='chatgpt-clients',
            issuer='chatgpt-api',
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise AuthError('Token expired')
    except jwt.InvalidTokenError:
        raise AuthError('Invalid token')
```

### 3. Rate Limiting by Auth Type
```python
rate_limits = {
    'free': {
        'requests_per_minute': 20,
        'tokens_per_day': 10_000,
    },
    'pro': {
        'requests_per_minute': 100,
        'tokens_per_day': 1_000_000,
    },
    'enterprise': {
        'requests_per_minute': 1000,
        'tokens_per_day': 'unlimited',
    },
}

# Distributed rate limiting (Redis)
def check_rate_limit(user_id, tier):
    key = f"rate_limit:{user_id}:{current_minute}"
    count = redis.incr(key)
    redis.expire(key, 60)  # TTL 1 minute

    limit = rate_limits[tier]['requests_per_minute']
    if count > limit:
        raise RateLimitError(f'Exceeded {limit} RPM')
```

### 4. Access Logging
```python
# Log every API request for audit
audit_log = {
    'timestamp': '2024-01-15T10:30:00Z',
    'user_id': 'usr_123',
    'org_id': 'org_789',
    'method': 'POST',
    'endpoint': '/v1/chat/completions',
    'ip': '203.0.113.45',
    'user_agent': 'Mozilla/5.0...',
    'status': 200,
    'latency_ms': 450,
    'tokens_used': 150,
}

# Store in:
# - Elasticsearch (searchable, 90 days)
# - S3 (long-term archive, 2 years)
```

## Organization-Level Access Control

### Multi-Tenant Hierarchy
```
Organization (org_789)
  ├── Owner (user_123) - Full admin
  ├── Admin (user_456) - Manage members, billing
  ├── Member (user_789) - Use API, view conversations
  └── Guest (user_012) - Read-only access
```

### Role-Based Permissions
```sql
CREATE TABLE org_members (
    org_id UUID REFERENCES organizations(id),
    user_id UUID REFERENCES users(id),
    role VARCHAR(20),  -- owner, admin, member, guest
    scopes TEXT[],
    joined_at TIMESTAMP,
    PRIMARY KEY (org_id, user_id)
);

-- Row-level security policy
CREATE POLICY org_access ON conversations
    USING (
        user_id = current_user_id()
        OR org_id IN (
            SELECT org_id FROM org_members
            WHERE user_id = current_user_id()
        )
    );
```

## Session Management

### Session Storage (Redis)
```python
session_data = {
    'session_id': 'sess_abc123',
    'user_id': 'usr_123',
    'org_id': 'org_789',
    'ip': '203.0.113.45',
    'user_agent': 'Mozilla/5.0...',
    'created_at': '2024-01-15T10:00:00Z',
    'last_activity': '2024-01-15T10:30:00Z',
    'expires_at': '2024-01-15T10:15:00Z',
}

# Store with TTL
redis.setex(f"session:{session_id}", ttl=900, value=json.dumps(session_data))
```

### Session Revocation
```python
# User logs out
def logout(session_id):
    redis.delete(f"session:{session_id}")

# Revoke all sessions for user
def logout_all(user_id):
    sessions = redis.keys(f"session:*")
    for session_key in sessions:
        session = json.loads(redis.get(session_key))
        if session['user_id'] == user_id:
            redis.delete(session_key)

# Admin: Revoke specific user's access
def revoke_user_access(user_id, reason):
    logout_all(user_id)
    db.execute("UPDATE users SET suspended = true WHERE id = %s", user_id)
    audit_log(f"User {user_id} access revoked: {reason}")
```

## Compliance & Security Best Practices

### 1. OWASP Top 10 Protection
- **SQL Injection**: Use parameterized queries
- **XSS**: Sanitize outputs, CSP headers
- **CSRF**: Use CSRF tokens for state-changing operations
- **Broken Auth**: Strong password policy, MFA, rate limiting
- **Sensitive Data Exposure**: Encrypt at rest/transit, redact logs

### 2. GDPR Compliance
- **Right to access**: Export user data API
- **Right to deletion**: Cascade delete conversations, embeddings
- **Data portability**: JSON export of all user data
- **Consent**: Opt-in for data processing, clear ToS

### 3. SOC 2 / ISO 27001
- **Access controls**: RBAC, least privilege
- **Audit logging**: All access logged and retained 2 years
- **Encryption**: AES-256 at rest, TLS 1.3 in transit
- **Incident response**: Runbooks for breaches, on-call rotation

## Interview Talking Points

**Q: How do you secure API keys?**
- Hash with SHA-256 before storage (never store plaintext)
- Show key only once at creation
- Support rotation (generate new, revoke old)
- Monitor usage (alert on suspicious patterns)

**Q: How do you handle compromised tokens?**
- Short-lived access tokens (15 min)
- Refresh token rotation (single-use)
- Session revocation (Redis blacklist)
- Alert on anomalous access (new IP/location)

**Q: How do you implement RBAC?**
- Scopes in JWT (checked at API gateway)
- Resource-level checks (owner, org member)
- Row-level security (PostgreSQL policies)
- Principle of least privilege

**Q: How do you prevent brute force attacks?**
- Rate limiting (5 attempts per 15 min)
- CAPTCHA after 3 failed attempts
- Account lockout after 10 failures
- Monitor for distributed attacks (IP reputation)
