# Bookkeeping Automation - Project Plan

**Created:** 2026-02-23  
**Status:** Planning → Build → Launch  
**Target Launch:** TBD

---

## Problem Statement

Small service businesses (marketing agencies, creative studios, consultants, freelancers) waste 5-15 hours/week on bookkeeping busywork:
- Collecting invoices from emails/vendors
- OCR/manual data entry
- Matching receipts to bank statements
- Organizing files for accountant
- Chasing missing documents

**They pay accountants $500-2000/month but still do most of the grunt work themselves.**

---

## Solution

**Automated Bookkeeping Pipeline** - SaaS platform that:
1. **Collects** invoices automatically (email forwarding, OCR, direct upload)
2. **Validates** and matches to bank transactions
3. **Organizes** into proper folders/categories
4. **Delivers** clean, structured data to their accountant

---

## Target Market (NARROWED)

### Primary (ONLY THIS FOR MVP):
**Israeli Marketing & Creative Agencies**
- Size: 2-20 employees
- Invoices: 50-200/month
- Geography: Israel only (Hebrew + Israeli bank support critical)
- Type: Ad agencies, social media agencies, creative studios
- Currently using: Excel + Google Drive + chaos

**Why this niche:**
- Defined market (thousands of agencies, easy to find)
- Built-in case study (Assaf's wife)
- Network access (her contacts = first 10 customers)
- Same pain points across all agencies
- Willingness to pay (marketing = money)

### Future expansion (after 50 customers):
- Consultants
- Law offices  
- Architecture studios
- Other service businesses

**For now: ONLY marketing/creative agencies in Israel. Master this first.**

---

## Competitive Landscape

**Existing players:**
- Expensify, Receipt Bank, Dext, QuickBooks - all focused on big companies or too complex
- Israeli: HoganCloud, Hashavim - enterprise-focused, clunky UX

**Our edge:**
- **Micro-niche:** Service businesses only (not retail, not e-commerce)
- **Israeli market first:** Hebrew, Israeli banks, Israeli accountant workflows
- **Simple:** One job, done well - not a full accounting suite

---

## Revenue Model

**Subscription tiers:**

| Tier | Price/Month | Invoices | Features |
|------|-------------|----------|----------|
| Solo | ₿49 ($15) | 50 | Basic OCR, email forwarding |
| Studio | ₿149 ($45) | 200 | Multi-user, bank sync, categories |
| Agency | ₿299 ($90) | 500+ | API, accountant portal, priority support |

**Add-ons:**
- Accountant coordination: +₿99/month
- VAT report generation: +₿49/month

---

## Tech Stack (Proposed)

**Backend:**
- Python/FastAPI (simple, fast, good for automation)
- PostgreSQL (structured data)
- Redis (job queue for processing)
- S3/Backblaze (document storage)

**OCR/Processing:**
- Tesseract or Google Vision API
- Israeli receipt parsing (Hebrew support critical)

**Integrations:**
- Email (Gmail/Outlook forwarding)
- Bank APIs (Israeli banks - limited, may need manual sync)
- Accountant export formats (Excel, CSV, Israeli standards)

**Frontend:**
- Next.js or simple Vue.js dashboard
- Mobile-friendly (people upload from phone)

---

## Development Phases

### Phase 1: MVP (2-4 weeks)
- [ ] Email forwarding → OCR → structured data
- [ ] Manual upload interface
- [ ] Basic dashboard (view, approve, download)
- [ ] Single user
- [ ] Export to Excel for accountant
- **Goal:** Get it working for Assaf's wife's business

### Phase 2: Beta (4-6 weeks)
- [ ] Bank transaction matching
- [ ] Multi-user support
- [ ] Categories/tags
- [ ] Israeli accountant format export
- [ ] 5-10 beta customers

### Phase 3: Launch (6-8 weeks)
- [ ] Payment integration (Israeli credit cards)
- [ ] Accountant portal (view-only access)
- [ ] Mobile app or PWA
- [ ] Marketing site + onboarding
- [ ] Public launch

---

## Marketing/Customer Acquisition (FOCUSED)

### Phase 1: Direct Network (First 10 customers)
- **Assaf's wife's contacts** (other agency owners she knows personally)
- Facebook groups: "סוכנויות פרסום בישראל", "Social Media Managers Israel"
- LinkedIn: Search "סוכנות פרסום" + Israel, DM owners directly
- **Message:** "בנינו משהו לאשתי, זה חסך לה 10 שעות בשבוע. רוצה לראות?"

### Phase 2: Community Presence (10-50 customers)
- Join every Israeli marketing/agency Facebook group
- Answer questions about bookkeeping pain
- Case study: "איך [Agency Name] חסכה 40 שעות בחודש"
- Hebrew blog: "המדריך המלא לניהול חשבוניות לסוכנות פרסום"
- Before/after demo video (Assaf's wife on camera)

### Phase 3: Partnerships (50+ customers)
- **Accountants who serve agencies** → they recommend us, get 20% commission
- Marketing agency networks/associations
- Integrate with Israeli accounting software (Hashavim, HoganCloud)
- Sponsor marketing conferences/meetups

### Positioning Statement:
**"המערכת היחידה שנבנתה במיוחד לסוכנויות פרסום בישראל"**
("The only system built specifically for Israeli marketing agencies")

---

## Success Metrics

**Month 1:** 1 paying customer (Assaf's wife)  
**Month 3:** 10 paying customers ($500 MRR)  
**Month 6:** 50 customers ($2500 MRR)  
**Month 12:** 200 customers ($10k MRR)

---

## Niche Validation (BEFORE building anything big)

### Week 1: Prove demand exists
- [ ] Interview Assaf's wife in detail (45 min recorded session)
- [ ] Find 5 other agency owners, ask: "Would you pay ₪150/month for this?"
- [ ] Join 3 Israeli agency Facebook groups, post question about bookkeeping pain
- [ ] LinkedIn search: Find 50 target agencies, save contact info
- [ ] **Success criteria:** 3+ people say "yes, I'd buy this"

### Week 2: Landing page test
- [ ] Build simple landing page (Hebrew)
- [ ] Headline: "תפסיקו לבזבז זמן על חשבוניות - אנחנו נעשה את זה בשבילכם"
- [ ] Show the problem, promise the solution
- [ ] "הצטרפו לרשימת ההמתנה" email form
- [ ] Post in groups, DM people → drive traffic
- [ ] **Success criteria:** 20+ email signups in one week

### Week 3-4: Pre-sell
- [ ] Email the waitlist: "We're launching in 2 weeks. First 10 customers get 50% off forever."
- [ ] Price: ₪99/month (normally ₪199)
- [ ] Manual demo calls with interested people
- [ ] **Success criteria:** 3+ people pay deposit before product exists

**If validation fails at any stage → pivot the niche or approach.**

---

## Next Steps (AFTER validation passes)

1. **Document current workflow** (Assaf's wife's process today)
2. **Build flow diagrams** for each automation step
3. **Build MVP** (email → OCR → dashboard → export)
4. **Deliver to first 3 paying customers manually** (before automation)
5. **Iterate based on feedback**

---

## Daily Tasks for Nivo

- **Research competitors** (features, pricing, reviews)
- **Find potential customers** (LinkedIn, Facebook groups)
- **Document use cases** (different business types, workflows)
- **Track industry trends** (what accountants need, what businesses hate)
- **Build prototypes** (scripts, automation flows)

---

_This is a real project. Build it properly. One step at a time._
