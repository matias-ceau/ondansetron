# Multi-Agent Workflow Coordination

This document provides guidelines for coordinating multiple AI agents working on the Ondansetron systematic review project. It ensures consistent behavior, prevents conflicts, and maintains project integrity when multiple agents are working in parallel.

## 🎯 Overview

This project is designed to support multiple AI agents working collaboratively:

- **GitHub Copilot**: Code completion, PR reviews, issue resolution
- **Claude Code**: Comprehensive code analysis, refactoring, documentation
- **OpenCode**: Development assistance, debugging, testing
- **Other AI Assistants**: Custom agents for specific tasks

## 🔄 General Workflow Principles

### Branch Strategy

**ALWAYS follow this workflow:**

1. **Create a new branch** when starting a modification round
   ```bash
   git checkout -b copilot/feature-name
   # or
   git checkout -b agent-name/task-description
   ```

2. **Make focused changes** on your assigned files/components

3. **Commit regularly** with clear, descriptive messages
   ```bash
   git add .
   git commit -m "descriptive message about changes"
   ```

4. **Push changes** to remote
   ```bash
   git push origin branch-name
   ```

5. **Create Pull Request** when work is complete

6. **Merge after review** and the cycle continues

### Parallel Work Guidelines

Multiple agents can work simultaneously on:
- ✅ **Different files** (encouraged)
- ✅ **Different sections** of the manuscript
- ✅ **Different CLI tools** in `src/ondansetron/`
- ✅ **Different data files** in `sourcedata/`
- ⚠️ **Same file** (requires careful coordination - see below)

### File Ownership & Coordination

To prevent conflicts, agents should respect these guidelines:

#### Core Files (Coordinate Before Editing)
- `manuscript/memoire.md` - Main manuscript (use sections to divide work)
- `manuscript/memoire.bib` - Bibliography (atomic edits only)
- `pyproject.toml` - Package configuration
- `README.md`, `AGENTS.md`, `TODO.md` - Documentation

#### Agent-Specific Files (Safe for Independent Work)
- `src/ondansetron/*.py` - Python modules (one agent per module)
- `tests/*.py` - Test files (one agent per test file)
- `sourcedata/*.json` - Data files (different files per agent)
- `manuscript/llm/` - LLM-generated content (separate files)

## 🤖 Agent-Specific Guidelines

### GitHub Copilot

**Primary Responsibilities:**
- Code completion and suggestions
- Pull request reviews
- Issue resolution and bug fixes
- Small, focused code improvements

**Best Practices:**
- Focus on single-purpose PRs
- Provide clear PR descriptions
- Reference related issues
- Keep changes minimal and surgical
- Always run tests before finalizing

**Branch Naming:** `copilot/issue-number-description` or `copilot/feature-name`

### Claude Code (claude.ai/code)

**Primary Responsibilities:**
- Comprehensive code analysis and refactoring
- Documentation updates and creation
- Complex multi-file changes
- Architecture decisions
- Testing strategy

**Best Practices:**
- Read `CLAUDE.md` for project-specific instructions
- Use `rg` for searching (not `grep`)
- Preserve YAML front matter in markdown files
- Follow existing code style strictly
- Check coherence across all modified files
- Use `uv` for all Python operations

**Branch Naming:** `claude/task-description`

**See [CLAUDE.md](CLAUDE.md) for detailed Claude-specific instructions.**

### OpenCode

**Primary Responsibilities:**
- Development environment setup
- Interactive debugging
- Test execution and validation
- Build process management

**Best Practices:**
- Refer to `OpenCode.md` for guidelines
- Use consistent code formatting
- Follow PEP8 conventions
- Maintain test coverage

**Branch Naming:** `opencode/task-name`

**See [OpenCode.md](OpenCode.md) for detailed OpenCode-specific instructions.**

### Custom Agents

**For specialized agents working on specific tasks:**

1. **Document your role** in this file
2. **Claim ownership** of specific files/modules
3. **Coordinate** with other agents via PR comments
4. **Follow** general workflow principles
5. **Update** TODO.md with your progress

**Branch Naming:** `agent-name/task-description`

## 📋 Task Assignment System

### Current Active Tasks

Track active work to avoid conflicts:

| Task | Agent | Branch | Files | Status |
|------|-------|--------|-------|--------|
| Documentation update | GitHub Copilot | copilot/update-readme-and-agents-file | README.md, AGENTS.md, TODO.md | In Progress |
| (Add new tasks here) | | | | |

### Claiming a Task

**Before starting work:**

1. Check the table above for conflicts
2. Add your task to the table
3. Commit the updated AGENTS.md
4. Create your branch
5. Begin work

**After completing work:**

1. Update task status to "Completed"
2. Create pull request
3. Remove task after merge

## 🔍 Coordination Mechanisms

### Before Starting Work

```bash
# 1. Pull latest changes
git fetch origin
git checkout main
git pull origin main

# 2. Check active branches
git branch -a | grep copilot
git branch -a | grep claude
git branch -a | grep opencode

# 3. Review recent commits
git log --oneline --graph --all -20

# 4. Check for file conflicts
git diff origin/main...origin/other-agent-branch -- path/to/file

# 5. Create your branch
git checkout -b your-agent/your-task
```

### During Work

- **Commit frequently** with descriptive messages
- **Push regularly** to share progress
- **Check for conflicts** periodically
  ```bash
  git fetch origin
  git diff origin/main...HEAD
  ```
- **Update AGENTS.md** task table as you progress

### Resolving Conflicts

If you encounter conflicts:

1. **Communicate** via PR comments or issues
2. **Fetch latest** changes
   ```bash
   git fetch origin
   git merge origin/main
   ```
3. **Resolve manually** - preserve both agents' valid changes
4. **Test thoroughly** after resolution
5. **Commit** with clear conflict resolution message

### Code Review Protocol

When reviewing another agent's work:

- ✅ Check for consistency with project style
- ✅ Verify tests pass
- ✅ Ensure documentation is updated
- ✅ Confirm no unintended side effects
- ✅ Validate minimal change principle
- ❌ Don't rewrite unless necessary
- ❌ Don't introduce new bugs
- ❌ Don't change unrelated code

## 📚 File-Specific Guidelines

### Manuscript (`manuscript/memoire.md`)

**Coordination Strategy: Section-based**

- **Section Ownership**: Different agents can edit different sections
- **YAML Front Matter**: First agent to edit claims ownership, others preserve it
- **Bibliography References**: Coordinate additions to avoid duplicates
- **Build Testing**: Always run `make pdf` after changes

**Claiming a Section:**
```markdown
<!-- AGENT: copilot - SECTION: Introduction - STATUS: editing -->
## Introduction
...
<!-- END AGENT: copilot -->
```

### Python Modules (`src/ondansetron/*.py`)

**Coordination Strategy: Module-based**

- One agent per module at a time
- Document your changes in docstrings
- Update related tests in `tests/`
- Run test suite before committing

### Data Files (`sourcedata/*.json`)

**Coordination Strategy: File-based**

- Each agent works on separate JSON files
- Use descriptive filenames: `agent_name_description.json`
- Keep historical versions in dated directories
- Document schema changes

### Configuration Files

**High Coordination Required:**

- `pyproject.toml`: Coordinate all dependency changes
- `.gitignore`: Discuss additions
- `pytest.ini`: Test configuration changes need review

## 🛠️ Tools & Commands

### Useful Git Commands

```bash
# See what other agents are working on
git branch -a --sort=-committerdate

# Check file history
git log --follow -p -- path/to/file

# See who last modified a file
git log -1 --format="%an <%ae>" -- path/to/file

# Compare branches
git diff branch1...branch2

# List files changed in a branch
git diff --name-only main...your-branch
```

### Python Development

```bash
# Add dependencies (coordinate via pyproject.toml)
uv add package-name

# Run specific tool
uv run ondansetron-search "query"

# Run tests
uv run pytest
uv run pytest tests/test_search.py -v

# Run specific test
uv run pytest tests/test_search.py::test_function_name -v
```

### Manuscript Building

```bash
cd manuscript

# Build PDF
make pdf

# Build DOCX
make docx

# Clean build artifacts
make clean
```

## 📝 Communication Guidelines

### PR Descriptions

Every PR should include:

```markdown
## Purpose
Brief description of what this PR accomplishes

## Changes
- File 1: Description of changes
- File 2: Description of changes

## Agent Information
- Agent: [GitHub Copilot/Claude/OpenCode/Other]
- Related Issues: #123, #456
- Dependencies: PR #789 (if applicable)

## Testing
- [ ] Tests pass
- [ ] Manual testing completed
- [ ] Documentation updated

## Coordination
- Conflicts with: [None/PR #XYZ]
- Coordinated with: [@agent-name]
```

### Commit Messages

Follow this format:

```
type(scope): brief description

Longer description if needed.

Agent: agent-name
Related: #issue-number
```

**Types**: feat, fix, docs, style, refactor, test, chore

### Issue Comments

When coordinating on issues:

```markdown
@agent-name: I'm working on this in branch copilot/feature-name.
Planning to modify files: file1.py, file2.py
ETA: [date]
```

## 🎓 Best Practices

### DO ✅

- **Create branches** for all work
- **Commit frequently** with clear messages
- **Test thoroughly** before pushing
- **Document changes** in code and PRs
- **Coordinate** on shared files
- **Review** other agents' work constructively
- **Update** AGENTS.md task table
- **Keep changes minimal** and focused
- **Follow** existing code style
- **Run tests** before finalizing

### DON'T ❌

- **Force push** (avoid rewriting history)
- **Edit others' active branches** without coordination
- **Make unrelated changes** in the same PR
- **Skip testing** after modifications
- **Delete others' work** without discussion
- **Introduce breaking changes** without warning
- **Work directly on main** branch
- **Commit sensitive data** (API keys, credentials)
- **Ignore conflicts** - resolve them properly
- **Bypass code review** process

## 🔒 Security & Privacy

All agents must:

- **Never commit** API keys or credentials
- **Use environment variables** for sensitive data
- **Check .gitignore** before committing
- **Scan for secrets** in commits
- **Report security issues** immediately

## 📊 Progress Tracking

### Weekly Coordination

Every week, update TODO.md with:
- Completed tasks
- Ongoing work
- Blocked tasks
- Next priorities

### Monthly Review

Review AGENTS.md to:
- Update agent responsibilities
- Adjust coordination strategies
- Document lessons learned
- Improve workflows

## 🆘 Troubleshooting

### Merge Conflicts

1. Identify conflicting files
   ```bash
   git status
   ```

2. Open files and look for conflict markers
   ```
   <<<<<<< HEAD
   Your changes
   =======
   Other agent's changes
   >>>>>>> branch-name
   ```

3. Resolve by keeping both valid changes or choosing one

4. Mark as resolved
   ```bash
   git add resolved-file.py
   git commit -m "Resolve merge conflict in resolved-file.py"
   ```

### Build Failures

If tests fail after pulling changes:

1. Check what changed
   ```bash
   git log --oneline origin/main..HEAD
   ```

2. Review test output carefully

3. If caused by your changes: fix them

4. If caused by others' changes: coordinate to resolve

### Lost Work

If you lose uncommitted work:

```bash
# Check reflog
git reflog

# Recover lost commits
git checkout <commit-hash>
git checkout -b recovery-branch
```

## 🔗 Related Documentation

- [README.md](README.md) - Project overview and usage
- [TODO.md](TODO.md) - Current tasks and roadmap
- [CLAUDE.md](CLAUDE.md) - Claude Code specific instructions
- [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) - General AI agent instructions
- [OpenCode.md](OpenCode.md) - OpenCode guidelines

## 📞 Contact

For questions about multi-agent coordination:
- Create an issue with the `coordination` label
- Tag relevant agents in PR comments
- Update this document with clarifications

---

**Remember: Good coordination prevents conflicts and ensures high-quality collaborative work!**
