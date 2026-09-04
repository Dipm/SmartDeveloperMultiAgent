---
name: fetch-jira-ticket
description: Pull title, description, acceptance criteria, linked tickets, and comments for a ticket ID via Jira MCP. Use when triage starts. Do not edit Jira.
disable-model-invocation: true
---

# Fetch Jira ticket

Use Jira MCP (`getJiraIssue`, links, comments) for the ticket ID.

Collect: title, description, acceptance criteria, linked tickets, comments.

If MCP is unavailable, use a body the parent pasted. If neither exists, stop.

Do not `createJiraIssue`, `editJiraIssue`, `transitionJiraIssue`, or comment
on the ticket. Read-only.
