# GATA3-centered program annotations in stimulated CD4+ T cells (48 h)

These are working, state-level annotations for the 14 programs in
`gene_centric_GATA3_Stim48hr.html`. They combine the highest absolute signed
loadings, the regulator/mediator labels in the graph, and GO Biological
Process/Reactome enrichment. They should not be read as proof of direct
regulation by GATA3.

## Program labels

| Modeled direction | Program | Effect | Working label | Main evidence in this program | Confidence |
|---|---:|---:|---|---|---|
| P → GATA3 | P1 | +0.033 | CD244/ABCC4 metabolic, TCR-low | CD244, ABCC4, MYB; opposing PLCG1, ZAP70, VAV1 | Low |
| P → GATA3 | P3 | +0.351 | FOXP1/FBXO32 activation restraint | KPNA1, FBXO32, FOXP1, HHLA2; opposing TADA2B | Medium |
| P → GATA3 | P4 | +0.053 | Innate-like inflammatory migration | ANXA1, AOAH, AIF1, GSDMD, CSF1; inflammatory-response and Rac/migration enrichment | Medium |
| P → GATA3 | P6 | +0.321 | IL-2/IL-23-responsive GZMK+ helper | IL2RA, IL23R, GZMK, AHR, STAT3, ITK; IL-2/IL-23 and lymphocyte-activation enrichment | High |
| P → GATA3 | P7 | +0.493 | CCR4+CCR8+ type-2 priming | CCR4, CCR8, BCL6, LAT2; Th2-differentiation enrichment | High |
| P → GATA3 | P8 | +0.251 | IL-5+ cytotoxic/innate-like effector | IL5, CTSW, CXCR6, IL10 with FCER1G, PLCG2, CCR1; cytokine/immune-effector enrichment | Medium |
| P → GATA3 | P9 | +0.068 | TCR–NF-κB / IL-22 effector | ZAP70, BCL10, NRAS, IL22, CCL3, IL7R | High |
| GATA3 → P | P0 | +0.113 | Metallothionein stress, Th17-low | ADAM19, MT1X/MT1E/MT2A; opposing CCR6, IL23R, IL22, CCR4 | High |
| GATA3 → P | P1 | +0.026 | Metal stress + CCR6/IL23R state | DNTTIP1, TARBP2, MT1X/MT1E/MT2A, CCR6, IL23R; opposing IL7R | Medium |
| GATA3 → P | P3 | +0.102 | ER/proteostasis + helper-receptor state | SPPL2A, MOGS, HM13, NAA30 with CCR6, IL23R, IL17RB; opposing metallothioneins | Medium |
| GATA3 → P | P5 | +0.131 | KPNA1/SLC2A1 effector metabolism | KPNA1, SLC2A1, APBB1IP, DIAPH1, IL5; opposing IKZF2 and KLRG1 | Medium |
| GATA3 → P | P6 | −0.066 | YTHDF2/CBLB activation restraint | YTHDF2, CBLB, IL17RB, CCR5; program score inversely associated with GATA3 | High |
| GATA3 → P | P8 | −0.063 | TXNIP/RASGRP1 TCR set-point, type-2-low | TXNIP, RASGRP1, KLF13, HOPX; opposing IL5, IL17RB, CYP1B1 | High |
| GATA3 → P | P9 | +0.027 | MYB/IKZF2 NF-κB restraint | NFKBIL1, MYB, IKZF2, ERAP1; opposing IL17RB, RGS1, CXCL8 | Medium |

## Interpretation notes

- The clearest GATA3-associated state is upstream P7. CCR4/CCR8 and the
  enrichment result support a type-2 interpretation, but BCL6 argues for
  “type-2 priming/modulation” rather than a fully committed canonical Th2
  label. BCL6 can repress GATA3-dependent Th2 transcription.
- Upstream P6 is a mixed activated helper program. IL23R/AHR/STAT3 support a
  Th17-like component, while IL2RA/GZMK/GIMAP4 indicate activation and an
  effector-memory-like state. It is intentionally not labeled simply “Th17.”
- Upstream P8 is biologically mixed. IL5 supports a type-2 effector component,
  CTSW/CXCR6 support an activated cytotoxic or tissue-associated component, and
  FCER1G/PLCG2/CCR1/SORL1 are unusually innate/myeloid-like for purified CD4+
  T cells.
- Downstream P0, P1, and P3 separate the metallothionein/metal-stress axis into
  related but oppositely oriented states. P0 is explicitly called Th17-low
  because CCR6, IL23R, and IL22 have negative loadings.
- Downstream P6 and P8 are best interpreted as activation-control axes.
  YTHDF2 is induced during early T-cell activation, CBLB sets an inhibitory
  TCR threshold, TXNIP constrains glucose uptake/growth, and RASGRP1 couples the
  TCR to Ras–ERK signaling.
- Effects with approximately |effect| < 0.07 are weak in this graph. Their
  biological labels can still describe the gene axis, but the inferred link to
  GATA3 should be treated cautiously.

## QC checks before using these as final labels

1. For P4 and P8, check per-cell CD3D/CD3E/TRAC expression, doublet scores,
   ambient-RNA correction, and donor consistency before calling an innate-like
   CD4 state.
2. Confirm that the signed loadings are stable across donors or bootstrap
   fits. A label based on one or two high-loading genes is less reliable than
   one supported by the whole program.
3. Compare program scores against protein or independent markers where
   possible: CCR4/CCR8 and IL-5 for type 2; CCR6/IL-23R and IL-22 for
   Th17/Th22-like activity; CD69, IL2RA, and GZMK for activation/effector state.
4. Keep the arrow direction distinct from gene-loading direction. A positive
   program effect does not mean every gene in that program is positively
   regulated; negative-loading genes move with the opposing pole.

## Biological references used to calibrate the labels

- Human CCR6+ helper cells induced with IL-23-associated conditions express
  IL23R and Th17 cytokines including IL22:
  [Boniface et al., J Exp Med (2009)](https://pmc.ncbi.nlm.nih.gov/articles/PMC2699124/).
- Activated human IL17RB+ CD4+ cells show a GATA3/IL5/IL13 type-2 profile:
  [Lam et al., J Allergy Clin Immunol (2016)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4852988/).
- BCL6 can repress GATA3 transcriptional activity and GATA3-dependent IL5:
  [Sawant et al., J Immunol (2012)](https://pmc.ncbi.nlm.nih.gov/articles/PMC3490013/).
- YTHDF2 rises during early anti-CD3/CD28 T-cell activation, including the
  3–48 h window:
  [Zhang et al., Nature Communications (2024)](https://pmc.ncbi.nlm.nih.gov/articles/PMC11538425/).
- CBLB functions as a negative regulator of activation in primary human T-cell
  perturbation screens:
  [Shifrut et al., Cell (2018)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6689405/).
- TXNIP is high in naïve T cells and is rapidly downregulated as human T cells
  increase glucose uptake after stimulation:
  [Muri et al., Sci Rep (2019)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6853882/).
- RASGRP1 is required for optimal antigen-receptor-triggered Ras–ERK activation
  in T cells:
  [Roose et al., Mol Cell Biol (2005)](https://pmc.ncbi.nlm.nih.gov/articles/PMC1140631/).

