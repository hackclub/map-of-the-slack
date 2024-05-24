<script>
  import "../app.css";
</script>

<svelte:head>
  <title>Hack Club's Map of the Slack</title>
  <meta
    name="description"
    content="An interactive map of the Hack Club Slack!"
  />
</svelte:head>

<div class="h-screen w-screen bg-black">
  <h1 class="py-20 text-center font-serif text-4xl font-bold text-white">
    Hack Club's Map of the Slack
  </h1>
  <main>
    <slot />
  </main>
</div>
