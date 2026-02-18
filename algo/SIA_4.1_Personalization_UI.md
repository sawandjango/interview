# SIA 4.1 - Personalization UI - Personalized Content Window

## User Story

**As a** Sales Coach user,
**I want to** see a "Recommended for You" section in the For You tab that continuously updates content based on my onboarding choices and engagement activity,
**so that** my experience feels timely, relevant, and personalized.

---

## Acceptance Criteria – Frontend / Experience

* As a user, I should see a personalized "For You" section displaying up to 10 recommendations preloaded at a time in a card shuffle format within the For You tab.

* As I swipe through or complete recommendations, the cards should shuffle and refresh dynamically to reveal new content.

* When I tap the "Recommended for You" button, I should enter a continuous scrolling feed of the personalized content — similar to social media platforms — that loads new items seamlessly as I scroll.

* As a user, I should see different recommendations that adapt based on my recent activity in Interactive Practice, Instant Answers, and content consumption history.

* Each recommendation card should display a title, thumbnail, and a "Why" chip explaining why it was recommended (e.g., "Because you practiced iPad Pro" or "Based on your recent interest in Mac").

---

## Description

1. The "Recommended for You" section highlights content aligned to the user's interests, behaviors, and learning patterns, surfaced through personalization signals.

2. The initial card shuffle UI presents a compact, interactive preview of recommended items directly within the For You tab — encouraging quick engagement.

3. Selecting "Recommended for You" transitions the user into a dedicated feed experience that continuously refreshes as the user scrolls, mimicking modern content discovery flows (e.g., TikTok, Instagram Reels).

4. The feed updates dynamically based on:
   - Onboarding inputs (role, country, Apple product focus)
   - Engagement patterns (views, completions, skips, likes)
   - Practice and Q&A interactions in Interactive Practice and Instant Answers

5. The recommendation logic uses a hybrid approach — rule-based content prioritization combined with behavior-driven ranking.

6. The experience is designed to feel alive and adaptive, with no visible refreshes or breaks in the flow.

7. Personalized recommendations and where you are persist across sessions and devices (iOS and Web).

---

## Dependencies

### Backend Services
* **Personalization Service API** to deliver and rank recommendations per user session

### Frontend Engineering
* Card shuffle UI within the For You tab
* Continuous feed implementation with infinite scroll and caching
* Transition animation between card shuffle and feed view

### Data & Analytics
* **Event Tracking / Analytics Pipeline** to capture engagement signals (swipes, clicks, scrolls, completions)
* **Content Metadata** tagging (competencies, topics, Apple LOBs, difficulty, locale) to drive accurate recommendations

### Localization
* **Localization team** for translations of the "Why" chip and feed content titles

---

## API Specifications

### 1. Get Personalized Recommendations

**Endpoint:** `GET /api/v1/personalization/recommendations`

**Request Headers:**
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Query Parameters:**
```json
{
  "limit": 10,
  "offset": 0,
  "context": "for_you_tab"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "recommendations": [
      {
        "id": "rec_12345",
        "contentId": "content_67890",
        "type": "video",
        "title": "iPad Pro Sales Techniques",
        "description": "Learn advanced selling strategies for iPad Pro",
        "thumbnailUrl": "https://cdn.example.com/thumbnails/ipad-pro.jpg",
        "duration": 300,
        "recommendationReason": {
          "reasonCode": "based_on_practice",
          "displayText": "Because you practiced iPad Pro",
          "confidence": 0.85
        },
        "metadata": {
          "competencies": ["product_knowledge", "objection_handling"],
          "topics": ["iPad", "Premium_Devices"],
          "appleLOB": "iPad",
          "difficulty": "intermediate",
          "locale": "en_US"
        },
        "engagementScore": 0.92,
        "createdAt": "2025-12-15T10:30:00Z"
      }
    ],
    "pagination": {
      "total": 150,
      "limit": 10,
      "offset": 0,
      "hasMore": true
    },
    "personalizationContext": {
      "userId": "user_123",
      "sessionId": "session_abc",
      "lastUpdated": "2025-12-17T08:00:00Z"
    }
  }
}
```

**Error Response (400 Bad Request):**
```json
{
  "status": "error",
  "error": {
    "code": "INVALID_PARAMETERS",
    "message": "Limit must be between 1 and 50",
    "details": {}
  }
}
```

---

### 2. Track Engagement Events

**Endpoint:** `POST /api/v1/personalization/events`

**Request Headers:**
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Request Body:**
```json
{
  "events": [
    {
      "eventType": "card_swipe",
      "recommendationId": "rec_12345",
      "contentId": "content_67890",
      "timestamp": "2025-12-17T10:35:00Z",
      "context": {
        "position": 3,
        "sessionId": "session_abc",
        "deviceType": "iOS",
        "viewDuration": 45
      },
      "action": "swipe_left"
    }
  ]
}
```

**Field Definitions:**
- `eventType`: card_swipe | card_view | card_complete | feed_scroll | content_tap
- `action`: swipe_left | swipe_right | tap | complete | skip
- `deviceType`: iOS | Web

**Response (201 Created):**
```json
{
  "status": "success",
  "data": {
    "eventsProcessed": 1,
    "timestamp": "2025-12-17T10:35:01Z"
  }
}
```

---

### 3. Get User Personalization Profile

**Endpoint:** `GET /api/v1/personalization/profile`

**Request Headers:**
```json
{
  "Authorization": "Bearer {access_token}",
  "Content-Type": "application/json"
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "data": {
    "userId": "user_123",
    "onboardingData": {
      "role": "sales_specialist",
      "country": "US",
      "productFocus": ["iPad", "Mac", "iPhone"]
    },
    "engagementHistory": {
      "totalViews": 45,
      "totalCompletions": 32,
      "totalSkips": 8,
      "totalLikes": 15,
      "lastActiveDate": "2025-12-17T10:30:00Z"
    },
    "interests": [
      {
        "topic": "iPad Pro",
        "weight": 0.85,
        "source": "practice_activity"
      },
      {
        "topic": "Mac",
        "weight": 0.72,
        "source": "content_consumption"
      }
    ],
    "preferences": {
      "contentTypes": ["video", "practice"],
      "difficulty": "intermediate",
      "locale": "en_US"
    }
  }
}
```
