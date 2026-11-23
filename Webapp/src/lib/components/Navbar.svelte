<script lang="ts">
  import { page } from "$app/state";

  let {
    links,
  }: { links: { href: string; label: string; external?: boolean }[] } =
    $props();
</script>

<header class="site-header">
  <nav aria-label="Main navigation">
    <a href="/" class="wordmark">
      <span class="brand-mark" aria-hidden="true"><i></i><i></i><i></i></span>
      <span
        ><strong>UC Investments</strong><small>by STEM4Palestine</small></span
      >
    </a>
    <div class="site-links">
      {#each links as link (link.href)}
        <a
          href={link.href}
          aria-current={page.url.pathname === link.href ? "page" : undefined}
          target={link.external ? "_blank" : undefined}
          rel={link.external ? "noopener noreferrer" : undefined}
        >
          {link.label}{#if link.external}
            <span aria-hidden="true">↗</span>{/if}
        </a>
      {/each}
    </div>
  </nav>
</header>

<style>
  .site-header {
    background: #fff;
    border-bottom: 1px solid #e0e7f3;
    color: #152238;
  }
  nav {
    width: min(1280px, calc(100% - 96px));
    margin: auto;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 5px 12px;
    min-height: 69px;
  }
  .wordmark {
    display: flex;
    align-items: center;
    gap: 9px;
    line-height: 1.2;
    padding-block: 9px;
  }
  .wordmark strong {
    display: block;
    font-size: 0.98rem;
    letter-spacing: -0.04em;
  }
  .wordmark small {
    display: block;
    margin-top: 2px;
    font-size: 0.66rem;
    color: #50617a;
  }
  .brand-mark {
    width: 35px;
    height: 35px;
    display: flex;
    align-items: end;
    justify-content: center;
    gap: 2px;
    padding-bottom: 9px;
    border-radius: 8px;
    background: #1d49c5;
  }
  .brand-mark i {
    display: block;
    width: 4px;
    height: 7px;
    border-radius: 1px;
    background: #c0d1ff;
  }
  .brand-mark i:nth-child(2) {
    height: 12px;
  }
  .brand-mark i:nth-child(3) {
    height: 17px;
    background: #fff;
  }
  .site-links {
    display: flex;
    flex-wrap: wrap;
    gap: 6px 17px;
    align-items: center;
  }
  .site-links a {
    color: #425472;
    font-weight: 600;
    font-size: 0.83rem;
    display: flex;
    gap: 3px;
    padding-block: 10px;
  }
  .site-links a:hover,
  .site-links a[aria-current] {
    color: #1d49c5;
    text-decoration: underline;
    text-underline-offset: 5px;
  }
  a:focus-visible {
    outline: 2px solid #3163e8;
    outline-offset: 3px;
  }
  @media (max-width: 900px) {
    nav {
      width: calc(100% - 40px);
    }
  }
  @media (max-width: 620px) {
    nav {
      width: calc(100% - 32px);
      min-height: 59px;
      gap: 0 12px;
    }
    .site-links {
      gap: 2px 12px;
    }
    .site-links a {
      font-size: 0.76rem;
    }
  }
</style>
