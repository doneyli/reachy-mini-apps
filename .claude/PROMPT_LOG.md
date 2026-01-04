# Prompt Log

## Purpose
This log tracks significant prompts and interactions across Claude Code sessions. It serves as:
- A session history for continuity across conversations
- A learning tool to identify effective prompting patterns
- A reference for future sessions on this project
- Source material for extracting proven prompts to the prompt library

## Entry Format
Each entry should include:
- **Timestamp**: Date and time of the prompt
- **Prompt**: The actual prompt text (or summary for very long prompts)
- **Outcome**: Brief note on results, learnings, or next steps
- **Category**: One of: Kickoff, Architecture, Refinement, Bug Fix, Recovery, Meta/Process

---

## Kickoff
*Initial project setup, major feature starts, or session initialization*

### 2025-12-29 (Session Start)
**Prompt**: Set up a prompt logging system for this project with `.claude/PROMPT_LOG.md`, `.claude/prompt-library/`, and instructions in `CLAUDE.md` (project root)

**Outcome**: Created comprehensive logging infrastructure including:
- This PROMPT_LOG.md file in .claude/
- prompt-library/ with categorized subdirectories in .claude/
- CLAUDE.md in project root (corrected from initial .claude/ location)
- Saved setup prompt as reusable template

**Category**: Kickoff

---

## Architecture Decisions
*Significant architectural choices, design patterns, technology selections*

---

## Refinements
*Iterative improvements, optimizations, code quality enhancements*

---

## Bug Fixes
*Problem identification and resolution, debugging sessions*

---

## Recovery/Corrections
*Course corrections, pivot decisions, fixing misunderstandings*

### 2025-12-29 - CLAUDE.md Location Correction
**Prompt**: "there's a major mistake. CLAUDE.md goes in the project root, not inside a .claude folder. Claude Code automatically reads CLAUDE.md from the root when you start a session in that directory."

**Outcome**: Moved CLAUDE.md from `.claude/CLAUDE.md` to project root `./CLAUDE.md`. Updated all documentation to reflect correct structure. Key learning: `.claude/` is for Claude Code internal settings/cache, not project instructions.

**Category**: Recovery

---

## Meta/Process
*Workflow improvements, tooling setup, development process changes*

### 2026-01-03 14:30
**Prompt**: "I want to document in the README that the credentials for ssh to the Reachy-mini are: username: pollen pass: root"

**Outcome**: Added "SSH Access to Reachy Mini" section to README.md with default credentials and connection command. Positioned after SDK connection information for logical grouping of device access details.

**Category**: Meta/Process

---

## Notes
- Log prompts that took multiple iterations to get right
- Include context that would help future sessions understand decisions
- Extract particularly effective prompts to `.claude/prompt-library/`
- Update categories as project needs evolve
