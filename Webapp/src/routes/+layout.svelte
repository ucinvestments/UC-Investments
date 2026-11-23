<script lang="ts">
  import "../app.css";
  import { dev, browser } from "$app/environment";
  import { inject } from "@vercel/analytics";
  import { page } from "$app/stores";
  import posthog from "posthog-js";
  import { onMount } from "svelte";
  import Navbar from "$lib/components/Navbar.svelte";
  import Footer from "$lib/components/Footer.svelte";

  let { children } = $props();

  const navLinks = [
    { href: "/", label: "Explorer" },
    { href: "/about", label: "About" },
    { href: "/resources", label: "Resources" },
    {
      href: "https://github.com/ucinvestments/UC-Investments",
      label: "GitHub",
      external: true,
    },
  ];

  const footerLinks = [
    { href: "/", label: "Explorer" },
    { href: "/about", label: "Methodology" },
    { href: "/resources", label: "Resources" },
    {
      href: "https://www.ucop.edu/investment-office/",
      label: "UC Investment Office",
      external: true,
    },
  ];

  const cryptoAddresses = [
    { label: "ETH", address: "0x623c7559ddC51BAf15Cc81bf5bc13c0B0EA14c01" },
    {
      label: "XMR",
      address:
        "44bvXALNkxUgSkGChKQPnj79v6JwkeYEkGijgKyp2zRq3EiuL6oewAv5u2c7FN7jbN1z7uj1rrPfL77bbsJ3cC8U2ADFoTj",
    },
  ];

  onMount(() => {
    if (browser) {
      inject({ mode: dev ? "development" : "production" });
      posthog.init("phc_3vyk0G3UGOLR5TBAPt3ksbHbGbRNOI42aGZsoWvrBzU", {
        api_host: "/ingest",
        ui_host: "https://us.posthog.com",
        capture_pageview: false,
        capture_pageleave: true,
        person_profiles: "always",
        session_recording: {
          maskAllInputs: false,
          maskInputOptions: { password: true, email: true },
        },
        persistence: "localStorage+cookie",
        cross_subdomain_cookie: false,
        secure_cookie: true,
        loaded: () => {
          if (dev) console.log("PostHog loaded");
        },
      });
    }
  });

  $effect(() => {
    if (browser && $page.url) {
      posthog.capture("$pageview", {
        $current_url: $page.url.href,
        $pathname: $page.url.pathname,
        $title: typeof document !== "undefined" ? document.title : "",
      });
    }
  });
</script>

<Navbar links={navLinks} />

<main>
  {@render children?.()}
</main>

<Footer
  appName="STEM4Palestine's UC Investment Data Explorer"
  description="Transparency in university endowment and pension fund management."
  links={footerLinks}
  contactEmail="admin@ucinvestments.info"
  altContactEmail="sdokita@berkeley.edu"
  {cryptoAddresses}
  copyrightHolder="STEM4Palestine"
  affiliationDisclaimer="Not affiliated with or authorized by the University of California."
/>

<style>
  :global(html) {
    scroll-behavior: smooth;
  }

  main {
    min-height: calc(100vh - 400px);
  }
</style>
