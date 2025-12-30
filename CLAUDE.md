# Project-Specific Claude Code Instructions

## Prompt Logging System

This project uses a structured prompt logging system to track session history and build a library of proven prompts.

### Always Log These Prompts to `.claude/PROMPT_LOG.md`

Log significant prompts with timestamp, prompt text, and brief outcome. Always log:

1. **Kickoff** - Project initialization, major feature starts, session resumption
2. **Architecture Decisions** - Design patterns, technology choices, structural changes
3. **Multi-iteration Refinements** - Prompts that required multiple rounds to get right
4. **Pivots** - Direction changes, significant scope adjustments
5. **Bug Fixes** - Problem investigation and resolution
6. **Recovery/Corrections** - Course corrections, fixing misunderstandings

### Entry Format

```markdown
### YYYY-MM-DD HH:MM
**Prompt**: [The actual prompt text or concise summary]

**Outcome**: [Brief note on results, learnings, or next steps]

**Category**: [Kickoff | Architecture | Refinement | Bug Fix | Recovery | Meta/Process]
```

### Extract Proven Prompts to `.claude/prompt-library/`

When a prompt is particularly effective:
1. Create a new `.md` file in the appropriate category subdirectory
2. Follow the template in `.claude/prompt-library/README.md`
3. Include context, expected outcome, variations, and lessons learned
4. Use descriptive kebab-case filenames

### Categories in prompt-library/
- **project-setup/** - Environment, tooling, initialization
- **architecture/** - Design decisions, patterns, system structure
- **debugging/** - Problem investigation, error resolution
- **refinement/** - Code improvements, optimization, refactoring

### Workflow
1. At session start, review `PROMPT_LOG.md` for context
2. During session, log significant prompts as they occur
3. At session end or when discovering effective prompts, extract to prompt-library
4. Browse prompt-library before starting new major features

## Project Context

*[Add project-specific context, conventions, and instructions here as the project evolves]*

### Technology Stack
- Reachy Mini robotics platform
- Python applications
- React/TypeScript web interfaces

### Development Notes
- This is a collection of applications for the Reachy Mini robot
- Deployment involves SSH to reachy-mini device
- Web apps typically run on custom ports (8000-8080 range)
