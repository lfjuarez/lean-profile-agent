// ?lang=en swaps every [data-en] text; Spanish is the default written in the markup.
if (new URLSearchParams(location.search).get("lang") === "en") {
  document.documentElement.lang = "en";
  document.querySelectorAll("[data-en]").forEach((el) => { el.innerHTML = el.dataset.en; });
}
