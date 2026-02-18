# Question 1: JWT Token Security & Breach Response

[← Back to Case Study 1](./README.md)

---

## 🎯 Difficulty: 🟢 Core Concept

## 📝 Question

### Setup

It's 2 PM on Friday. Your security team just called - someone leaked your JWT secret key on GitHub. There are potentially **50,000 active user tokens** out there, and attackers are using them **right now**.

You have two scenarios to handle:

### Part A: You DON'T have Redis (stateless JWT only)

**Tell me step-by-step, what do you do in the next 30 minutes?**

### Part B: You DO have Redis available

**How does having Redis change your response strategy?**

---

## 🎓 What I'm Looking For

- Understanding that rotating the secret invalidates ALL tokens (including legitimate users)
- Knowledge of deployment strategies without downtime
- Communication plan for users
- Trade-offs between security and user experience
- Performance implications of different approaches
- Redis patterns for token management

---

## ✅ Good Answer Should Include

### Part A: Without Redis

```
Step 1: Generate new JWT secret immediately
    - Create new secret: openssl rand -base64 32
    - Store securely in environment/secrets manager

Step 2: Deploy with blue-green strategy
    - Phase 1: Servers accept BOTH old and new secrets (5-min grace period)
    - Phase 2: Gradually shift traffic to new secret
    - Phase 3: Completely cutover to new secret

Step 3: Force re-authentication
    - All users must re-login
    - Clear any cached tokens on client side
    - Send notification: "Security update - please log in again"

Why this is painful:
✗ Everyone gets logged out (bad UX)
✗ Mobile apps might break (if they don't handle gracefully)
✗ Deployment coordination across servers
✗ Customer support will get flooded
```

**Code Example:**
```python
class JWTValidator:
    def __init__(self):
        self.current_secret = os.getenv('JWT_SECRET_V2')
        self.old_secret = os.getenv('JWT_SECRET_V1')
        self.cutover_time = datetime(2024, 11, 2, 14, 30, 0)  # 30 min from now

    def validate(self, token):
        try:
            # Try new secret first
            return jwt.decode(token, self.current_secret, algorithms=['HS256'])
        except jwt.InvalidSignatureError:
            # Allow old secret for 5-minute grace period only
            if datetime.now() < self.cutover_time + timedelta(minutes=5):
                try:
                    return jwt.decode(token, self.old_secret, algorithms=['HS256'])
                except:
                    raise InvalidToken("Token invalid")
            raise InvalidToken("Token expired - please re-login")
```

### Part B: With Redis

**Much better options available:**

```
Option 1: Token Denylist (Recommended)
───────────────────────────────────────
Strategy:
- Keep list of revoked token IDs in Redis
- Check every incoming token against denylist
- Only revoke compromised tokens (surgical approach)

Implementation:
redis.setex(
    f"revoked:{token_jti}",  # jti = JWT ID claim
    remaining_ttl,           # seconds until token would expire anyway
    "1"
)

def validate_token(token):
    claims = jwt.decode(token, secret)
    jti = claims.get('jti')

    # Check if revoked
    if redis.exists(f"revoked:{jti}"):
        raise TokenRevoked("This token has been revoked")

    return claims

Pros:
✓ Surgical revocation (only compromised tokens)
✓ Legitimate users stay logged in
✓ Fast (Redis lookup ~1-2ms)

Cons:
✗ Redis becomes critical path (every request)
✗ Need to track token JTIs (add to JWT claims)
✗ Denylist cleanup needed (TTL = token expiry)
```

**Code Example:**
```python
from functools import wraps
import redis

redis_client = redis.Redis(host='localhost', decode_responses=True)

def require_valid_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')

        try:
            claims = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            jti = claims['jti']

            # Check denylist
            if redis_client.exists(f"revoked:{jti}"):
                return {"error": "Token revoked"}, 401

            # Token is valid
            request.user_id = claims['user_id']
            return f(*args, **kwargs)

        except jwt.ExpiredSignatureError:
            return {"error": "Token expired"}, 401
        except jwt.InvalidTokenError:
            return {"error": "Invalid token"}, 401

    return decorated

@app.route('/api/conversations')
@require_valid_token
def get_conversations():
    # This endpoint is protected
    return {"conversations": [...]}
```

```
Option 2: Store Active Sessions
────────────────────────────────
Strategy:
- Store all valid tokens in Redis (allowlist)
- If token not in Redis → invalid

Implementation:
# On login:
redis.setex(
    f"session:{user_id}:{device_id}",
    token_ttl,
    json.dumps({
        "jti": token_jti,
        "created_at": timestamp,
        "ip": user_ip,
        "user_agent": user_agent
    })
)

# On validation:
def validate_token(token):
    claims = jwt.decode(token, secret)
    session_key = f"session:{claims['user_id']}:{claims['device_id']}"

    if not redis.exists(session_key):
        raise InvalidSession()

    return claims

Pros:
✓ Full control over sessions
✓ Can revoke by user, device, or specific token
✓ Can see all active sessions

Cons:
✗ More Redis memory usage (all tokens stored)
✗ Redis becomes SPOF (single point of failure)
✗ Cleanup complexity
```

---

## 🔴 Common Mistakes to Avoid

1. **❌ Only rotating secret without grace period**
   ```
   Result: All requests fail immediately during deployment
   Better: Dual-secret validation for 5 minutes
   ```

2. **❌ Not tracking token JTIs from the start**
   ```
   Problem: Can't selectively revoke tokens
   Better: Always include 'jti' claim in JWT payload
   ```

3. **❌ No fallback when Redis is down**
   ```python
   # Bad:
   if redis.exists(f"revoked:{jti}"):  # Crashes if Redis down
       raise TokenRevoked()

   # Good:
   try:
       if redis.exists(f"revoked:{jti}"):
           raise TokenRevoked()
   except redis.ConnectionError:
       # Fail closed (secure) or fail open (available)?
       # Decision depends on risk tolerance
       logger.error("Redis down - failing closed for security")
       raise ServiceUnavailable("Authentication service temporarily down")
   ```

4. **❌ Infinite denylist growth**
   ```
   Problem: Denylist keeps growing forever
   Better: TTL = token expiry time (auto cleanup)
   ```

---

## 🤔 Follow-Up Questions

### Q1: "What if you can't log everyone out because it's Black Friday and that would cost millions in lost sales?"

**Good Answer:**
```
Tough trade-off: Security vs Revenue

Immediate actions:
1. Rate limit heavily from suspicious IPs
2. Enable fraud detection alerts
3. Monitor for unusual patterns
4. Revoke known compromised tokens via denylist

Gradual mitigation:
1. Shorten token TTL to 15 minutes (from 24 hours)
2. Force re-auth for high-risk actions (checkout, profile changes)
3. Implement device fingerprinting
4. Gradual secret rotation over 24 hours

Post-incident:
1. Rotate secret after Black Friday
2. Implement refresh token strategy
3. Add monitoring for token abuse
```

### Q2: "Redis just crashed. Do you fail open or fail closed?"

**Good Answer:**
```
Depends on context:

Fail Closed (Secure):
- Financial transactions
- Admin panels
- PII access
Risk: Service outage

Fail Open (Available):
- Public content
- Read-only operations
- Low-risk features
Risk: Security breach

My recommendation: HYBRID
- Check Redis with timeout (100ms)
- If timeout or down:
  * Fail closed for /admin/* endpoints
  * Fail open for /public/* endpoints
  * Log all requests for later audit

Code:
def check_revoked(jti):
    try:
        return redis.exists(f"revoked:{jti}", timeout=0.1)
    except redis.TimeoutError:
        if request.path.startswith('/admin'):
            raise ServiceUnavailable()  # Fail closed
        else:
            logger.warning(f"Redis timeout - allowing request to {request.path}")
            return False  # Fail open
```

### Q3: "How do you notify affected users?"

**Good Answer:**
```
Multi-channel notification:

1. In-app banner (immediate)
   - "Security update in progress. Please re-login if you experience issues."

2. Email (within 1 hour)
   - Subject: "Important: Security Update Completed"
   - Body: Explain what happened (without details), what we did, what they should do

3. Status page
   - Update status.company.com
   - Timeline of incident and resolution

4. API response header (for developers)
   - X-Auth-Status: "rotated-2024-11-02"
   - Helps debug integration issues

Don't mention:
✗ "Our secret was leaked"
✗ Technical details of vulnerability
✗ Panic-inducing language

Do mention:
✓ "Proactive security measure"
✓ "No evidence of data breach"
✓ "Your account is secure"
```

---

## 📊 Trade-Off Analysis

| Approach | Security | UX | Complexity | Cost |
|----------|----------|-----|------------|------|
| Rotate secret | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ | Free |
| Redis denylist | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Redis cost |
| Redis allowlist | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | High Redis cost |
| Hybrid (short-lived JWT + refresh token) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Medium |

---

## 💡 Key Takeaways

1. **Prevention > Cure**
   - Use short-lived access tokens (15 min)
   - Implement refresh tokens stored in Redis
   - Never commit secrets to code

2. **Always include `jti` claim**
   - Enables selective token revocation
   - Essential for denylist pattern

3. **Plan for Redis failure**
   - Circuit breaker pattern
   - Decide fail-open vs fail-closed per endpoint
   - Monitor Redis health

4. **Blue-green deployments**
   - Never hard-cutover
   - Always have grace period
   - Test rollback procedure

5. **Communication matters**
   - Clear user notifications
   - Update status page
   - Coordinate with customer support

---

## 🔗 Related Questions

- [Question 2: Rate Limiting Across Multiple Servers](./02_rate_limiting.md)
- [Question 10: Circuit Breaker Implementation](./10_circuit_breaker.md)

---

[← Back to Case Study 1](./README.md) | [Next Question →](./02_rate_limiting.md)
