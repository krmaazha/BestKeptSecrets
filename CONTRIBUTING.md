# Contributing to Best Kept Secrets

First off, thank you for considering contributing to Best Kept Secrets! It's people like you that make this list such a great resource for everyone.

## Quality Standards

To maintain the high quality of this repository, please ensure your suggestion meets these criteria:

1. **Utility:** The tool must solve a real problem well.
2. **Relevance:** It should fit cleanly into one of our existing categories.
3. **Quality:** The tool should be well-maintained, stable, and generally recognized as a good solution. We avoid listing abandoned projects or tools that are just starting out unless they offer something truly revolutionary.
4. **No Duplicates:** Please search the README to ensure the tool hasn't already been added.

## How to Suggest a Tool

The easiest way to suggest a tool is to open an issue using the [Suggest a Tool](https://github.com/your-username/BestKeptSecrets/issues/new?template=suggest-tool.yml) issue template.

## How to Submit a Pull Request

If you'd like to add the tool yourself via a Pull Request, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b add-tool-name`.
3. Add your entry to the `README.md` file in the appropriate category.
4. Ensure your entry exactly matches our required format.
5. Commit your changes: `git commit -m 'Add Tool Name to Category'`.
6. Push to the branch: `git push origin add-tool-name`.
7. Submit a Pull Request using our template.

## Required Entry Format

Every entry must strictly follow this exact formatting:

```markdown
- 🟢 [**Tool Name**](https://link.com) — Brief description of what it does and why it's great.
  `Pricing` `Type` · ⚠️ *Security note or privacy consideration.*
  > 💡 **Use case:** When and why you'd use this.
```

### Format Breakdown:

- **Security Icon:** 🟢 (Safe), 🟡 (Caution), or 🔴 (Warning). See README for definitions.
- **Link:** Bolded tool name linked to the official website or repository.
- **Description:** One clear, concise sentence ending with a period.
- **Tags:** Enclosed in backticks (e.g., `` `Free` ``). Use standard tags like Free, Freemium, Paid, Open Source, Self-Hosted.
- **Security Note:** Prefaced with `· ⚠️ *` and ending with `.*`. Should describe any data collection or privacy considerations. Use `· ✅ *` if there are positive privacy features to highlight.
- **Use Case Blockquote:** Starts with `> 💡 **Use case:**` followed by a practical example of when to use the tool.

### Example Entry:

```markdown
- 🟢 [**Obsidian**](https://obsidian.md) — Markdown-based knowledge base with bidirectional linking.
  `Freemium` · ✅ *Notes stored as local Markdown files. Sync is paid but optional.*
  > 💡 **Use case:** Building a personal knowledge base / second brain with interconnected notes and ideas.
```

Thank you for contributing!
