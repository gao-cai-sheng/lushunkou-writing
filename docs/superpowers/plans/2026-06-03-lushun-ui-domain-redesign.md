# Lushun UI Domain Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign all 7 static UI prototype pages into a cohesive, domain-accurate historical strategy game interface.

**Architecture:** Keep the static HTML files and existing page scripts, but replace shared styling and page-specific visual surfaces. `ui-kit.css` owns the material system and common shell; each HTML file owns its domain-specific central visualization.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Playwright CLI screenshots, Node.js built-in filesystem checks.

---

### Task 1: Add Red-Line Verification

**Files:**
- Create: `07_UI原型/ui-demo/scripts/verify-domain-redesign.mjs`

- [ ] Write a Node.js static verification script that checks shared CSS tokens, per-page domain markers, `ui-kit.css` linkage, and absence of pictographic emoji glyphs.
- [ ] Run `node scripts/verify-domain-redesign.mjs` and verify it fails against the current prototype.

### Task 2: Replace Shared UI Kit

**Files:**
- Modify: `07_UI原型/ui-demo/ui-kit.css`

- [ ] Define material variables for cold iron, paper, brass, brick alarm, navy steel, snow, soot, and subdued status colors.
- [ ] Restyle app shell, panels, topbar, nav, buttons, badges, bars, bottom bar, scrollbars, and reusable map/card surfaces.
- [ ] Keep existing class names so page scripts continue working.

### Task 3: Redesign Main Defense Screen

**Files:**
- Modify: `07_UI原型/ui-demo/index.html`

- [ ] Link `ui-kit.css` and replace the inline shell styles with page-specific campaign-table styles.
- [ ] Preserve facility selection, map route data, and countdown behavior.
- [ ] Convert map routes, nodes, legend, and alert to military map annotation language.

### Task 4: Redesign Specialist Pages

**Files:**
- Modify: `07_UI原型/ui-demo/bastion-section.html`
- Modify: `07_UI原型/ui-demo/strategic-map.html`
- Modify: `07_UI原型/ui-demo/map-builder.html`
- Modify: `07_UI原型/ui-demo/senate-roster.html`
- Modify: `07_UI原型/ui-demo/diplomacy.html`
- Modify: `07_UI原型/ui-demo/tech-tree.html`

- [ ] Replace page-specific CSS surfaces with domain-object classes.
- [ ] Replace emoji/pictographic glyph data with text labels or CSS marks.
- [ ] Preserve current JS-generated lists, selections, sliders, and controls.

### Task 5: Verify And Screenshot

**Files:**
- No source changes expected.

- [ ] Run `node scripts/verify-domain-redesign.mjs`.
- [ ] Run Playwright screenshots for all 7 HTML files at 1600x900.
- [ ] Inspect screenshots for blank renders, text overlap, broken assets, and console/script errors where practical.
