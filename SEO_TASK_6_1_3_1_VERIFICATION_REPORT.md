# PixelCraft AI — SEO Task 6.1.3.1: Final SSC & UPSC Preset Corrections Report

**Repository:** `https://github.com/BiradarSwapnilDeveloper/PixelCraft_AI`  
**Active Branch:** `feature/seo-development`  
**Base Commit:** `16b435a`  
**Task Status:** COMPLETE  
**Production Deployment:** **STRICTLY NOT DEPLOYED — NOT MERGED INTO `main`**

---

## 1. Executive Summary

This surgical corrective pass completes **SEO Task 6.1.3.1: Final SSC & UPSC Preset Corrections**, addressing subtle notification inconsistencies and separating distinct examination mandates:

1. **SSC 4 cm vs. 6 cm Discrepancy Transparently Resolved:**
   - Addressed the official textual discrepancy found in Staff Selection Commission (SSC) publications:
     - Notice Variant 1 (Annexures / Select Guidelines): *"about $4.0\text{ cm}\text{ (width)}\times 2.0\text{ cm}\text{ (height)}$"* ($2:1$ aspect ratio).
     - Notice Variant 2 (Main Application Instructions in CGL / CHSL / MTS): *"about $6.0\text{ cm}\text{ (width)}\times 2.0\text{ cm}\text{ (height)}$"* ($3:1$ aspect ratio).
   - Documented that SSC application servers enforce **10 KB to 20 KB** file size limits in JPG/JPEG format and reject block/capital signatures, rather than calculating rigid sub-millimeter pixel boundaries.
2. **Unsupported 200 × 100 px Equivalence Removed:**
   - Eliminated all occurrences of the unverified $200\times 100\text{ px}$ claim across preset arrays, button labels, candidate advisories, and Schema.org FAQ structured data. Presets now represent clean, unskewed aspect ratios based directly on the physical centimeter notice variants ($400\times 200\text{ px}$ for $2:1$ ratio and $600\times 200\text{ px}$ for $3:1$ ratio).
3. **Current UPSC CSE / OTR Instructions Separated from Older ORA Rules:**
   - **Current UPSC CSE (Civil Services Exam) & Central OTR (2024+):**
     - Mandatory photograph recency rule: Photo must **not be more than 10 days old** from the start of the online application window.
     - Mandatory text imprint: Candidate's **name** (in capital letters) and **date on which photograph was taken (DOP)** clearly printed at the bottom.
     - Facial coverage: Candidate's face must occupy **$\sim 75\%$** of the frame.
     - Dimensions: $350\times 350$ to $1000\times 1000\text{ px}$ ($1:1$ square ratio), $20-300\text{ KB}$ in JPG format.
   - **Older / Advertisement-Specific UPSC ORA Rules:**
     - Direct recruitment to specialized posts (e.g., Medical Officers, Scientists) on `upsconline.nic.in`.
     - Validates within the same general technical envelope ($350\times 350$ to $1000\times 1000\text{ px}$, $20-300\text{ KB}$), but individual vacancy advertisements determine specific document formatting requirements rather than universally enforcing the 10-day CSE rule.
4. **All Improvements Preserved:**
   - QR Generator conservative Classic Square defaults, dynamic scanner compatibility advisory, and SVG vector scannability remain intact.
   - Image Compressor byte-for-byte retention of already-compliant images (e.g. 11.2 KB signature file) remains untouched.

---

## 2. Granular Code Changes Matrix

| Target File | Component / Line Range | Previous Text / Behavior | Corrected Implementation (Task 6.1.3.1) |
|---|---|---|---|
| [`smart-resize.html`](file:///d:/AI%20tools%20Website/public/tools/smart-resize.html) | **Popular Presets Bar** (Lines 252–253) | `✍️ SSC Signature (~4.0x2.0 cm)` and `🏛️ UPSC OTR Photo (500x500 px)` | Corrected to: `✍️ SSC Signature (4x2 cm / 6x2 cm)` and `🏛️ UPSC CSE / OTR Photo (500x500 px)`. |
| [`smart-resize.html`](file:///d:/AI%20tools%20Website/public/tools/smart-resize.html) | **`PLATFORMS` Array** (Lines 316–319) | Contained `SSC Scanned Signature (Suggested ~4.0x2.0 cm: 200x100 px, 10-20 KB)` and bundled `UPSC OTR / ORA Photo` | Split into: (1) `SSC Scanned Signature (~4.0x2.0 cm Notice Variant / 2:1 Ratio)` ($400\times 200\text{ px}$), (2) `SSC Scanned Signature (~6.0x2.0 cm Notice Variant / 3:1 Ratio)` ($600\times 200\text{ px}$), (3) `UPSC CSE / OTR Photo (Current 10-Day Rule: 500x500 px)`, (4) `UPSC ORA Portal Photo (General Upload Bounds: 350x350 px)`. |
| [`smart-resize.html`](file:///d:/AI%20tools%20Website/public/tools/smart-resize.html) | **Candidate Advisory Box** (Lines 748–750) | Generic mention of SSC 4x2 cm with 200x100 px and bundled UPSC OTR/ORA | Detailed transparent explanation of SSC 4 cm vs. 6 cm discrepancy across notices; separated Current UPSC CSE 10-day DOP rule from individual ORA vacancy notices. |
| [`smart-resize.html`](file:///d:/AI%20tools%20Website/public/tools/smart-resize.html) | **Section 5 Cards 3 & 4** (Lines 770–784) | Contained unsupported 200x100 px equivalence | Replaced with detailed analysis of SSC physical centimeter standards and distinct UPSC CSE vs. ORA operational frameworks. |
| [`smart-resize.html`](file:///d:/AI%20tools%20Website/public/tools/smart-resize.html) | **Schema.org JSON-LD FAQ** (Lines 100–135) | Q2, Q4, Q5 referenced 200x100 px or grouped UPSC | Updated Q2 (SSC 4 cm vs 6 cm without 200x100 px), Q4 (SSC 4 cm vs 6 cm explanation), and Q5 (UPSC CSE/OTR vs ORA distinction). |
| [`smart-resize.html`](file:///d:/AI%20tools%20Website/public/tools/smart-resize.html) | **Section 6 Visible FAQs** (Lines 810–835) | Q2, Q4, Q5 visible cards | Fully synchronized with the updated Schema.org JSON-LD FAQ questions and answers. |
| [`image-compressor.html`](file:///d:/AI%20tools%20Website/public/tools/image-compressor.html) | **Section 5 Signature Target** (Line 877) | Referenced `SSC (~4.0×2.0 cm, 10–20KB)` | Updated to: `SSC (4×2 cm or 6×2 cm notice variants, 10–20KB)` to reflect both notice standards. |
| [`scripts/test_task6_functional.py`](file:///d:/AI%20tools%20Website/scripts/test_task6_functional.py) | **Test Preset Array** (Lines 88–97) | Evaluated single 200x100 px SSC entry | Expanded to evaluate both SSC Notice Variants ($400\times 200\text{ px}$ and $600\times 200\text{ px}$) and both UPSC standards ($500\times 500\text{ px}$ CSE/OTR and $350\times 350\text{ px}$ ORA). |

---

## 3. Presets & Dimension Standards Reference

| Preset Label | Physical / Official Source Standard | Canonical Aspect Ratio | Target Pixel Resolution in Preset | Byte Constraints | Authority & Regulatory Context |
|---|---|:---:|:---:|:---:|---|
| **SSC Scanned Signature (Variant 1)** | About $4.0\text{ cm}\text{ (W)}\times 2.0\text{ cm}\text{ (H)}$ | $2.0000$ ($2:1$) | $400\times 200\text{ px}$ | $10-20\text{ KB}$ | **SSC Notice Variant 1**: Appears in application annexures and select notification guidelines. Requires dark pen running signature on white paper. |
| **SSC Scanned Signature (Variant 2)** | About $6.0\text{ cm}\text{ (W)}\times 2.0\text{ cm}\text{ (H)}$ | $3.0000$ ($3:1$) | $600\times 200\text{ px}$ | $10-20\text{ KB}$ | **SSC Notice Variant 2**: Appears in main application instructions for CGL, CHSL, MTS, and GD. |
| **UPSC CSE / Central OTR Photo** | 10-Day Recency + Name/Date Imprint | $1.0000$ ($1:1$) | $500\times 500\text{ px}$ | $20-300\text{ KB}$ | **Current UPSC CSE Instructions (2024+)**: Must not be $>10$ days old; candidate's name and DOP imprinted at bottom; 75% facial coverage; appearance consistency required. |
| **UPSC ORA Portal Photo** | General System Validation Envelope | $1.0000$ ($1:1$) | $350\times 350\text{ px}$ | $20-300\text{ KB}$ | **UPSC ORA Direct Recruitment**: General system upload envelope ($350\times 350$ min to $1000\times 1000$ max). Specific terms govern per individual vacancy notice. |
| **IBPS Candidate Photo** | Dimensions $200\times 230\text{ px}$ (Preferred) | $0.8696$ | $200\times 230\text{ px}$ | $20-50\text{ KB}$ | **IBPS Official Standard**: Pixel dimensions designated as preferred; file weight mandatory. |
| **IBPS Scanned Signature** | Dimensions $140\times 60\text{ px}$ (Preferred) | $2.3333$ ($7:3$) | $140\times 60\text{ px}$ | $10-20\text{ KB}$ | **IBPS Official Standard**: Black ink on white paper; 10-20 KB mandatory. |
| **Indian Passport Photo** | $35\times 45\text{ mm}$ ($413\times 531\text{ px}$ at $300\text{ DPI}$) | $0.7778$ ($7:9$) | $413\times 531\text{ px}$ | N/A | **MEA Optional Physical Print**: Live digital capture at Counter A for adult PSK applicants. |
| **PAN Card (UTIITSL)** | $213\times 213\text{ px}$ at $300\text{ DPI}$ | $1.0000$ ($1:1$) | $213\times 213\text{ px}$ | $<30\text{ KB}$ | **Suggested Convenience Preset (Unverified)**: Applicable to physical document upload mode. |
| **PAN Card (Protean/NSDL)** | $2.5\times 3.5\text{ cm}$ | $0.7143$ | $200\times 280\text{ px}$ | $<50\text{ KB}$ | **Suggested Convenience Preset (Unverified)**: Applicable to physical document upload mode. |

---

## 4. Empirical Verification & Test Matrix Results

### 1. Preset Aspect Ratio & Cover-Fit Geometry Test
Executed via [`scripts/test_task6_functional.py`](file:///d:/AI%20tools%20Website/scripts/test_task6_functional.py):
- Evaluated all 11 presets on simulated test captures.
- Tested bicubic resampling and centered cover-fit cropping.
- **Result:** $100\%$ of cropped outputs precisely match target width and height without aspect ratio distortion or edge distortion. Status: **PASS ✅**.

### 2. Live Browser DOM State Audit (Chrome MCP)
Evaluated dynamically on `http://localhost:8080/tools/smart-resize.html` using Chrome MCP:
- `govtPresetsCount`: **11 presets active in DOM**.
- `faqQuestionsCount`: **11 questions in Schema.org JSON-LD FAQPage**.
- `visibleFaqCount`: **11 questions in visible HTML Section 6**.
- Console messages: 0 JavaScript errors or unhandled exceptions.

### 3. Comprehensive SEO Regression Suite
Executed via [`scripts/verify_all_seo.py`](file:///d:/AI%20tools%20Website/scripts/verify_all_seo.py):
- Title length audit: **0 titles exceed 60 characters** across all 38 public HTML pages.
- Meta description length audit: **0 descriptions exceed 160 characters** across all 38 pages.
- Uniqueness audit: **0 duplicate titles, 0 duplicate descriptions**.
- Heading hierarchy audit: **0 heading skips (H1 $\to$ H2 $\to$ H3 $\to$ H4)** across all 37 content pages.
- Primary H1 check: **Exactly 1 primary H1 tag per content page**.
- Orphan page check: `/download-app.html` linked from 4 separate pages.
- Image alt attributes: **0 missing alt tags** across all pages.
- **Overall SEO Suite Status: PASS ✅**.

### 4. Cookie Consent Lifecycle Suite
Executed via [`scripts/test_cookie_consent_lifecycle.js`](file:///d:/AI%20tools%20Website/scripts/test_cookie_consent_lifecycle.js):
- 8/8 automated lifecycle scenarios passed:
  - Scenario 1 (First-time visitor): PASS ✅
  - Scenario 2 (Accept All): PASS ✅
  - Scenario 3 (Reject All): PASS ✅
  - Scenario 4 (Refresh after accept): PASS ✅
  - Scenario 5 (Refresh after reject): PASS ✅
  - Scenario 6 (Navigation idempotency): PASS ✅
  - Scenario 7 (Preference reopening & revocation): PASS ✅
  - Scenario 8 (HTML codebase audit across 38 files): PASS ✅

---

## 5. Repository & Branch Integrity Notice

- **Active Branch:** `feature/seo-development`.
- **Merge Status:** **NOT MERGED INTO `main`**.
- **Deployment Status:** **NOT DEPLOYED TO PRODUCTION**.
- **Remote Status:** **NO PUSH TO REMOTE EXECUTED**.
