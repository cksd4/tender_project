# tender_project
# Catering Management System

## Project Name: tender_project
Tender (`tender_project`) is an accessible, responsive full-stack Django web application engineered to manage corporate catering operations. The system helps office employees pre-order weekly lunch options while enforcing strict operational cut-off constraints (10:00 AM) and cross-referencing dietary allergies automatically via custom database structures.

---

## 🎨 1. UX Design & Accessibility (Rubric 1.1, 1.5)

### Design Rationale
The front-end design is engineered mobile-first to accommodate employees on the go. Layout boundaries adapt using a fluid grid structure (CSS Grid & Flexbox) to prevent overlapping layout breaks across small Viewport displays.

Bootstrap utilities are integrated to manage responsive column breakpoints and maintain UI consistency across the application.

### Accessibility Safeguards (WCAG Compliance)
- **High Contrast Framework:** All text components maintain strict contrast levels against backgrounds.
- **Screen Reader Readiness:** Form inputs use explicit `<label>` declarations and structural visual fallbacks use `visually-hidden` descriptions.
- **Semantic HTML5:** Built entirely upon structured landmarks (`<nav>`, `<main>`, `<section>`, `<header>`).

---

## 🗄️ 2. Database Architecture (Rubric 1.2, 2.1, 7.1)

The application leverages Django's object-relational mapper (ORM) linked to an underlying SQLite environment. The structural entities communicate through specified relationships:

- **UserProfile (Custom User Model):** Manages user authentications, enterprise roles (`employee` vs `admin`), and custom allergen listings.
- **MealOption:** Represents individual dishes, managing descriptive texts, costs, and safe food tracking values.
- **Order:** Tracks transactional records linking user definitions directly to a chosen meal item using explicit relational constraints (`models.ForeignKey`).

---

## 📅 3. Agile Project Management Tracker (Rubric 1.3)

All project objectives were mapped, scheduled, and completed incrementally using GitHub Projects. Deliverables were categorized into prioritized Epics:
- **Epic 1: Auth Security:** Role differentiation views, dashboard permission access controls.
- **Epic 2: Core CRUD:** Administrative menu creation controls, employee registration capabilities.
- **Epic 3: Notification Guards:** Complex cut-off loops, allergen warning signals.

---

## 🧪 4. Testing Protocols & Verification (Rubric 4.1, 4.3)

### Automated Python Tests
The test module (`catering/tests.py`) targets core backend logic routines including verification of profile roles and allergy match rules.

To run automated assertions locally:
```bash
python manage.py test
```

### Manual Verification Ledger

| Test Case Identifier | Expected Outcome | Observed Behavior | Status |
| :--- | :--- | :--- | :--- |
| **TC-01:** Place Order Before 10 AM | Database appends record; success confirmation banner renders. | Order committed; dashboard displays validation confirmation. | **PASS** |
| **TC-02:** Place Order After 10 AM | Application intercepts execution; throws explicit deadline error. | System blocks submission; safely redirects with message banner. | **PASS** |
| **TC-03:** Horizontal Authorization Block | Basic user manually routing to `/admin-management/` triggers block. | View intercepts request; issues insufficient permissions error. | **PASS** |

### Debugging & Fix Log

| Issue | Resolution |
| :--- | :--- |
| Signing out did not return to the login page. | Changed sign-out to use a CSRF-protected POST form compatible with Django's logout view. |
| Automatic idle logout waited for activity or did not use the configured timeout. | Corrected the JavaScript static path, aligned the idle timer with Django's session timeout, and submitted the POST logout form automatically. |
| Admins could not find menu edit or remove controls. | Added a menu management list to the admin page; removal uses POST and is blocked for options linked to existing orders. |
| `runserver` failed importing `views` from `tender_project`. | Updated the project URL configuration to import views from the `catering` app. |
| The employee login page raised `NoReverseMatch` for the missing `login` URL name. | Updated login links and redirects to use the configured `employee_login` URL name. |

---

## 🧭 5. Wireframe Section

### Core User Flow Wireframe

```text
+--------------------------------------------------------------+
| Tender                                                       |
| [Login] [Register] [Admin]                                   |
+--------------------------------------------------------------+
|                                                              |
| Employee Dashboard                                            |
| ------------------------------------------------------------ |
| Welcome, [Name]                                              |
| [Meal Card] [Meal Card] [Meal Card]                          |
| [Order Summary]                                              |
|                                                              |
| Admin Panel                                                   |
| ------------------------------------------------------------ |
| Publish New Meal Option                                       |
| [Name] [Description] [Vendor] [Price] [Status]               |
|                                                              |
| Manage Menu Options                                           |
| [Meal Name] [Edit] [Remove]                                  |
| [Meal Name] [Edit] [Remove]                                  |
+--------------------------------------------------------------+
```

### Page Structure Overview

- **Login / Register Page**: user authentication and account creation
- **Employee Dashboard**: meal selection, order summary, allergy details
- **Admin Panel**: menu publishing and menu item management
- **Edit Meal Page**: update existing meal information
- **Order Confirmation**: success or validation warning states

---

## 🚀 6. Secure Deployment Checklist (Rubric 5.2, 6.2, 6.3)

1. Set up a secure configuration configuration layout by excluding credentials using `.gitignore`.
2. Isolate internal keys into an independent `.env` environment file.
3. Configure the destination Cloud Server Environment Variables:
   - `SECRET_KEY` = [Encrypted String Value]
   - `DEBUG` = `False`
4. Compile production assets using `python manage.py collectstatic`.

---

## 🤖 7. AI Tools Orchestration & Reflections (Rubric LO8)

### 8.1 Code Creation Support
- **Application Workflow:** GitHub Copilot assisted in structuring boilerplate fields inside `forms.py` and configuring the initial `AbstractUser` properties.
- **Outcome Evaluation:** This increased development velocity by eliminating repetitive field code, allowing more development time to focus on complex view calculations.

### 8.2 Debugging Optimization
- **Application Workflow:** Encountered an operational timezone mismatch during the 10:00 AM validation step. The AI tool diagnosed that `datetime.now()` needed to explicitly use `timezone.localtime(timezone.now()).time()` to reflect local office parameters accurately.
- **Outcome Evaluation:** Resolved routing calculations smoothly, avoiding data scheduling faults.

### 8.3 Performance & User Experience (UX) Adjustments
- **Application Workflow:** The AI tool suggested building an early exit routine (`break`) into the allergen verification loop inside `views.py`.
- **Outcome Evaluation:** This code enhancement prevents unnecessary loops once a positive match is flagged, maximizing server processing efficiency.

### 8.4 Automated Test Generation
- **Application Workflow:** GitHub Copilot was utilized to write basic test cases inside `tests.py`. It provided standard boilerplate assertions checking database entries.
- **Outcome Evaluation:** Minor structural adjustments were manually made to the generated model attributes to match our exact custom fields. This successfully provided clean test coverage for key operational endpoints.
