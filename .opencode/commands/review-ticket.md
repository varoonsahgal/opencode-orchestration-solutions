---
description: Review everything changed since the starter tag against TICKET-001
agent: reviewer
---

DO:     Review the change below against tickets/TICKET-001.md, using your checklist.
READ:   tickets/TICKET-001.md, plus every file listed below.
RULES:  Above 20% → pending_approval; exactly 20% → active. The service decides, never the importer.
TOUCH:  Nothing.
DONE:   Every checklist item has a verdict. If nothing changed, say so.
REPORT: findings by severity with file:line · missing tests · anything you guessed.

Changed files (?? = new, not in the diff below; read them yourself):
!`git status --short`

The change since the starter tag:
!`git diff starter`
