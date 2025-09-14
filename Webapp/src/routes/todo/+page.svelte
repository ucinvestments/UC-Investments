<script>
  import { fade, fly, scale } from "svelte/transition";
  import { flip } from "svelte/animate";
  import { onMount } from "svelte";
  import Icon from "@iconify/svelte";

  let mounted = false;

  // Project todos organized by category
  let todos = {
    dataCollection: {
      title: "Data Collection & Processing",
      icon: "mdi:database-search",
      items: [
        { id: 1, text: "Automate quarterly UC investment report downloads", completed: false, priority: "high" },
        { id: 2, text: "Implement PDF parser for new investment disclosures", completed: false, priority: "high" },
        { id: 3, text: "Create data validation pipeline for fund holdings", completed: false, priority: "medium" },
        { id: 4, text: "Set up automated SEC filing scraper (13F, 13D, 13G)", completed: false, priority: "high" },
        { id: 5, text: "Build historical data archive system", completed: false, priority: "low" },
        { id: 6, text: "Integrate Whale Wisdom API for hedge fund data", completed: false, priority: "medium" }
      ]
    },
    frontend: {
      title: "Frontend Features",
      icon: "mdi:application-brackets",
      items: [
        { id: 7, text: "Add search functionality for specific investments", completed: false, priority: "high" },
        { id: 8, text: "Implement time-series visualization for portfolio changes", completed: false, priority: "medium" },
        { id: 9, text: "Create detailed investment drill-down views", completed: false, priority: "medium" },
        { id: 10, text: "Add export functionality (CSV, PDF reports)", completed: false, priority: "low" },
        { id: 11, text: "Build comparison tool for UC campuses", completed: false, priority: "medium" },
        { id: 12, text: "Implement dark mode toggle", completed: false, priority: "low" },
        { id: 13, text: "Add mobile-responsive data tables", completed: false, priority: "high" }
      ]
    },
    analysis: {
      title: "Analysis & Research",
      icon: "mdi:chart-line",
      items: [
        { id: 14, text: "Analyze remaining $59B unaccounted investments", completed: false, priority: "high" },
        { id: 15, text: "Research foreign hedge fund holdings", completed: false, priority: "medium" },
        { id: 16, text: "Create ESG scoring methodology", completed: false, priority: "medium" },
        { id: 17, text: "Implement carbon footprint calculator", completed: false, priority: "low" },
        { id: 18, text: "Track fossil fuel divestment progress", completed: false, priority: "high" },
        { id: 19, text: "Analyze investment performance metrics", completed: false, priority: "medium" }
      ]
    },
    infrastructure: {
      title: "Infrastructure & DevOps",
      icon: "mdi:server",
      items: [
        { id: 20, text: "Migrate backend to edge functions", completed: false, priority: "medium" },
        { id: 21, text: "Implement caching strategy for API responses", completed: false, priority: "high" },
        { id: 22, text: "Set up CI/CD pipeline for automated testing", completed: false, priority: "medium" },
        { id: 23, text: "Create backup and recovery system", completed: false, priority: "high" },
        { id: 24, text: "Implement rate limiting for API endpoints", completed: false, priority: "low" },
        { id: 25, text: "Set up monitoring and alerting", completed: false, priority: "medium" }
      ]
    },
    documentation: {
      title: "Documentation & Outreach",
      icon: "mdi:book-open-variant",
      items: [
        { id: 26, text: "Write comprehensive API documentation", completed: false, priority: "medium" },
        { id: 27, text: "Create contributor guidelines", completed: false, priority: "low" },
        { id: 28, text: "Document data collection methodology", completed: false, priority: "high" },
        { id: 29, text: "Publish research findings whitepaper", completed: false, priority: "medium" },
        { id: 30, text: "Create video tutorials for using the platform", completed: false, priority: "low" },
        { id: 31, text: "Reach out to other UC campuses for collaboration", completed: false, priority: "medium" }
      ]
    }
  };

  // Stats calculation
  $: totalTodos = Object.values(todos).reduce((acc, cat) => acc + cat.items.length, 0);
  $: completedTodos = Object.values(todos).reduce(
    (acc, cat) => acc + cat.items.filter(item => item.completed).length,
    0
  );
  $: highPriorityCount = Object.values(todos).reduce(
    (acc, cat) => acc + cat.items.filter(item => item.priority === "high" && !item.completed).length,
    0
  );

  function toggleTodo(categoryKey, todoId) {
    todos[categoryKey].items = todos[categoryKey].items.map(item =>
      item.id === todoId ? { ...item, completed: !item.completed } : item
    );
  }

  function getPriorityColor(priority) {
    switch(priority) {
      case 'high': return 'var(--golden-gate)';
      case 'medium': return 'var(--founder)';
      case 'low': return 'var(--sec)';
      default: return 'var(--text-secondary)';
    }
  }

  onMount(() => {
    mounted = true;
  });
</script>

{#if mounted}
  <div class="todo-container">
    <!-- Hero Section -->
    <div class="todo-hero" in:fade={{ duration: 800 }}>
      <div class="hero-content">
        <Icon icon="mdi:clipboard-list" class="hero-icon" />
        <h1 class="hero-title">Project Roadmap</h1>
        <p class="hero-subtitle">
          Track our progress on improving UC investment transparency
        </p>
      </div>
    </div>

    <!-- Stats Bar -->
    <div class="stats-bar" in:fly={{ y: 20, duration: 600, delay: 200 }}>
      <div class="stat-item">
        <Icon icon="mdi:chart-donut" class="stat-icon" />
        <div class="stat-content">
          <div class="stat-value">{completedTodos}/{totalTodos}</div>
          <div class="stat-label">Tasks Completed</div>
        </div>
      </div>
      <div class="stat-item">
        <Icon icon="mdi:progress-clock" class="stat-icon" />
        <div class="stat-content">
          <div class="stat-value">{Math.round((completedTodos / totalTodos) * 100)}%</div>
          <div class="stat-label">Overall Progress</div>
        </div>
      </div>
      <div class="stat-item">
        <Icon icon="mdi:alert-circle" class="stat-icon high-priority" />
        <div class="stat-content">
          <div class="stat-value">{highPriorityCount}</div>
          <div class="stat-label">High Priority</div>
        </div>
      </div>
    </div>

    <!-- Todo Categories -->
    <div class="content-wrapper">
      {#each Object.entries(todos) as [categoryKey, category], i}
        <section
          class="todo-section"
          in:fly={{ y: 30, duration: 600, delay: 400 + i * 100 }}
        >
          <div class="section-header">
            <Icon icon={category.icon} class="section-icon" />
            <h2 class="section-title">{category.title}</h2>
            <div class="section-progress">
              {category.items.filter(item => item.completed).length}/{category.items.length}
            </div>
          </div>

          <div class="todo-card">
            <div class="todo-list">
              {#each category.items as todo (todo.id)}
                <div
                  class="todo-item"
                  class:completed={todo.completed}
                  animate:flip={{ duration: 300 }}
                >
                  <button
                    class="todo-checkbox"
                    class:checked={todo.completed}
                    on:click={() => toggleTodo(categoryKey, todo.id)}
                    aria-label={todo.completed ? "Mark as incomplete" : "Mark as complete"}
                  >
                    {#if todo.completed}
                      <Icon icon="mdi:check" class="check-icon" />
                    {/if}
                  </button>

                  <span class="todo-text">{todo.text}</span>

                  <span
                    class="priority-badge"
                    style="background-color: {getPriorityColor(todo.priority)}20; color: {getPriorityColor(todo.priority)}"
                  >
                    {todo.priority}
                  </span>
                </div>
              {/each}
            </div>
          </div>
        </section>
      {/each}

      <!-- Call to Action -->
      <section
        class="cta-section"
        in:fly={{ y: 30, duration: 600, delay: 1000 }}
      >
        <div class="cta-card">
          <Icon icon="mdi:rocket-launch" class="cta-icon" />
          <h2 class="cta-title">Want to Help?</h2>
          <p class="cta-text">
            Join us in making UC investments more transparent. Whether you're interested in
            data analysis, web development, or research, there's a place for you in this project.
          </p>
          <div class="cta-actions">
            <a
              href="https://github.com/TheArctesian/UC-Investments"
              target="_blank"
              rel="noopener noreferrer"
              class="action-button"
            >
              <Icon icon="mdi:github" class="button-icon" />
              Contribute on GitHub
            </a>
            <a
              href="mailto:dev@ucinvestments.info"
              class="action-button secondary"
            >
              <Icon icon="mdi:email" class="button-icon" />
              Get in Touch
            </a>
          </div>
        </div>
      </section>
    </div>
  </div>
{/if}

<style>
  .todo-container {
    min-height: 100vh;
    background: linear-gradient(to bottom, var(--bg), var(--bg-secondary));
  }

  .todo-hero {
    background: linear-gradient(135deg, var(--pri) 0%, var(--founder) 100%);
    padding: 3rem 2rem;
    text-align: center;
    position: relative;
    overflow: hidden;
  }

  .todo-hero::before {
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
    color: var(--sec);
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

  /* Stats Bar */
  .stats-bar {
    max-width: 1200px;
    margin: -2rem auto 3rem;
    padding: 0 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    position: relative;
    z-index: 2;
  }

  .stat-item {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: all 0.3s ease;
  }

  .stat-item:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
  }

  :global(.stat-icon) {
    font-size: 2rem;
    color: var(--founder);
  }

  :global(.stat-icon.high-priority) {
    color: var(--golden-gate);
  }

  .stat-content {
    flex: 1;
  }

  .stat-value {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--pri);
    line-height: 1;
  }

  .stat-label {
    font-size: 0.875rem;
    color: var(--text-secondary);
    margin-top: 0.25rem;
  }

  /* Content */
  .content-wrapper {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 2rem 3rem;
  }

  .todo-section {
    margin-bottom: 3rem;
  }

  .section-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }

  :global(.section-icon) {
    font-size: 2rem;
    color: var(--founder);
  }

  .section-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--pri);
    margin: 0;
    letter-spacing: -0.01em;
    flex: 1;
  }

  .section-progress {
    background: var(--bg-secondary);
    padding: 0.375rem 0.75rem;
    border-radius: 0.5rem;
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
  }

  .todo-card {
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(20px);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
  }

  .todo-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .todo-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem 1.25rem;
    background: var(--bg);
    border-radius: 0.75rem;
    border: 1px solid var(--border);
    transition: all 0.3s ease;
  }

  .todo-item:hover {
    transform: translateX(4px);
    box-shadow: var(--shadow-sm);
  }

  .todo-item.completed {
    opacity: 0.6;
  }

  .todo-item.completed .todo-text {
    text-decoration: line-through;
    color: var(--text-secondary);
  }

  .todo-checkbox {
    width: 1.5rem;
    height: 1.5rem;
    border-radius: 0.375rem;
    border: 2px solid var(--border);
    background: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .todo-checkbox:hover {
    border-color: var(--founder);
    transform: scale(1.1);
  }

  .todo-checkbox.checked {
    background: linear-gradient(135deg, var(--founder), var(--pri));
    border-color: var(--founder);
  }

  :global(.check-icon) {
    color: white;
    font-size: 1rem;
  }

  .todo-text {
    flex: 1;
    color: var(--text-primary);
    line-height: 1.5;
  }

  .priority-badge {
    padding: 0.25rem 0.625rem;
    border-radius: 0.375rem;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  /* CTA Section */
  .cta-section {
    margin-top: 4rem;
  }

  .cta-card {
    background: linear-gradient(135deg, var(--bg-secondary), white);
    border-radius: 1.5rem;
    border: 1px solid var(--border);
    padding: 3rem;
    text-align: center;
    box-shadow: var(--shadow-md);
  }

  :global(.cta-icon) {
    font-size: 3rem;
    color: var(--founder);
    margin-bottom: 1rem;
  }

  .cta-title {
    font-family: "Space Grotesk", sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--pri);
    margin-bottom: 1rem;
  }

  .cta-text {
    font-size: 1.125rem;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 600px;
    margin: 0 auto 2rem;
  }

  .cta-actions {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
  }

  .action-button {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.875rem 1.5rem;
    background: linear-gradient(135deg, var(--founder), var(--pri));
    color: white;
    text-decoration: none;
    border-radius: 0.75rem;
    font-weight: 600;
    transition: all 0.3s ease;
    box-shadow: var(--shadow-sm);
  }

  .action-button.secondary {
    background: white;
    color: var(--pri);
    border: 2px solid var(--border);
  }

  .action-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  :global(.button-icon) {
    font-size: 1.125rem;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .todo-hero {
      padding: 2rem 1rem;
    }

    .hero-title {
      font-size: 2rem;
    }

    .stats-bar {
      margin: -1.5rem 1rem 2rem;
      padding: 0;
    }

    .content-wrapper {
      padding: 0 1rem 2rem;
    }

    .section-header {
      flex-wrap: wrap;
    }

    .section-title {
      font-size: 1.5rem;
    }

    .todo-card {
      padding: 1rem;
    }

    .todo-item {
      padding: 0.875rem 1rem;
    }

    .cta-card {
      padding: 2rem 1.5rem;
    }

    .cta-actions {
      flex-direction: column;
    }

    .action-button {
      width: 100%;
      justify-content: center;
    }
  }

  @media (max-width: 480px) {
    .hero-title {
      font-size: 1.75rem;
    }

    .stats-bar {
      grid-template-columns: 1fr;
    }

    .todo-item {
      flex-wrap: wrap;
    }

    .priority-badge {
      margin-left: 2.5rem;
    }
  }
</style>