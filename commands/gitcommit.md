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

### Step 4: Loop Check & Continue
After executing the commit, **loop back to Step 1** to check if there are still files waiting to be committed:
```bash
git status
```

**Decision Logic:**
- If `git status` shows **no staged or unstaged changes**, the workflow is complete 🎉
- If `git status` shows **remaining changes** (staged or unstaged), repeat from **Step 2** to group and commit the next set of related files
- Continue this loop until all changes are committed

**⚠️ IMPORTANT: Each iteration should handle a logically related group of files. Do not commit unrelated files together.**

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
    ↓
git status (Loop back)
    ↓
Any remaining changes? 
    ↓                              ↓
   YES                            NO (Done 🎉)
    ↓                              ↓
Repeat from Step 2              Workflow Complete
```

### Key Principles
- **Sequential Execution**: Each step must complete before moving to the next
- **No Parallel Execution**: Never run multiple git commands simultaneously
- **No Intermediate Review**: Commit message is generated and executed in the same step
- **Smart Grouping**: Stage related files together; leave unrelated changes for separate commits
- **Output Verification**: Confirm each command's output before proceeding
- **Continuous Loop**: Automatically repeat the workflow until all changes are committed
- **One Logical Unit Per Commit**: Each commit should represent a single, cohesive change or feature

### Example Scenario

```bash
# 初始状态：4个未提交文件，分为2个功能模块
$ git add User/Model/User.swift User/View/UserCell.swift User/ViewModel/UserVM.swift
$ git commit -m "feat(user): 重构用户数据模型和视图 (3个文件)
1. 更新 User 数据模型以支持新字段
2. 优化 UserCell 视图展示逻辑
3. 重构 UserVM 以适配新的数据结构

🎨✨🚀"

# 循环检测：剩余1个未提交文件（Market模块）
$ git add Market/View/MarketCell.swift
$ git commit -m "fix(market): 修复 MarketCell 显示问题 (1个文件)
1. 修正商品价格显示格式
2. 优化图片加载逻辑

🐛🔧✅"

# 循环检测：工作区干净，所有变更已提交 🎉
```
