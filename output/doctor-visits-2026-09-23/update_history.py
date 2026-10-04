from pathlib import Path
p=Path('sources/updates-2026-09-23.md')
s=p.read_text()
s+='''

## U20260923-05 — three specialist visits planned; asthma onset and intake updated

Dmytro requests documents for hospital visits today (September 23): allergist follow-up, endocrinologist, and gastroenterologist. These are planned visits, not completed consultations or admission.

Latest partner report: asthma worsened the same night after the last doctor's visit and seems very bad; Lada is largely sleeping or using her nebulizer, with occasional rescue inhaler use. Dmytro questions adequacy of daily asthma treatment and wants examination and a concrete regimen. This latest recollection supersedes the September 21 account placing onset early evening September 19 for purposes of the current handout; no precise clock time is inferred.

For endocrinology he requests assessment of fatigue/sleepiness, thyroid history, possible endocrine contribution to allergy/asthma, and useful additional diagnostics. He reiterates a prior hormone prescription and uncertain recalled autoimmune explanation; no original clinician diagnosis found. Existing original lab reports and the previously clarified spring 2025 Euthyrox course remain the evidence.

For gastroenterology: frequent abdominal pain continues, especially after food and steroids. **Latest estimate: approximately 100 kcal/day for almost a month, now 800–900, possibly 1,000 kcal/day.** This supersedes older 150–200 kcal estimates in new handouts; old reports are preserved. He wants examination and assessment of whether she is safe. No new dietary prescription, medicine change or diagnostic finding supplied.

He also consistently reiterates that clinicians specifically recommended vegetables to strengthen peristalsis; preserve this as relayed advice rather than silently recasting it as a misunderstanding.

Prepared three two-page Ukrainian personal notes, following the archived September 18 allergist and September 14 gastroenterologist handouts; original prescriptions, thyroid reports and September 19 labs visually checked. Notes distinguish prior prescribed doses from uncertain current adherence and include focused questions, not a new treatment plan. Medication clarification requested but no reply available at preparation. Combined six-page packet also saved. See Documents index.
'''
p.write_text(s)
p=Path('HEALTH_CONTEXT.md');s=p.read_text()
new='''**September 23 — visits planned; latest asthma and intake account:** Dmytro plans an allergist follow-up, endocrinologist and gastroenterologist today and requests personal handouts. Latest recollection places asthma worsening **the same night after the last doctor visit**, superseding the earlier September 19 evening onset in new notes. Reports largely sleeping/nebulizing with occasional rescue inhaler, persistent fatigue/sleepiness and abdominal pain especially after food/steroids. Latest estimated intake **~100 kcal/day for almost a month, now 800–900, perhaps 1,000 kcal/day**; prior estimates preserved historically. Wants assessment of current safety and concrete treatment/testing/nutrition decisions. No visits completed or medication changes inferred. [U20260923-05](sources/updates-2026-09-23.md#u20260923-05--three-specialist-visits-planned-asthma-onset-and-intake-updated).

'''
s=s.replace('## Start here\n\n','## Start here\n\n'+new,1)
rows=''
for key,label,meaning in [
 ('allergist-follow-up','Allergist follow-up','Current asthma symptoms, nebulizer amounts, prior controller prescription, steroid uncertainty and focused treatment/assessment questions.'),
 ('endocrinologist','Endocrinologist','Fatigue/sleepiness, original 2025–2026 thyroid results, historical Euthyrox, steroid exposure and focused diagnostic/treatment questions.'),
 ('gastroenterologist-follow-up','Gastroenterologist follow-up','Ongoing post-food/steroid pain, latest intake/weight, obstruction/surgical history, prior prescriptions and nutrition/assessment questions.')]:
 rows+=f'| 2026-09-23 | [{label} PDF](docs/2026-09-23-{key}-uk.pdf) · [Editable notes](docs/2026-09-23-{key}-uk.md) | Two-page Ukrainian personal consultation notes in Dmytro’s voice. {meaning} Prepared from reports/records; not a clinician plan or proof of current adherence. |\n'
rows+='| 2026-09-23 | [All three consultation notes](docs/2026-09-23-doctor-visits-uk.pdf) | Six-page combined printing packet; identical copies of the three specialist notes above. Update together with individual PDFs. |\n'
s=s.replace('| --- | --- | --- |\n','| --- | --- | --- |\n'+rows,1)
s=s.replace('## Update log\n\n','## Update log\n\n- **2026-09-23:** U20260923-05 records planned three-specialist visits, latest asthma-onset recollection and ~100 kcal/day month-long intake estimate, now 800–1,000. Created/indexed three two-page Ukrainian personal consultation notes and six-page combined packet using archived handout style and verified original results. No completed visits or new medication instructions inferred.\n\n',1)
p.write_text(s)
