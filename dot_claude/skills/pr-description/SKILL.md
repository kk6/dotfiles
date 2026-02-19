---
name: pr-description
description: Automatically generate PR descriptions according to project templates.
---

## Instructions

Generate a pull request description by following these steps:

1. **Review the PR Template**
   - Read the `.github/PULL_REQUEST_TEMPLATE.md` file or similar template
   - Understand the structure and sections of the template

2. **Analyze the Changes**
   - Use `git diff` to examine the changes
   - Review the commit history with `git log`
   - Understand the purpose of the modified files

3. **Generate the Description**
   - Fill in all sections of the template
   - Clearly describe the reasons and impact of the changes
   - Include any test plans if available

4. **Complete Generation**
   - Finish generating the description without interruption
   - Verify that all sections are properly filled in

## Output

**Important**: Always wrap the PR description in a ```markdown``` code block when outputting. This allows users to copy and paste the raw Markdown text.

Output format:
```markdown
## Summary
...
```

- Generate a complete PR description following the template
- Ensure the output is wrapped in a code block to prevent Markdown text from rendering
- Make sure Markdown syntax like `##`, `-`, `- [ ]` appears as raw text
