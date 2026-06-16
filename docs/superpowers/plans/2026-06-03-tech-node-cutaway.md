# Tech Node Cutaway Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a domain-object cutaway expansion to the technology tree, starting with a complete black-powder-standardization dependency stack.

**Architecture:** Extend the existing static `tech-tree.html` node data with optional `cutaway` arrays. Add a right-side `tech-cutaway` renderer that updates inside `selectNode(id)` without changing the tree navigation model.

**Tech Stack:** Static HTML, CSS, vanilla JavaScript, Node.js static verification, Playwright screenshot.

---

### Task 1: Red-Line Checks

**Files:**
- Modify: `07_UI原型/ui-demo/scripts/verify-domain-redesign.mjs`

- [ ] Require `tech-tree.html` to include `tech-cutaway`, `tech-layer-stack`, `dependency-layer`, and black-powder layer labels.
- [ ] Run `node scripts/verify-domain-redesign.mjs` and confirm it fails before implementation.

### Task 2: Cutaway UI

**Files:**
- Modify: `07_UI原型/ui-demo/tech-tree.html`

- [ ] Add CSS for the technology cutaway stack.
- [ ] Add HTML containers for the cutaway title and layer stack in the detail panel.
- [ ] Add `cutaway` data to the black-powder node.
- [ ] Add a generic fallback cutaway for nodes without custom data.
- [ ] Render cutaway layers from `selectNode(id)`.

### Task 3: Verification

**Files:**
- No source changes expected.

- [ ] Run `node scripts/verify-domain-redesign.mjs`.
- [ ] Capture a 1600x900 screenshot of `tech-tree.html`.
- [ ] Inspect the screenshot to ensure the cutaway is visible and text does not overlap.
