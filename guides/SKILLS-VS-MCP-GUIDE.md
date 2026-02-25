# המדריך המלא: מתי Skills ומתי MCP?
**עודכן:** 25 בפברואר 2026  
**למי:** צוותי DevOps, מפתחים, מנהלי פרויקטים

---

## 🎯 התשובה המהירה

| צריך | השתמש ב |
|------|---------|
| ללמד את ה-AI את הקונבנציות שלך | **Skill** |
| לתת ל-AI יכולת לגשת ל-API | **MCP Tool** |
| לשתף prompt עם הצוות (מתעדכן אוטומטית) | **MCP Prompt** |
| קיצור דרך ידני (slash command) | **Command** |

---

## 📚 הסבר מעמיק

### 1. Skills (מיומנויות)

**מה זה?**  
קובץ Markdown שמלמד את ה-AI איך לבצע משהו לפי הסטנדרטים שלך.

**איך זה עובד?**
- קובץ `SKILL.md` בתיקייה `skills/`
- ה-AI קורא אותו אוטומטית כשצריך
- כמו "ספר חוקים" שהבוט למד

**דוגמה:**
```markdown
# SKILL: Deploy to Production

כשמבקשים ממך לעשות deploy לפרודקשן:

1. וודא שכל הטסטים עברו (CI/CD ירוק)
2. בדוק שיש approval מ-tech lead
3. רץ: `npm run deploy:prod`
4. עקוב אחרי logs ל-5 דקות
5. שלח הודעה ל-#deployments בסלאק

חוקים:
- אף פעם לא deploy ביום שישי אחרי 14:00
- תמיד צור backup לפני deployment
- אם משהו נכשל, תעשה rollback מיד
```

**מתי להשתמש?**
✅ יש לך תהליך עבודה מוגדר  
✅ רוצה שהבוט יעקוב אחרי הקונבנציות של הצוות  
✅ הקבצים מקומיים (לא צריך server)  
✅ עדכונים נדירים (שבוע/חודש)

❌ צריך access לנתונים חיים (DB, API)  
❌ רוצה עדכונים אוטומטיים לכל הצוות  

---

### 2. MCP Tools (כלים)

**מה זה?**  
שרת שנותן ל-AI יכולות חדשות - גישה ל-APIs, DBs, מערכות חיצוניות.

**איך זה עובד?**
- שרת MCP רץ ברקע
- ה-AI קורא לשרת כש"מבין" שצריך
- השרת מבצע את הפעולה (query, API call, etc.)

**דוגמה:**
```json
// MCP Server: GitHub
{
  "tools": [
    "create_issue",
    "search_repos",
    "create_pr",
    "merge_pr"
  ]
}
```

כשאתה אומר: "תיצור issue על הבאג הזה בגיטהאב"  
→ הבוט **אוטומטית** קורא ל-MCP GitHub server → יוצר issue

**מתי להשתמש?**
✅ צריך נתונים חיים (מזג אוויר, מחירי מניות, DB queries)  
✅ רוצה שהבוט יחליט מתי להשתמש בכלי  
✅ אינטגרציה עם APIs (GitHub, Jira, Salesforce)  
✅ פעולות שדורשות authentication

❌ רק רוצה ללמד את הבוט תהליך עבודה  
❌ לא רוצה להריץ server  

---

### 3. MCP Prompts (תבניות prompt מרוכזות)

**מה זה?**  
Prompt templates ששרת MCP מחלק לכל הצוות.

**איך זה עובד?**
- Server מרכזי מחזיק prompts
- כל הצוות מתחבר לאותו server
- עדכנת prompt פעם אחת → מתעדכן לכולם אוטומטית

**דוגמה:**
```markdown
# MCP Prompt: PR Review Checklist

כש-reviewer מבקש ממך לבדוק PR:

1. Code quality:
   - יש tests?
   - יש type annotations?
   - עוקב אחרי ESLint rules?

2. Security:
   - אין secrets בקוד?
   - dependencies מעודכנים?
   - אין SQL injection risks?

3. Performance:
   - אין N+1 queries?
   - יש caching במקומות הנכונים?

תן feedback מסודר ב-3 קטגוריות:
✅ מה טוב
⚠️ מה צריך תיקון
💡 הצעות לשיפור
```

**מתי להשתמש?**
✅ צוות מרובה משתמשים (5+ אנשים)  
✅ רוצה לשמור על consistency בין כולם  
✅ עדכונים תכופים (יומי/שבועי)  
✅ Version control על prompts  
✅ רוצה analytics על שימוש

❌ עובד solo  
❌ prompts לא משתנים הרבה  

---

### 4. Commands (קיצורי דרך)

**מה זה?**  
קיצור דרך שאתה מפעיל ידנית עם slash.

**דוגמה:**
אתה כותב: `/deploy`  
→ הבוט מקבל את ההוראות מהקובץ

**מתי להשתמש?**
✅ משימות חוזרות שאתה רוצה לקצר  
✅ לא צריך שהבוט יחליט - אתה מחליט  
✅ פשוט מאוד, zero setup

❌ רוצה שהבוט יפעיל אוטומטית  

---

## 🎪 הבעיה שלך: PR גדול על repos מרובים

### התרחיש:
- יש לך **חוקים קבועים** ל-PRs (code review, security checks, etc.)
- צריך לבצע זאת על **הרבה repos**
- רוצה **לשתף עם הצוות**
- רוצה **עדכונים אוטומטיים** בלי להעתיק קבצים

### ✅ הפתרון: MCP Prompt Server

למה דווקא MCP Prompt?

1. **שיתוף עם צוות** ✅  
   כל הצוות מתחבר לאותו MCP server → כולם מקבלים את אותם החוקים

2. **עדכונים אוטומטיים** ✅  
   אתה מעדכן את ה-prompt בשרת → כולם מקבלים את העדכון מיידית (בלי להעתיק קבצים!)

3. **חוקים קבועים** ✅  
   ה-prompt מכיל את כל הרולים (security, tests, code quality)

4. **עובד על כל repo** ✅  
   אותו prompt חל על כל repos (GitHub MCP Tool מטפל ב-repo-specific logic)

---

## 🏗️ הארכיטקטורה המומלצת לבעיה שלך

### שכבה 1: MCP Prompt Server (החוקים)
```markdown
# PR Review Rules - Company Standard

## Mandatory Checks:
1. **Tests:** Coverage > 80%
2. **Security:** 
   - No hardcoded secrets
   - Dependencies updated (npm audit)
   - No SQL injection risks
3. **Code Quality:**
   - ESLint passes
   - Type annotations present
   - No console.log in production code
4. **Documentation:**
   - README updated if API changed
   - Comments for complex logic

## Review Response Format:
### ✅ Approved:
- List what's good
- Green light for merge

### ⚠️ Changes Requested:
- Critical issues (blocking)
- Nice-to-have improvements

### 💡 Suggestions:
- Performance tips
- Code optimization ideas
```

**איך מגדירים:**
```bash
# 1. הרץ MCP Prompt Server
npx @modelcontextprotocol/server-prompts \
  --config prompts-config.json

# 2. prompts-config.json
{
  "prompts": [
    {
      "name": "pr-review",
      "description": "Company-wide PR review checklist",
      "file": "./prompts/pr-review.md"
    }
  ]
}

# 3. כל הצוות מתחבר ל-server הזה
# בקובץ openclaw.json:
{
  "mcp": {
    "servers": {
      "company-prompts": {
        "url": "http://prompts.company.com:3000"
      }
    }
  }
}
```

---

### שכבה 2: MCP GitHub Tool (הפעולות)
```bash
# MCP GitHub Server נותן יכולות:
- create_pr
- list_repos
- search_code
- run_actions
- create_review_comment
```

---

### שכבה 3: Skill (התהליך הספציפי שלך)
```markdown
# SKILL: Multi-Repo PR Campaign

כשמבקשים ממך לבצע PR על repos מרובים:

1. קבל רשימת repos מהמשתמש
2. לכל repo:
   a. clone locally
   b. צור branch חדש: `feature/company-wide-update`
   c. בצע את השינויים
   d. הרץ tests
   e. commit + push
   f. צור PR עם MCP GitHub Tool
   g. הוסף את ה-reviewer המתאים (לפי CODEOWNERS)

3. עקוב אחרי כל ה-PRs:
   - שלח summary ל-#engineering בסלאק
   - יצור tracking issue עם רשימת כל ה-PRs

## חוקי עבודה:
- אם repo אחד נכשל → המשך לבא (אל תעצור את כל התהליך)
- תמיד שמור logs של מה עשית
- אם PR נדחה → תעדכן את המשתמש מיד
```

---

## 🎯 התהליך המלא - דוגמה

**אתה אומר לבוט:**
> "תבצע PR על כל ה-microservices שלנו - תוסיף GitHub Actions workflow לauto-deploy"

**מה קורה:**

1. **Skill נכנס לפעולה:**  
   הבוט יודע את התהליך (clone, branch, commit, PR)

2. **MCP GitHub Tool מבצע:**  
   יוצר את ה-PRs בפועל (דרך GitHub API)

3. **MCP Prompt מכתיב:**  
   בכל PR, הבוט מוסיף description עם ה-checklist הסטנדרטי של החברה

4. **כל הצוות רואה אותו checklist:**  
   כי כולם מחוברים לאותו MCP Prompt Server

5. **עדכנת את הרולים?**  
   שינוי אחד ב-prompt server → כל ה-PRs הבאים ישתמשו בחוקים החדשים

---

## 📊 טבלת השוואה - למקרה שלך

| קריטריון | Skill | MCP Prompt | Command |
|----------|-------|------------|---------|
| **שיתוף עם צוות** | ❌ צריך git pull | ✅ אוטומטי | ❌ צריך git pull |
| **עדכונים מיידיים** | ❌ manual sync | ✅ live updates | ❌ manual sync |
| **חוקים קבועים** | ✅ כן | ✅ כן | ✅ כן |
| **repos מרובים** | ✅ יכול | ✅ יכול | ✅ יכול |
| **Setup complexity** | 🟢 Easy | 🟡 Medium | 🟢 Easy |
| **Version control** | 🟡 Git | ✅ Built-in | 🟡 Git |
| **Analytics** | ❌ לא | ✅ כן | ❌ לא |

**המלצה עבורך:** **MCP Prompt + MCP GitHub Tool + Skill**

---

## 🚀 Setup מהיר - 3 שלבים

### שלב 1: הקם MCP Prompt Server
```bash
# 1. צור תיקייה לprompts
mkdir company-prompts
cd company-prompts

# 2. צור prompt
cat > pr-review.md << 'EOF'
# PR Review - Company Standard
[החוקים שלך כאן]
EOF

# 3. הרץ server
npx @modelcontextprotocol/server-prompts \
  --prompts pr-review.md \
  --port 3000
```

### שלב 2: חבר GitHub MCP Tool
```json
// openclaw.json
{
  "mcp": {
    "servers": {
      "github": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
        "env": {
          "GITHUB_TOKEN": "your-token-here"
        }
      }
    }
  }
}
```

### שלב 3: צור Skill לתהליך
```bash
# skills/multi-repo-pr/SKILL.md
[התהליך הספציפי שלך]
```

---

## 💡 טיפים מתקדמים

### טיפ 1: Versioning של Prompts
```bash
# prompts/pr-review-v2.md
# כשמעדכנים חוקים, שמור גרסה ישנה לbackward compatibility
```

### טיפ 2: Per-Team Prompts
```json
{
  "prompts": [
    {
      "name": "pr-review-frontend",
      "teams": ["frontend"]
    },
    {
      "name": "pr-review-backend",
      "teams": ["backend"]
    }
  ]
}
```

### טיפ 3: Monitoring
```bash
# Track איזה prompts נמשכים הכי הרבה
# MCP Prompt Server יכול לשלוח analytics
```

---

## ❓ שאלות נפוצות

### ש: מה אם אני רוצה prompts שונים לrepos שונים?
**ת:** השתמש במשתנים:
```markdown
# Prompt Template
כש-reviewer מבקש PR על {{REPO_NAME}}:
{% if REPO_TYPE == "frontend" %}
- בדוק accessibility
- בדוק responsive design
{% endif %}
{% if REPO_TYPE == "backend" %}
- בדוק API security
- בדוק database migrations
{% endif %}
```

### ש: איך אני מוודא שכולם עובדים עם הגרסה האחרונה?
**ת:** MCP Prompt Server עושה את זה אוטומטית - אין cache, כל שאילתה מושכת את הגרסה העדכנית.

### ש: מה אם ה-server נופל?
**ת:** הגדר fallback:
```json
{
  "mcp": {
    "servers": {
      "prompts-primary": "http://server1:3000",
      "prompts-backup": "http://server2:3000"
    },
    "fallback": "local-skill"
  }
}
```

---

## 📚 משאבים נוספים

- [MCP Protocol Docs](https://modelcontextprotocol.io)
- [OpenClaw Skills Guide](https://docs.openclaw.ai/tools/skills)
- [AgentSkills.io](https://agentskills.io)
- [Video: Commands vs MCP vs Skills](https://www.youtube.com/watch?v=xAIN7YHXfCY)

---

## 🎯 סיכום - מה לעשות מחר בבוקר

1. **הקם MCP Prompt Server** עם החוקים שלך (30 דק')
2. **חבר GitHub MCP Tool** לOpenClaw (10 דק')
3. **כתוב Skill** לתהליך multi-repo PR (20 דק')
4. **שתף את ה-server URL** עם הצוות (5 דק')

**סה"כ:** שעה אחת → פתרון מלא שעובד לכל הצוות ✅

---

**עודכן:** 25.02.2026 | **גרסה:** 1.0  
**יוצר:** Nivo 🌊 | **שאלות?** שאל בצ'אט
