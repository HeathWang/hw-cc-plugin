# Git Commit Message Workflow

## Workflow Steps

### Step 1: Check Repository Status
First, check the overall git repository status:
```bash
git status
```
This will show:
- Current branch information
- Staged changes (green text)
- Unstaged changes (red text)
- Untracked files

**⚠️ IMPORTANT: Wait for the output before proceeding to the next step.**

---

### Step 2: Intelligent File Staging (If Needed)

**Scenario A: Files are already staged**
- If `git status` shows "Changes to be committed", proceed directly to **Step 3**

**Scenario B: No files are staged**
- Analyze all modified/untracked files
- Group related files by functionality (e.g., same feature, bug fix, refactor)
- Execute `git add` for files that belong together:
  ```bash
  git add <file1> <file2> <file3> ...
  ```
- **Grouping Strategy**:
  - Feature changes: Model + View + ViewModel + ViewController files
  - Bug fixes: Files related to the same bug
  - Refactoring: Files within the same module/directory
  - Documentation: README, comments, config changes

**⚠️ IMPORTANT: Be selective. Only stage related files for a single commit. Leave unrelated changes for separate commits.**

---

### Step 3: Review Staged Changes & Generate + Execute Commit
After files are staged, review the actual changes:
```bash
git diff --cached
```
Analyze:
- What functionality was added, modified, or removed
- The scope and impact of changes across files
- Related files that were changed together

Then, based on the staged changes analysis, **immediately generate and execute** the commit command with a message following these requirements:

#### Commit Message Requirements
1. The change summary must be listed as numbered items, e.g., '1. ...', '2. ...'
2. Follow Conventional Commits format: `feat`, `fix`, `refactor`, `docs`, `style`, `test`, `chore`, etc.
3. The commit message must be in Chinese
4. Include a summary of the changes, including the number of files modified
5. Use markdown format for git change details
6. Conclude with a creative sequence of 3-5 emojis that reflect the nature of the changes (e.g., ✨ for new features, 🐛 for bugfixes, 🚀 for performance improvements, 🎨 for UI updates)

**⚠️ IMPORTANT: Execute the commit command immediately after generating the message:**
```bash
git commit -m "<generated_commit_message>"
```

---

## Execution Rules

### Decision Flow
```
git status
    ↓
Check if files staged?
    ↓                              ↓
   YES                            NO
    ↓                              ↓
Review staged          → Analyze changes → Group related files → git add → Review staged
    ↓                              ↓
Generate & Execute Commit    ← ← ← ← ← ← ← ← ← ← ← ← ← ← ←
```

### Key Principles
- **Sequential Execution**: Each step must complete before moving to the next
- **No Parallel Execution**: Never run multiple git commands simultaneously
- **No Intermediate Review**: Commit message is generated and executed in the same step
- **Smart Grouping**: Stage related files together; leave unrelated changes for separate commits
- **Output Verification**: Confirm each command's output before proceeding

### Example Scenario

```bash
# Step 1: Check status
$ git status
# Modified: User/Model/User.swift
# Modified: User/View/UserCell.swift
# Modified: User/ViewModel/UserVM.swift
# Modified: Market/View/MarketCell.swift  # ← Unrelated change
# No files staged

# Step 2: Stage related User module files only
$ git add User/Model/User.swift User/View/UserCell.swift User/ViewModel/UserVM.swift

# Step 3: Review and commit
$ git diff --cached  # Review only User module changes
$ git commit -m "feat(user): 重构用户数据模型和视图 (3个文件) ..."

# For the remaining MarketCell.swift change, create a separate commit
```
