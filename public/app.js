const state = {
  apps: [],
  category: "All",
  query: "",
};

const grid = document.querySelector("#app-grid");
const filters = document.querySelector("#filters");
const search = document.querySelector("#search");
const resultCount = document.querySelector("#result-count");
const emptyState = document.querySelector("#empty-state");
const clearSearch = document.querySelector("#clear-search");

function normalise(value) {
  return value.toLocaleLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}

function visibleApps() {
  const needle = normalise(state.query.trim());
  return state.apps.filter((app) => {
    const inCategory = state.category === "All" || app.category === state.category;
    const haystack = normalise(`${app.title} ${app.description} ${app.category} ${app.slug}`);
    return inCategory && (!needle || haystack.includes(needle));
  });
}

function card(app, index) {
  const link = document.createElement("a");
  link.className = "app-card";
  link.href = app.url;
  link.style.setProperty("--accent", app.accent);
  link.style.setProperty("--delay", `${Math.min(index, 12) * 28}ms`);
  link.dataset.category = app.category;
  link.innerHTML = `
    <span class="card-topline">
      <span class="monogram" aria-hidden="true">${app.symbol}</span>
      <span class="category-label">${app.category}</span>
      <span class="arrow" aria-hidden="true">↗</span>
    </span>
    <span class="card-copy">
      <strong>${app.title}</strong>
      <span>${app.description}</span>
    </span>
    <span class="card-host">${app.slug}.apps.kibk.net</span>
  `;
  return link;
}

function render() {
  const apps = visibleApps();
  grid.replaceChildren(...apps.map(card));
  grid.setAttribute("aria-busy", "false");
  emptyState.hidden = apps.length !== 0;
  resultCount.textContent = `${apps.length} ${apps.length === 1 ? "place" : "places"}`;

  for (const button of filters.querySelectorAll("button")) {
    const selected = button.dataset.category === state.category;
    button.classList.toggle("active", selected);
    button.setAttribute("aria-pressed", String(selected));
  }
}

function renderFilters() {
  const categories = ["All", ...new Set(state.apps.map((app) => app.category))];
  const buttons = categories.map((category) => {
    const button = document.createElement("button");
    const count = category === "All"
      ? state.apps.length
      : state.apps.filter((app) => app.category === category).length;
    button.type = "button";
    button.dataset.category = category;
    button.innerHTML = `<span>${category}</span><small>${count}</small>`;
    button.addEventListener("click", () => {
      state.category = category;
      render();
    });
    return button;
  });
  filters.replaceChildren(...buttons);
}

search.addEventListener("input", () => {
  state.query = search.value;
  render();
});

clearSearch.addEventListener("click", () => {
  search.value = "";
  state.query = "";
  state.category = "All";
  search.focus();
  render();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "/" && document.activeElement !== search) {
    event.preventDefault();
    search.focus();
  }
  if (event.key === "Escape" && document.activeElement === search) {
    search.value = "";
    state.query = "";
    search.blur();
    render();
  }
});

fetch("/apps.json", { cache: "no-store" })
  .then((response) => {
    if (!response.ok) throw new Error(`Catalogue request failed: ${response.status}`);
    return response.json();
  })
  .then((apps) => {
    state.apps = apps;
    renderFilters();
    render();
  })
  .catch((error) => {
    console.error(error);
    grid.setAttribute("aria-busy", "false");
    resultCount.textContent = "Catalogue unavailable";
    emptyState.hidden = false;
    emptyState.querySelector("p").textContent = "The collection could not be loaded.";
    clearSearch.hidden = true;
  });
