# Prompt Library

## Purpose
This directory contains curated, proven prompts for Claude Code interactions. These are prompts that have been tested and refined through actual use in this project.

## Structure
Prompts are organized by category in subdirectories:

- **project-setup/** - Project initialization, environment setup, tooling configuration
- **architecture/** - Design decisions, system architecture, technical patterns
- **debugging/** - Problem investigation, error resolution, troubleshooting
- **refinement/** - Code improvements, optimization, refactoring

## Adding New Prompts

### When to Add a Prompt
Extract prompts to this library when they:
- Produced particularly good results
- Required multiple iterations to perfect
- Solve a problem likely to recur
- Demonstrate an effective pattern
- Could benefit future sessions or other projects

### Template for New Prompts
Create a new `.md` file in the appropriate category with this format:

```markdown
# [Brief Descriptive Title]

## Context
When to use this prompt / what problem it solves

## Prompt
```
[The actual prompt text]
```

## Expected Outcome
What this prompt should achieve

## Variations
- Alternative phrasings or adaptations
- Context-specific modifications

## Notes
- Lessons learned
- Common pitfalls to avoid
- Related prompts
```

### Naming Convention
Use descriptive kebab-case filenames:
- `setup-logging-system.md`
- `debug-api-timeout.md`
- `refactor-component-structure.md`

## Usage Tips
- Browse this library before starting new features
- Adapt prompts to your specific context
- Update prompts when you discover improvements
- Cross-reference from PROMPT_LOG.md when extracting
- Include enough context for standalone use

## Maintenance
- Review quarterly for outdated prompts
- Consolidate similar prompts
- Update based on new Claude Code features
- Remove prompts that no longer apply
