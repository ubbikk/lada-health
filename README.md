# Lada health

A local, updateable health history with a searchable source archive.

**Start with [HEALTH_CONTEXT.md](HEALTH_CONTEXT.md).** It contains a short orientation, recent developments, detailed history, medications, test results, uncertainties and source references. Its current cutoff is September 9, 2026.

The structure keeps everyday context manageable:

- **CLINICIAN_BRIEF_2026-09-08.md:** concise latest handover for a treating clinician.
- **sources/updates-2026-09-08.md:** new interview provenance, linked to the preserved original notes.
- **output/pdf/allergist-followup-draft.pdf** and **.md:** Ukrainian follow-up discussion draft, September 9.
- **HEALTH_CONTEXT.md:** the main working document, updated as information arrives.
- **sources/transcript.md:** the original conversation's user/assistant text, searched only when detail is needed.
- **sources/user-messages.md:** a quicker way to find reported events without the AI advice.
- **sources/attachments/:** six saved and checked medical/symptom images.
- **AGENTS.md:** project instructions to read the context, preserve evidence distinctions and maintain the record. Codex supports project instructions through this file; see [official documentation](https://learn.chatgpt.com/docs/agent-configuration/agents-md).

For a future task in this workspace, a useful opening is:

> Read HEALTH_CONTEXT.md. Here is the new development: … Update the history, then help me with …

The Markdown file can also be attached to a separate chat. Files here do not automatically synchronize with every ChatGPT conversation. Other chats can be imported from supplied links or exports when needed; only the linked anaphylaxis conversation has been imported so far.

The source archive preserves Russian/Ukrainian passages as written. The main summary is English. Old AI advice is kept for traceability and is not an endorsed treatment plan.

## Adding an update

Record the event date, what happened, who reported it, any measurements, treatment actually taken and the outcome. Add original reports/images where available. Update the recent-status section and medication/test status, retaining earlier events in the history. Important contradictions should stay visible until resolved.

## Import scope

Imported September 6, 2026 from the shared conversation linked in the context file: 143 user/assistant messages spanning August 11–September 6. The first history reaches back to 2022. Six attachments were saved and visually checked; other attachments remain placeholders with clearly labeled secondary transcriptions where available.

The HTML, decoded conversation and extraction script in sources/ are retained to make the import reproducible. They are not needed for routine reading. No files were published or sent to a clinician.
