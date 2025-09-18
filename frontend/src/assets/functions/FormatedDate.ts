export function formatedTimestamp(timestamp: string) {
  const date = new Date(timestamp);

  const optionsDate = { day: "2-digit" as const, month: "2-digit" as const, year: "numeric" as const };
  const optionsHeure = { hour: "2-digit" as const, minute: "2-digit" as const, hour12: false };

  const dateFormatee = date.toLocaleDateString("fr-FR", optionsDate);
  const heure = date.toLocaleTimeString("fr-FR", optionsHeure);

  return `${dateFormatee} - ${heure}`;
}
