<script>
  import { fade, fly } from "svelte/transition";
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";

  let mounted = false;

  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted}
  <div class="ice-container">
    <!-- Hero Section -->
    <div class="ice-hero" in:fade={{ duration: 800 }}>
      <div class="hero-content">
        <Icon icon="mdi:shield-alert" class="hero-icon" />
        <h1 class="hero-title">ICE Out LA</h1>
        <p class="hero-subtitle">
          Legal Support for ICE Raid Documentation
        </p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="content-wrapper">
      <!-- Contact Information -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 200 }}
      >
        <div class="section-header">
          <Icon icon="mdi:information" class="section-icon" />
          <h2 class="section-title">Legal Documentation Request</h2>
        </div>

        <div class="content-card">
          <div class="alert-card">
            <Icon icon="mdi:gavel" class="alert-icon" />
            <p class="alert-text">
              I am in contact with the ACLU legal team that is suing DHS/ICE and other officials on behalf of people arrested by ICE during raids in LA/Pasadena over the past few months.
            </p>
          </div>

          <p class="section-intro">
            The legal team is seeking credible media that can speak to the illegal behavior being carried out by ICE/homeland/police agents as a result of policy or direct orders.
          </p>
        </div>
      </section>

      <!-- What We Need Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 400 }}
      >
        <div class="section-header">
          <Icon icon="mdi:file-document-multiple" class="section-icon" />
          <h2 class="section-title">Documentation Needed</h2>
        </div>

        <div class="content-card">
          <p class="section-intro">
            We are specifically looking for <strong>interviews, video footage, text or image posts</strong> of/about raid(s) which occurred in LA by:
          </p>

          <div class="evidence-grid">
            <div class="evidence-card">
              <div class="evidence-header">
                <Icon icon="mdi:account-group" class="evidence-icon" />
                <h3>Victims & Bystanders</h3>
              </div>
              <p>
                Documentation from people who witnessed or were affected by ICE raids in the LA/Pasadena area
              </p>
            </div>

            <div class="evidence-card">
              <div class="evidence-header">
                <Icon icon="mdi:shield-account" class="evidence-icon" />
                <h3>ICE/Homeland Agents</h3>
              </div>
              <p>
                Especially those that reference their orders, aims, or state of mind during operations
              </p>
            </div>

            <div class="evidence-card">
              <div class="evidence-header">
                <Icon icon="mdi:office-building" class="evidence-icon" />
                <h3>Administration Officials</h3>
              </div>
              <p>
                Leaders in the ICE network (e.g. Greg Bovino, etc)  especially those that reference orders, aims, or state of mind
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Requirements Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 600 }}
      >
        <div class="section-header">
          <Icon icon="mdi:check-circle" class="section-icon" />
          <h2 class="section-title">Requirements</h2>
        </div>

        <div class="content-card">
          <div class="requirement-list">
            <div class="requirement-item">
              <Icon icon="mdi:check-bold" class="requirement-icon" />
              <span>Information must be <strong>credible</strong></span>
            </div>
            <div class="requirement-item">
              <Icon icon="mdi:check-bold" class="requirement-icon" />
              <span>Information must be <strong>legally obtained</strong></span>
            </div>
          </div>

          <div class="disclaimer-card">
            <Icon icon="mdi:alert-circle-outline" class="disclaimer-icon" />
            <div class="disclaimer-content">
              <p>
                <strong>Important Disclaimer:</strong> I am not a lawyer, and this is not a promise of legal advice or services. I can only pass on any and all stories, videos, posts, etc that could be compelling to the legal team.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- Contact Section -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 800 }}
      >
        <div class="section-header">
          <Icon icon="mdi:message-text" class="section-icon" />
          <h2 class="section-title">Contact</h2>
        </div>

        <div class="content-card">
          <div class="contact-info">
            <div class="contact-method">
              <Icon icon="simple-icons:signal" class="contact-icon" />
              <div class="contact-details">
                <h3>Signal</h3>
                <p class="contact-handle">@mj_.18</p>
              </div>
            </div>
          </div>

          <div class="security-note">
            <Icon icon="mdi:security" class="security-icon" />
            <p>
              Signal provides end-to-end encryption for secure communication. Your privacy and safety are important.
            </p>
          </div>
        </div>
      </section>

      <!-- Additional Resources -->
      <section
        class="content-section"
        in:fly={{ y: 30, duration: 600, delay: 1000 }}
      >
        <div class="section-header">
          <Icon icon="mdi:link-variant" class="section-icon" />
          <h2 class="section-title">Know Your Rights</h2>
        </div>

        <div class="content-card">
          <p class="section-intro">
            If you have been affected by ICE enforcement actions, it's important to know your rights and have access to legal resources.
          </p>

          <div class="resource-links">
            <a
              href="https://www.aclu.org/know-your-rights/immigrants-rights/"
              target="_blank"
              rel="noopener noreferrer"
              class="resource-button"
            >
              <Icon icon="mdi:scale-balance" class="button-icon" />
              ACLU Immigration Rights
            </a>
            <a
              href="https://www.nilc.org/get-involved/community-education-resources/know-your-rights/"
              target="_blank"
              rel="noopener noreferrer"
              class="resource-button secondary"
            >
              <Icon icon="mdi:information" class="button-icon" />
              NILC Know Your Rights
            </a>
          </div>
        </div>
      </section>
    </div>
  </div>
{/if}

<style>
  .ice-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg), var(--bg-secondary));
  }

  .ice-hero {
    background: linear-gradient(135deg, #dc2626 0%, #7f1d1d 100%);
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .ice-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.05'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }

  .hero-content {
    max-width: 800px;
    margin: 0 auto;
    position: relative;
    z-index: 1;
  }

  :global(.hero-icon) {
    font-size: 3rem;
    color: #fbbf24;
    margin-bottom: 1rem;
  }

  .hero-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2.5rem;
    font-weight: 700;
    color: white;
    margin-bottom: 1rem;
    letter-spacing: -0.02em;
  }

  .hero-subtitle {
    font-size: 1.125rem;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.6;
    margin: 0;
  }

  .content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 2rem;
  }

  .content-section {
    margin-bottom: 4rem;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  :global(.section-icon) {
    font-size: 2rem;
    color: #dc2626;
  }

  .section-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--pri);
    margin: 0;
    letter-spacing: -0.01em;
  }

  .content-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 2.5rem;
    box-shadow: var(--shadow-md);
  }

  .alert-card {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
    border: 2px solid #f59e0b;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  :global(.alert-icon) {
    font-size: 1.5rem;
    color: #d97706;
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .alert-text {
    margin: 0;
    color: #92400e;
    font-weight: 500;
    line-height: 1.6;
  }

  .section-intro {
    font-size: 1.125rem;
    line-height: 1.7;
    margin-bottom: 2rem;
    color: var(--text-primary);
  }

  .evidence-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 2rem;
  }

  .evidence-card {
    background: var(--bg-secondary);
    border-radius: 1rem;
    padding: 1.5rem;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
  }

  .evidence-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  .evidence-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1rem;
  }

  :global(.evidence-icon) {
    font-size: 1.5rem;
    color: #dc2626;
  }

  .evidence-card h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0;
  }

  .evidence-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin: 0;
  }

  .requirement-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .requirement-item {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    font-size: 1.125rem;
  }

  :global(.requirement-icon) {
    font-size: 1.25rem;
    color: #16a34a;
    flex-shrink: 0;
  }

  .disclaimer-card {
    background: linear-gradient(135deg, #fee2e2, #fecaca);
    border: 2px solid #f87171;
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  :global(.disclaimer-icon) {
    font-size: 1.5rem;
    color: #dc2626;
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .disclaimer-content p {
    margin: 0;
    color: #7f1d1d;
    line-height: 1.6;
  }

  .contact-info {
    margin-bottom: 2rem;
  }

  .contact-method {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    padding: 2rem;
    background: var(--bg);
    border-radius: 1rem;
    border: 1px solid var(--border);
  }

  :global(.contact-icon) {
    font-size: 2.5rem;
    color: #2563eb;
  }

  .contact-details h3 {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--pri);
    margin: 0 0 0.5rem 0;
  }

  .contact-handle {
    font-family: 'Courier New', monospace;
    font-size: 1.125rem;
    font-weight: 600;
    color: #2563eb;
    margin: 0;
    background: rgba(37, 99, 235, 0.1);
    padding: 0.25rem 0.5rem;
    border-radius: 0.375rem;
    display: inline-block;
  }

  .security-note {
    background: linear-gradient(135deg, #e0f2fe, #b3e5fc);
    border: 2px solid #0288d1;
    border-radius: 1rem;
    padding: 1.5rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  :global(.security-icon) {
    font-size: 1.5rem;
    color: #0277bd;
    flex-shrink: 0;
    margin-top: 0.125rem;
  }

  .security-note p {
    margin: 0;
    color: #01579b;
    line-height: 1.6;
  }

  .resource-links {
    display: flex;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
  }

  .resource-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, #dc2626, #991b1b);
    color: white;
    text-decoration: none;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .resource-button.secondary {
    background: white;
    color: #dc2626;
    border: 2px solid #fecaca;
  }

  .resource-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  :global(.button-icon) {
    font-size: 1.125rem;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .ice-hero {
      padding: 2rem 1rem;
    }

    .hero-title {
      font-size: 2rem;
    }

    .hero-subtitle {
      font-size: 1rem;
    }

    .content-wrapper {
      padding: 2rem 1rem;
    }

    .section-title {
      font-size: 1.5rem;
    }

    .content-card {
      padding: 1.5rem;
    }

    .evidence-grid {
      grid-template-columns: 1fr;
    }

    .contact-method {
      flex-direction: column;
      text-align: center;
    }

    .resource-links {
      flex-direction: column;
    }

    .resource-button {
      justify-content: center;
    }
  }

  @media (max-width: 480px) {
    .hero-title {
      font-size: 1.75rem;
    }

    .section-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .alert-card,
    .disclaimer-card,
    .security-note {
      flex-direction: column;
      text-align: center;
    }
  }
</style>