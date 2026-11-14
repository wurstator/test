// Single source of truth for site topics. Add a topic here and it appears everywhere.
export const TOPICS = [
  { id: 'medical',       name: 'Medical',          icon: '🧫', blurb: 'Antibiotics, phages, the microbiome and human health.' },
  { id: 'environmental', name: 'Environmental',    icon: '🌍', blurb: 'Bioremediation, soil, oceans and the carbon cycle.' },
  { id: 'industrial',    name: 'Industrial & Food', icon: '🏭', blurb: 'Fermentation, enzymes, biofuels and biomaterials.' },
  { id: 'agriculture',   name: 'Agriculture',      icon: '🌱', blurb: 'Biofertilisers, biocontrol and plant–microbe partnerships.' },
  { id: 'synbio',        name: 'Synthetic Biology', icon: '🧬', blurb: 'Genetic engineering, CRISPR, sequencing and bioinformatics.' },
  { id: 'fundamentals',  name: 'Fundamentals',     icon: '🔬', blurb: 'What microbes are and how we study them.' },
] as const;

export const TOPIC_IDS = TOPICS.map((t) => t.id) as [string, ...string[]];
export const topicById = (id: string) => TOPICS.find((t) => t.id === id)!;
