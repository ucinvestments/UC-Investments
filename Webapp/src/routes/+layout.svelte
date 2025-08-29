<script>
  import "../app.css";
  import { dev } from "$app/environment";
  import { inject } from "@vercel/analytics";
  import { fade } from "svelte/transition";
  import { page } from "$app/stores";
  import Icon from "@iconify/svelte";
  inject({ mode: dev ? "development" : "production" });
  import posthog from "posthog-js";
  import { browser } from "$app/environment";
  import { onMount } from "svelte";

  export const load = async () => {
    if (browser) {
      posthog.init("phc_3vyk0G3UGOLR5TBAPt3ksbHbGbRNOI42aGZsoWvrBzU", {
        api_host: "https://us.i.posthog.com",
        defaults: "2025-05-24",
        person_profiles: "always", // or 'always' to create profiles for anonymous users as well
      });
    }

    return;
  };
</script>

<nav class="navbar">
  <div class="nav-container">
    <a href="/" class="logo-link">
      <div class="logo">
        <Icon icon="mdi:chart-donut" class="logo-icon" />
        <span class="logo-text">UC Investments</span>
      </div>
    </a>

    <div class="nav-links">
      <a href="/" class="nav-link" class:active={$page.url.pathname === "/"}>
        <Icon icon="mdi:home" class="nav-icon" />
        Explorer
      </a>
      <a
        href="/about"
        class="nav-link"
        class:active={$page.url.pathname === "/about"}
      >
        <Icon icon="mdi:information" class="nav-icon" />
        About
      </a>
      <a
        href="https://github.com/TheArctesian/UC-Investments"
        target="_blank"
        rel="noopener noreferrer"
        class="nav-link external"
      >
        <Icon icon="mdi:github" class="nav-icon" />
        GitHub
        <Icon icon="mdi:open-in-new" class="external-icon" />
      </a>
    </div>
  </div>
</nav>

<main in:fade={{ duration: 300 }}>
  <slot />
</main>

<footer class="footer">
  <div class="footer-content">
    <div class="footer-section">
      <h4 class="footer-title">UC Investment Explorer</h4>
      <p class="footer-text">
        Transparency in university endowment and pension fund management.
      </p>
    </div>

    <div class="footer-section">
      <h4 class="footer-title">Quick Links</h4>
      <div class="footer-links">
        <a href="/" class="footer-link">Explorer</a>
        <a href="/about" class="footer-link">Methodology</a>
        <a
          href="https://www.ucop.edu/investment-office/"
          target="_blank"
          rel="noopener noreferrer"
          class="footer-link"
        >
          UC Investment Office
          <Icon icon="mdi:open-in-new" class="footer-external" />
        </a>
      </div>
    </div>

    <div class="footer-section">
      <h4 class="footer-title">Data Sources</h4>
      <p class="footer-text">
        Last updated: May 2024<br />
        Data accuracy: ~68%
      </p>
    </div>
  </div>

  <div class="footer-bottom">
    <p>&copy; 2024 UC Investment Explorer. Educational purposes only.</p>
  </div>
</footer>

<style>
  :global(html) {
    scroll-behavior: smooth;
  }

  .navbar {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid var(--border);
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
  }

  .nav-container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .logo-link {
    text-decoration: none;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    transition: transform 0.3s ease;
  }

  .logo:hover {
    transform: scale(1.05);
  }

  :global(.logo-icon) {
    font-size: 2rem;
    color: var(--founder);
  }

  .logo-text {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--pri);
    letter-spacing: -0.01em;
  }

  .nav-links {
    display: flex;
    gap: 0.5rem;
    align-items: center;
  }

  .nav-link {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    padding: 0.625rem 1.25rem;
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    border-radius: 0.75rem;
    transition: all 0.2s ease;
    position: relative;
  }

  :global(.nav-icon) {
    font-size: 1.125rem;
  }

  .nav-link:hover {
    background: var(--bg-secondary);
    color: var(--pri);
    transform: translateY(-1px);
  }

  .nav-link.active {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
  }

  .nav-link.external {
    border: 2px solid var(--border);
  }

  :global(.external-icon) {
    font-size: 0.875rem;
    margin-left: -0.125rem;
  }

  main {
    min-height: calc(100vh - 400px);
  }

  .footer {
    background: linear-gradient(180deg, var(--bg-secondary) 0%, white 100%);
    border-top: 1px solid var(--border);
    margin-top: 4rem;
    padding: 3rem 0 1.5rem;
  }

  .footer-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 2rem;
    display: grid;
    grid-template-columns: 2fr 1fr 1fr;
    gap: 3rem;
    margin-bottom: 2rem;
  }

  .footer-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .footer-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0;
  }

  .footer-text {
    color: var(--text-secondary);
    line-height: 1.6;
    font-size: 0.925rem;
    margin: 0;
  }

  .footer-links {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .footer-link {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    color: var(--text-secondary);
    text-decoration: none;
    font-size: 0.925rem;
    transition: all 0.2s ease;
    width: fit-content;
  }

  .footer-link:hover {
    color: var(--founder);
    transform: translateX(4px);
  }

  :global(.footer-external) {
    font-size: 0.75rem;
  }

  .footer-bottom {
    max-width: 1400px;
    margin: 0 auto;
    padding: 2rem 2rem 0;
    border-top: 1px solid var(--border);
    text-align: center;
  }

  .footer-bottom p {
    color: var(--text-secondary);
    font-size: 0.875rem;
    margin: 0;
  }

  @media (max-width: 768px) {
    .nav-container {
      flex-direction: column;
      gap: 1rem;
      padding: 1rem;
    }

    .nav-links {
      width: 100%;
      justify-content: center;
    }

    .nav-link {
      padding: 0.5rem 1rem;
      font-size: 0.875rem;
    }

    :global(.nav-icon) {
      font-size: 1rem;
    }

    .logo-text {
      font-size: 1.125rem;
    }

    .footer-content {
      grid-template-columns: 1fr;
      gap: 2rem;
      padding: 0 1.5rem;
    }

    .footer-section {
      text-align: center;
    }

    .footer-links {
      align-items: center;
    }
  }

  @media (max-width: 480px) {
    .nav-links {
      flex-direction: column;
      width: 100%;
    }

    .nav-link {
      width: 100%;
      justify-content: center;
    }
  }
</style>
