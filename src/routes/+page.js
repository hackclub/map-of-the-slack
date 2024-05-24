// since there's no dynamic data here, we can prerender
// it so that it gets served as a static asset in production
export const prerender = true;

/** @type {import('./$types').PageLoad} */
export async function load({ fetch }) {
  const nodes = await (await fetch("/geojson.json")).json();

  return {
    nodes,
  };
}
