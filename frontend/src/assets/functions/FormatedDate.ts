export function getFormattedDateTime() {
  const now = new Date();
  const date = now.toLocaleDateString('fr-FR', {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
  });
  const time = now.toLocaleTimeString('fr-FR', {
    hour: '2-digit', minute: '2-digit', hour12: false
  });
  return `${date.replace(/^\w/, c => c.toUpperCase())} - ${time}`;
}
