<script>
  import { MapLibre, GeoJSON, MarkerLayer, LineLayer } from "svelte-maplibre";

  export let data;
</script>

<svelte:head>
  <title>Home</title>
  <meta name="description" content="Svelte demo app" />
</svelte:head>

<section>
  <MapLibre
    center={[0, 0]}
    zoom={7}
    class="map"
    standardControls
    style="/style.json"
  >
    <GeoJSON id="nodes" data={data.nodes}>
      <MarkerLayer asButton let:feature>
        {@const props = feature.properties}
        <div class="rounded-full bg-orange-200 p-1">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            ><path
              fill="currentColor"
              d="M14 11.5A2.5 2.5 0 0 0 16.5 9A2.5 2.5 0 0 0 14 6.5A2.5 2.5 0 0 0 11.5 9a2.5 2.5 0 0 0 2.5 2.5M14 2c3.86 0 7 3.13 7 7c0 5.25-7 13-7 13S7 14.25 7 9a7 7 0 0 1 7-7M5 9c0 4.5 5.08 10.66 6 11.81L10 22S3 14.25 3 9c0-3.17 2.11-5.85 5-6.71C6.16 3.94 5 6.33 5 9Z"
            /></svg
          >
        </div>
        <span>{props?.name}</span>
      </MarkerLayer>
      <LineLayer
        layout={{ "line-cap": "round", "line-join": "round" }}
        paint={{
          "line-width": 3,
          "line-color": "#000000",
          "line-opacity": 0.6,
        }}
      />
    </GeoJSON>
  </MapLibre>
</section>

<style>
  :global(.map) {
    height: 500px;
  }
</style>
