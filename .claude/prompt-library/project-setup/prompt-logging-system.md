# Set Up Prompt Logging System

## Context
Use this prompt when starting a new project or adding a prompt logging system to an existing project. This creates infrastructure to track session history, learn from effective prompts, and build a reusable prompt library.

## Prompt
```
Set up a prompt logging system for this project:

  1. Create `.claude/PROMPT_LOG.md` with this structure:
     - Header explaining its purpose (track session history, enable learning)
     - Sections: Kickoff, Architecture Decisions, Refinements, Bug Fixes, Recovery/Corrections, Meta/Process
     - Entry format: timestamp, prompt text, brief outcome note

  2. Create `.claude/prompt-library/` directory with README.md explaining:
     - Purpose: curated, proven prompts for Claude Code interactions
     - Structure: subdirectories by category (project-setup/, architecture/, debugging/, refinement/)
     - Template for adding new prompts

  3. Create `CLAUDE.md` in project root (NOT in .claude/) to instruct future Claude sessions to:
     - Log significant prompts to `.claude/PROMPT_LOG.md`
     - Always log: project kickoff, architecture changes, multi-iteration refinements, pivots, bug fixes
     - Extract proven prompts to `.claude/prompt-library/` when valuable
     - Use format: timestamp, prompt text, brief outcome note
     - Note: Claude Code automatically reads CLAUDE.md from project root at session start

  4. If this project has a separate `prompts/` directory for system/runtime prompts, keep them separate and clarify in README.

  5. Review conversation history and log all significant prompts from this session.

  After setup, confirm structure and prompts captured.

  Also saved to: .claude/prompt-library/project-setup/prompt-logging-system.md
```

## Expected Outcome
Creates a complete prompt logging infrastructure:
- `.claude/PROMPT_LOG.md` - Session history with categorized entries (in .claude/)
- `.claude/prompt-library/` - Curated library of proven prompts with subdirectories (in .claude/)
- `CLAUDE.md` - Instructions for future Claude sessions on logging practices (in project root)
- Initial logging of current session's significant prompts
- Self-documenting: this prompt itself is saved to the library

**Important**: `CLAUDE.md` goes in project root, not `.claude/`. The `.claude/` folder is for Claude Code internal settings and cache.

## Variations

### Minimal Version
If you want a simpler system without the full prompt library:
```
Create `.claude/PROMPT_LOG.md` with sections for: Kickoff, Architecture, Refinements, Bug Fixes, Recovery, Meta. Include timestamp, prompt, and outcome for each entry. Create `CLAUDE.md` in project root to instruct future sessions to log significant prompts here.
```

### With Custom Categories
Adapt categories to your project type:
- **Data Engineering**: data-pipeline/, schema-design/, etl-jobs/, monitoring/
- **Web Apps**: frontend/, backend/, api-design/, deployment/
- **ML Projects**: model-training/, data-preparation/, evaluation/, deployment/

### Existing Project Migration
```
Review our conversation history and extract all significant prompts to `.claude/PROMPT_LOG.md`. Then set up the full prompt logging system with library for future sessions.
```

## Notes
- The system is self-bootstrapping: this setup prompt becomes the first library entry
- Logging discipline improves with practice - start by logging everything, refine over time
- The prompt library grows organically through actual use, not upfront planning
- Review PROMPT_LOG.md at session start for context continuity
- Extract to library when prompts prove valuable through repeated use

## Related Prompts
- `resume-from-logs.md` - Starting a new session with historical context
- `extract-learnings.md` - Mining logs for patterns and improvements
- `prompt-refinement.md` - Iteratively improving prompts based on outcomes
