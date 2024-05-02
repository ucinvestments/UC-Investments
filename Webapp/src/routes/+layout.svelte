<script>
  import "../app.css";
  import { dev } from "$app/environment";
  import { inject } from "@vercel/analytics";
  inject({ mode: dev ? "development" : "production" });
</script>

<br />
<hr class="h-px mx-8 bg-black border-0 dark:bg-gray-700" />
<hr class="h-px mx-8 bg-black border-0 dark:bg-gray-700" />
<div class="w-full text-center m-auto p-1">
  <a
    href="/"
    class="a bold mx-2  transition-colors duration-300 text-[var(--pri)] hover:text-[var(--sec)]"
    >UC Investments Explorer</a
  >
<a
    href="/sources"
    class="a bold mx-2 transition-colors duration-300 text-[var(--black)] hover:text-[var(--blackHover)]"
    >Sources</a
  >
  <a
    href="/about"
    class="a bold mx-2 transition-colors duration-300 text-[var(--black)] hover:text-[var(--blackHover)]"
    >About</a
  >
</div>

<hr class="h-px mx-8 bg-black border-0 dark:bg-gray-700" />
<hr class="h-px mx-8 bg-black border-0 dark:bg-gray-700" />
<slot />

<div class="m-10"></div>

<style>
  :global(body) {
    letter-spacing: 0.1em;
  }

  /* Dynamic font size using viewport width (vw) */

  .a {
    font-size: clamp(
      1rem,
      2rem,
      3rem
    ); /* Use clamp() to set a minimum and maximum font size */
  }

  .dropdown-btn:focus + .dropdown-content,
  .dropdown-btn:hover + .dropdown-content,
  .dropdown-content:hover {
    display: block;
  }

  .dropdown-content {
    display: none;
    position: absolute;
    background-color: var(--bg);
    min-width: 160px;
    box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
    z-index: 1;
  }

  .dropdown-content a {
    color: black;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }

  .dropdown-content a:hover {
    background-color: var(--sec);
  }
</style>
