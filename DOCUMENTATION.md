# Documentation Index

This file provides a quick reference to all documentation in the Ondansetron systematic review project.

## 📚 Main Documentation Files

### [README.md](README.md) - **START HERE** 
**Primary project documentation**
- Project overview and features
- Installation and quick start guide
- Complete CLI tools documentation
- Project structure explanation
- Manuscript workflow
- Development guidelines
- Contributing instructions
- Environment setup

**Audience**: Everyone (developers, users, researchers)

### [AGENTS.md](AGENTS.md)
**Multi-agent workflow coordination**
- Workflow principles and branch strategy
- File ownership and conflict prevention
- Agent-specific guidelines (GitHub Copilot, Claude, OpenCode)
- Task assignment and tracking
- Coordination mechanisms
- Code review protocols
- Best practices

**Audience**: AI agents working on the project (GitHub Copilot, Claude Code, etc.)

### [TODO.md](TODO.md)
**Project roadmap and task tracking**
- High priority tasks
- Manuscript tasks (content, formatting, review)
- CLI tools improvements and features
- Data and analysis tasks
- Documentation tasks
- Infrastructure and future enhancements
- Progress tracking with milestones

**Audience**: Project contributors, maintainers, and stakeholders

## 🤖 AI Assistant Documentation

### [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md)
**General AI agent instructions**
- Quick reference guide
- Project structure overview
- Key commands and typical tasks
- Code and data organization
- Tool development features
- Guidelines for AI assistants

**Audience**: General AI assistants (Codex CLI, generic agents)

### [CLAUDE.md](CLAUDE.md)
**Claude Code specific instructions**
- Development commands
- Architecture overview
- Environment requirements
- Manuscript review strategy
- Development workflow guidelines

**Audience**: Claude Code (claude.ai/code)

### [OpenCode.md](OpenCode.md)
**OpenCode development guidelines**
- Build and test commands
- Code style conventions
- Formatting rules
- Notebook usage

**Audience**: OpenCode assistant

## 📖 Quick Navigation by Task

### I want to...

**Get started with the project:**
→ [README.md](README.md) - Installation and Quick Start sections

**Use the CLI tools:**
→ [README.md](README.md) - CLI Tools section

**Work on the manuscript:**
→ [README.md](README.md) - Manuscript Workflow section  
→ [TODO.md](TODO.md) - Manuscript Tasks section

**Develop new features:**
→ [README.md](README.md) - Development section  
→ [TODO.md](TODO.md) - CLI Tools Tasks section  
→ [OpenCode.md](OpenCode.md) - Code Style guidelines

**Coordinate with other agents:**
→ [AGENTS.md](AGENTS.md) - Complete multi-agent coordination guide

**See what needs to be done:**
→ [TODO.md](TODO.md) - All tasks and priorities

**Configure API keys:**
→ [README.md](README.md) - Environment Variables section

**Build the manuscript PDF:**
→ [README.md](README.md) - Manuscript Workflow section

**Run tests:**
→ [README.md](README.md) - Development section  
→ [OpenCode.md](OpenCode.md) - Build & Test section

**Submit a contribution:**
→ [README.md](README.md) - Contributing section  
→ [AGENTS.md](AGENTS.md) - Workflow principles

## 📁 Other Documentation

### In the Repository

- **`pyproject.toml`** - Python package configuration and dependencies
- **`pytest.ini`** - Test configuration
- **`manuscript/memoire.md`** - Main manuscript (includes YAML front matter with abstract)
- **`manuscript/Makefile`** - Build commands for PDF/DOCX generation

### External Resources

- [PRISMA Guidelines](http://www.prisma-statement.org/) - Systematic review standards
- [Cochrane Handbook](https://training.cochrane.org/handbook) - Review methodology
- [uv Documentation](https://github.com/astral-sh/uv) - Package manager
- [Pandoc Manual](https://pandoc.org/MANUAL.html) - Document conversion

## 🔄 Documentation Maintenance

### When to Update Documentation

- **README.md**: When adding features, changing installation, or updating commands
- **AGENTS.md**: When changing workflow, adding agents, or updating coordination rules
- **TODO.md**: Continuously as tasks are completed or added
- **AI_INSTRUCTIONS.md**: When project structure changes or new patterns emerge
- **CLAUDE.md**: When Claude-specific workflows change
- **OpenCode.md**: When code style or build process changes

### Documentation Standards

All documentation should:
- ✅ Use clear, concise language
- ✅ Include code examples where appropriate
- ✅ Maintain consistent formatting
- ✅ Cross-reference related documentation
- ✅ Be kept up-to-date with code changes
- ✅ Follow Markdown best practices

## 📊 Documentation Coverage

```
README.md          ████████████████████ 100% Complete
AGENTS.md          ████████████████████ 100% Complete
TODO.md            ████████████████████ 100% Complete (Living Document)
AI_INSTRUCTIONS.md ████████████████████ 100% Complete
CLAUDE.md          ████████████████████ 100% Complete
OpenCode.md        ████████████████████ 100% Complete
```

## 🆘 Getting Help

If you can't find what you're looking for:

1. **Check [README.md](README.md) first** - Most common information is there
2. **Search across all docs** - Use `grep` or your IDE's search
3. **Check [TODO.md](TODO.md)** - Your question might be on the roadmap
4. **Review [AGENTS.md](AGENTS.md)** - For coordination and workflow questions
5. **Create an issue** - If documentation is unclear or missing

---

**Last Updated**: 2025-10-21  
**Maintained by**: Project contributors and AI agents  
**Status**: Complete and actively maintained
