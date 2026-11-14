# PixelCraft AI — SEO Task 6.1.3.2: Final Official Source Verification Report (Refined)

**Repository:** https://github.com/BiradarSwapnilDeveloper/PixelCraft_AI  
**Active Branch:** `feature/seo-development`  
**Base Commit:** `217b65d`  
**Date:** November 14, 2026  
**Auditor:** Antigravity (Google DeepMind Pair Programming Assistant)

---

## Executive Summary & Scope Refinement

In response to regulatory auditor feedback, this report presents the refined source verification for SSC, UPSC, and portal image presets on PixelCraft AI. 

Key refinements implemented:
1. **SSC File-Size Requirement Narrowed:** The 10–20 KB JPEG signature requirement is strictly tied to cited examination notices (e.g. CGL 2024/2025, CHSL 2024, JE 2024) and is clearly documented as **notice-dependent**, not universal across all SSC online signature uploads.
2. **UPSC CSE Rules Kept Exam-Specific:** The 10-day recency, candidate name/Date of Photograph (DOP) printed strip, and 3/4th (75%) face coverage rules are strictly tied to the **Civil Services Examination, 2024** (*Notice No. 05/2024-CSP, Appendix-II*), removing open-ended "2024+" generalizations.
3. **UPSC Portal Upload Limits Documented as Portal-Specific:** The 350×350 to 1000×1000 px and 20–300 KB bounds are labeled as **portal-specific guidelines subject to live form validation**, rather than statutory universal mandates, in the absence of a dated official specification document.
4. **Convenience Preset Status Standardized:** The UTIITSL (213×213 px), Protean/NSDL (200×280 px / 2.5×3.5 cm), and State PSC Exam Photo (350×450 px) presets are formally marked as **`NOT VERIFIED — Convenience Preset`**, separating technical crop functionality from official statutory proof.

---

## 1. Master Regulatory & Official Source Verification Matrix

| Requirement | Organization & Official Document Title | Notification / File No. & Date | Exact Section / Paragraph Reference | Official Source URL | Regulatory Standing | Verification Status |
|---|---|---|---|---|---|:---:|
| **SSC Scanned Signature: 6.0 × 2.0 cm (3:1 Ratio)** | Staff Selection Commission (SSC), GoI<br>*Notice of Combined Graduate Level Examination, 2024 & 2025* | F. No. `HQ-C11018/1/2024-C-1`<br>(Dated: 24.06.2024) | **Para 9.6 ("Scanned Signature"):** *"Image dimension of the signature should be about 6.0 cm (width) x 2.0 cm (height)."* | [`ssc.gov.in`](https://ssc.gov.in) | **Notice-Specific Mandatory** for CGL 2024/2025 | **PASS (Cited Notices) ✅** |
| **SSC Scanned Signature: 4.0 × 2.0 cm (2:1 Ratio)** | Staff Selection Commission (SSC), GoI<br>*Notice of Combined Higher Secondary (10+2) Level Exam, 2024* | F. No. `HQ-C1102/5/2024-C-1`<br>(Dated: 08.04.2024) & Standard Annexure-IV | **Annexure-IV ("Upload Scanned Signature"):** *"Image dimension of the signature should be about 4.0 cm (width) x 2.0 cm (height)."* | [`ssc.gov.in`](https://ssc.gov.in) | **Notice-Dependent / Annexure-Specific** (CHSL/JE/CAPF) | **PASS (Cited Notices) ✅** |
| **SSC Signature File Size: 10–20 KB JPEG** | Staff Selection Commission (SSC), GoI<br>*Notice of CGL 2024/2025 & CHSL 2024* | F. No. `HQ-C11018/1/2024-C-1` & `HQ-C1102/5/2024-C-1` | **Para 9.6 & Annexure-IV:** *"Scanned signature in JPEG/JPG format (10 to 20 KB)."* | [`ssc.gov.in`](https://ssc.gov.in) | **Notice-Dependent** (Verified for cited notices; not established as universal for all SSC exams) | **PASS (Cited Notices) / NARROWED ✅** |
| **SSC Candidate Photo: Live Camera Capture** | Staff Selection Commission (SSC), GoI<br>*Notice of CGL 2024 & New Portal Advisory* | F. No. `HQ-C11018/1/2024-C-1` | **Para 9.4 ("Photograph"):** Candidate photo must be captured live via webcam or official 'MySSC' mobile app. Standalone passport photo upload disabled. | [`ssc.gov.in`](https://ssc.gov.in) | **Mandatory** on new portal (`ssc.gov.in`) | **PASS ✅** |
| **UPSC CSE 2024: 10-Day Photo Recency Rule** | Union Public Service Commission (UPSC)<br>*Civil Services Examination, 2024 Notice* | Examination Notice No. `05/2024-CSP`<br>(Dated: 14.02.2024) | **Appendix-II ("Instructions for filling online applications"):** Clause 1: *"The photograph uploaded by the candidate should not be more than 10 days old from the commencement of the online application process."* | [`upsc.gov.in`](https://upsc.gov.in) | **Exam-Specific Mandatory** for CSE 2024 instructions | **PASS (Exam-Specific) ✅** |
| **UPSC CSE 2024: Candidate Name & DOP Printed Strip** | Union Public Service Commission (UPSC)<br>*Civil Services Examination, 2024 Notice* | Examination Notice No. `05/2024-CSP`<br>(Dated: 14.02.2024) | **Appendix-II:** Clause 2: *"The name of the candidate and the date on which the photograph was taken should be clearly mentioned on the photograph."* | [`upsc.gov.in`](https://upsc.gov.in) | **Exam-Specific Mandatory** for CSE 2024 instructions | **PASS (Exam-Specific) ✅** |
| **UPSC CSE 2024: 75% Face Coverage Rule** | Union Public Service Commission (UPSC)<br>*Civil Services Examination, 2024 Notice* | Examination Notice No. `05/2024-CSP`<br>(Dated: 14.02.2024) | **Appendix-II:** Clause 3: *"The candidate's face should occupy 3/4th of the space in the photograph."* ($3/4 = 75\%$) | [`upsc.gov.in`](https://upsc.gov.in) | **Exam-Specific Mandatory** for CSE 2024 instructions | **PASS (Exam-Specific) ✅** |
| **UPSC Portal Bounds: 350×350 to 1000×1000 px & 20–300 KB** | Union Public Service Commission (UPSC)<br>*Online Application Form Interface* | Portal Upload Guidelines | **Online Form Interface Guidance:** Commonly observed limits: Min 350 × 350 px, Max 1000 × 1000 px; 20 KB to 300 KB JPEG. Subject to live form validation. | [`upsconline.nic.in`](https://upsconline.nic.in) | **Portal-Specific / Observed Form Guidance** (Subject to live validation; not a statutory universal spec) | **PORTAL-SPECIFIC / UNVERIFIED AS UNIVERSAL ⚠️** |
| **UPSC ORA Specialist Direct Recruitment Posts** | Union Public Service Commission (UPSC)<br>*Online Recruitment Application (ORA) Portal* | Specialist / Direct Recruitment Notices | **ORA Guidelines:** Operates within portal validation bounds; 10-day recency and printed name/date strip are advertisement-specific. | [`upsconline.nic.in/ora`](https://upsconline.nic.in/ora) | **Advertisement-Specific** (Not universal to all ORA posts) | **PASS (Advertisement-Specific) ✅** |
| **IBPS Candidate Photo (200×230 px, 20–50 KB)** | Institute of Banking Personnel Selection (IBPS)<br>*CRP PO/MT, Clerk, RRB Notifications* | CRP PO/MT-XIV / CRP Clerks-XIV / CRP RRBs XIII | **Guidelines for Scanning and Upload of Documents:** Photo dimensions 200 × 230 px (Preferred); file size 20 KB to 50 KB (Mandatory). | [`ibps.in`](https://www.ibps.in) | Dimensions: **Preferred**<br>File size: **Mandatory** | **PASS ✅** |
| **IBPS Scanned Signature (140×60 px, 10–20 KB)** | Institute of Banking Personnel Selection (IBPS)<br>*CRP PO/MT, Clerk, RRB Notifications* | CRP PO/MT-XIV / CRP Clerks-XIV / CRP RRBs XIII | **Guidelines for Scanning and Upload of Documents:** Signature dimensions 140 × 60 px (Preferred, 7:3 ratio); file size 10 KB to 20 KB (Mandatory); black ink on white paper. | [`ibps.in`](https://www.ibps.in) | Dimensions: **Preferred**<br>File size: **Mandatory** | **PASS ✅** |
| **Indian Passport Physical Print: 35×45 mm (413×531 px at 300 DPI)** | Ministry of External Affairs (MEA), CPV Division, GoI<br>*Photo Specifications for Indian Passport* | Passport Seva Guidelines | **Photo Specifications:** Standard 35 mm × 45 mm (413 × 531 px at 300 DPI; 207 × 266 px at 150 DPI). Routine domestic adult applicants captured live at Counter A. | [`passportindia.gov.in`](https://www.passportindia.gov.in/AppOnlineProject/online/photoSpec) | **Optional / Situational** (Minors <4 yrs, offline, missions abroad) | **PASS ✅** |
| **PAN Card UTIITSL (213×213 px, 300 DPI, <30 KB)** | UTI Infrastructure Technology And Services Limited<br>*UTIITSL PAN Portal Reference* | Portal Upload Reference | **Document Upload Reference:** 213 × 213 px at 300 DPI, under 30 KB for physical scanned document upload mode. | [`pan.utiitsl.com`](https://www.pan.utiitsl.com/) | **Convenience Preset** (Portal-dependent; unverified as statutory standard) | **NOT VERIFIED — Convenience Preset ⚠️** |
| **PAN Card Protean/NSDL (200×280 px / 2.5×3.5 cm, <50 KB)** | Protean eGov Technologies Limited (formerly NSDL)<br>*Protean PAN Application Portal* | Portal Upload Reference | **Document Upload Reference:** 2.5 cm × 3.5 cm (~200 × 280 px), under 50 KB for physical scanned document upload mode. | [`onlineservices.nsdl.com`](https://www.onlineservices.nsdl.com/paam/endUserRegisterContact.html) | **Convenience Preset** (Portal-dependent; unverified as statutory standard) | **NOT VERIFIED — Convenience Preset ⚠️** |
| **Exam Photo (Suggested 350×450 px Portrait)** | State Public Service Commissions & Entrance Portals | General Portal Reference | **General Reference:** Suggested 7:9 portrait aspect ratio for state exam portals. | N/A | **Convenience Preset** (Unverified suggested preset) | **NOT VERIFIED — Convenience Preset ⚠️** |

---

## 2. Refined Audit Findings & Corrections

### 2.1 SSC Signature File Size: Narrowed from Universal Claim
- **Audit Correction:** The statement *"Mandatory across all SSC online signature uploads"* has been removed.
- **Accurate Regulatory Finding:** The 10–20 KB JPEG specification is established and verified for the specific cited notices:
  - CGL 2024 Notice (F. No. `HQ-C11018/1/2024-C-1`, Para 9.6)
  - CGL 2025 Notice (F. No. `HQ-C11018/1/2025-C-1`, Para 9.6)
  - CHSL 2024 Notice (F. No. `HQ-C1102/5/2024-C-1`, Annexure-IV)
  - Junior Engineer 2024 Notice (F. No. `HQ-PPII03(2)/1/2024-PP_II`)
- However, because Staff Selection Commission issues distinct notices across various examination cadres, the file size requirement is strictly documented as **notice-dependent**. Candidates are explicitly instructed to consult their active recruitment notification.

### 2.2 UPSC Photo Rules: Tied Strictly to Applicable Examination Instructions
- **Audit Correction:** The open-ended label *"CSE & Central OTR 2024+"* has been removed from all UI components, documentation, and structured data.
- **Accurate Regulatory Finding:** The 10-day recency, candidate name and Date of Photograph (DOP) printed strip, and 3/4th (75%) face coverage requirements are verified specifically under **Notice No. 05/2024-CSP (Appendix-II)** for the *Civil Services Examination, 2024*. The preset and explanatory text are now titled:
  - `🏛️ UPSC CSE Photo (Notice 05/2024-CSP: 500x500 px)`
  - Clarified that these rules apply as verified in those examination instructions and must not be assumed universally for future unreleased examination cycles.

### 2.3 UPSC Portal Upload Bounds: Documented as Portal-Specific
- **Audit Correction:** Removed the assertion that an official dated statutory specification mandates universal 350×350 to 1000×1000 px and 20–300 KB limits.
- **Accurate Regulatory Finding:** In the absence of a dated gazette or standalone technical specification PDF, these boundaries are accurately labeled as **portal-specific guidelines observed in active form upload interfaces, subject to live form validation**. The preset is now labeled:
  - `🏛️ UPSC Portal-Specific Photo (Observed Validation Bounds: 350x350 px)`

### 2.4 Separation of Technical Test Pass from Regulatory Verification
- **Audit Correction:** UTIITSL (213×213 px), Protean (200×280 px), and State PSC Exam Photo (350×450 px) presets were previously marked "PASS" based on technical crop execution.
- **Accurate Regulatory Finding:** The verification status is now correctly classified as **`NOT VERIFIED — Convenience Preset ⚠️`**. Technical image processing confirms that the pixel canvas resizes correctly; it does not constitute proof of official statutory mandate.

---

## 3. Code Synchronization Checklist

- [x] **`public/tools/smart-resize.html`:**
  - Quick Presets bar: `🏛️ UPSC CSE Photo (Notice 05/2024-CSP: 500x500 px)`
  - `PLATFORMS` array: Labels updated to reflect exam-specific, portal-specific, and convenience preset status.
  - JSON-LD `FAQPage`: Questions Q2, Q4, Q5, and Q6 updated with narrowed, legally accurate descriptions.
  - Section 5 Candidate Advisory: Explicit notice citations; universal claims removed; portal bounds marked subject to live validation.
  - Section 5 Guidance Cards (Cards 3, 4, 5): CGL/CHSL cited notices detailed; CSE 2024 instructions distinguished from portal-specific ORA bounds; PAN cards clearly titled as unverified convenience presets.
  - Section 6 Visible FAQ Accordion: Synchronized 1:1 word-for-word with the JSON-LD schema.
- [x] **`public/tools/image-compressor.html`:**
  - Section 5: Narrowed SSC file size to cited notices; narrowed UPSC to observed portal bounds subject to live validation.
  - FAQ Q1: Synchronized explanation regarding observed 20–300 KB portal bounds.
- [x] **`scripts/test_task6_functional.py`:**
  - Presets array metadata updated to match narrowed authority standings.

---

## 4. Test Suite Execution Results

1. **Functional Suite (`scripts/test_task6_functional.py`):** **PASS ✅** (11/11 presets verified for mathematical cover-fit crop geometry; QR decoding matrix verified across logo area coverage; Image compressor binary search verified; Format converter white compositing verified).
2. **SEO Audit Suite (`scripts/verify_all_seo.py`):** **PASS ✅** (38/38 pages checked; 0 title length issues, 0 description length issues, 0 duplicate tags, 0 heading skips across all 37 content pages, 1 primary H1 per page, 0 missing image alts).
3. **Cookie Consent Lifecycle (`scripts/test_cookie_consent_lifecycle.js`):** **PASS ✅** (8/8 scenarios passed).

---

## 5. Git History & Constraints

- **Repository:** https://github.com/BiradarSwapnilDeveloper/PixelCraft_AI
- **Branch:** `feature/seo-development`
- **Base Commit:** `217b65d`
- **Zero merges into main.**
- **Zero pushes to remote.**
- **Zero production deployments.**
